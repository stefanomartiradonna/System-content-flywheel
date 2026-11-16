#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_esterno.py - Fase 5 del content-cockpit: copertura completa di autori e temi, ogni lunedi.

Il problema che risolve: la Fase 5 e' fatta di molte letture (autori x canali, temi core).
Se il modello ne salta una, nessuno se ne accorge. Qui la copertura non e' una raccomandazione in un
prompt, e' un registro: una riga per ogni lettura dovuta, e un comando (`verifica`) che esce con errore
finche resta una riga aperta. La Fase 6 non parte se `verifica` non da exit 0.

Quattro comandi (riprova: a fine Fase 5 rilegge con lo script le righe ancora "da_riprovare";
un canale che non risponde non si abbandona, vedi MIN_TENTATIVI):

  scan      Legge la watchlist, costruisce il registro (una riga per ogni autore x canale, per ogni tema
            core). Legge DA SOLO i canali che hanno un feed (YouTube, newsletter) e
            chiude quelle righe. Le altre (LinkedIn, X, Instagram, newsletter senza feed, temi)
            restano "da_leggere": le legge il modello e le chiude con `segna`.
  segna     Chiude una riga: --id, --esito contenuti|niente|non_raggiungibile, --n, --nota (sempre
            obbligatoria: cosa hai letto davvero, o perche non hai potuto).
  verifica  Exit 0 solo se OGNI riga della watchlist e' chiusa. Altrimenti stampa le righe aperte, exit 1.

Solo libreria standard di Python 3.8+. Nessuna chiave. Funziona su Windows (`py -3 scripts\\scan_esterno.py`).
I feed YouTube e Substack sono pubblici: niente API, niente quota. Se il feed YouTube non risponde
(succede per ore, con 404), lo script legge la pagina pubblica del canale, schede Video e Short.

Dati scritti (nel repo privato, default accanto al repo flywheel):
  linkedin/scan-esterno/copertura-AAAA-MM-GG.csv   il registro
  linkedin/scan-esterno/scan-esterno-AAAA-MM-GG.csv  i contenuti letti dallo script
"""
import argparse
import csv
import datetime as dt
import email.utils
import html
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from statistics import median
from urllib.parse import urlparse

UA = "Mozilla/5.0 (compatible; content-cockpit/1.0)"
SOGLIA_FERMO_SETTIMANE = 8          # stessa soglia di Fase 9, loop C
SOGLIA_FEED_OBSOLETO_SETTIMANE = 26  # un feed newsletter fermo da piu' di cosi' non chiude la riga
SOGLIA_FUORI_SCALA = 3.0            # views / mediana del canale
TENUTO = "[tenuto]"                 # marcatore nella cella: Stefano ha deciso di tenere il canale
CAMPI_REGISTRO = ["id", "tipo", "voce", "canale", "url", "modo", "esito", "n_contenuti", "nota",
                  "tentativi"]
# Un canale che non risponde non si abbandona (richiesta di Stefano, 16/11/2026): resta aperto come
# "da_riprovare" e si riprende a fine Fase 5. Si chiude come non raggiungibile solo dopo
# MIN_TENTATIVI tentativi falliti, distanti almeno GAP_TENTATIVI_MIN minuti, di cui almeno uno a mano.
# Senza limite un sito giu' per un giorno bloccherebbe il report del lunedi' per sempre.
MIN_TENTATIVI = 3
GAP_TENTATIVI_MIN = 10
DA_RIPROVARE = "da_riprovare"
CAMPI_SCAN = ["autore", "canale", "data", "titolo", "url", "views", "mediana_canale",
              "rapporto_mediana", "estratto"]
ESITI_CHIUSI = {"contenuti", "niente_nella_finestra", "non_raggiungibile"}
MAPPA_ESITI = {"contenuti": "contenuti", "niente": "niente_nella_finestra",
               "niente_nella_finestra": "niente_nella_finestra",
               "non_raggiungibile": "non_raggiungibile"}

SCRIPT_DIR = Path(__file__).resolve().parent
FLYWHEEL = SCRIPT_DIR.parent
DEFAULT_OUT = FLYWHEEL.parent / "claude-private-refs" / "linkedin" / "scan-esterno"
DEFAULT_WATCHLIST = (Path.home() / ".claude" / "skills" / "content-cockpit" / "references"
                     / "watchlist.md")

CANALI = {"linkedin": "linkedin", "newsletter": "newsletter", "x": "x",
          "youtube": "youtube", "instagram": "instagram"}


# ----------------------------------------------------------------------------- utilita

def out(*a):
    print(*a, flush=True)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fail(msg, code=2):
    out("ERRORE: " + msg)
    sys.exit(code)


def fetch(url, tentativi=2, timeout=25, headers=None, riprova_404=False):
    """riprova_404: i feed YouTube rispondono 404 a intermittenza (16/11/2026: 404 su tutti e cinque i
    canali la mattina, 200 due ore dopo). Per loro un 404 non e' definitivo e si riprova."""
    ultimo = None
    h = {"User-Agent": UA,
         "Accept": "application/atom+xml,application/rss+xml,application/xml,text/xml,*/*"}
    h.update(headers or {})
    for k in range(tentativi):
        try:
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(), None
        except urllib.error.HTTPError as e:
            ultimo = "HTTP %s" % e.code
            if e.code in (403, 410) or (e.code == 404 and not riprova_404):
                break
        except Exception as e:  # rete, timeout, TLS
            ultimo = "%s: %s" % (type(e).__name__, e)
        time.sleep(1.5 * (k + 1))
    return None, ultimo


def tentativi(r):
    """Lista dei tentativi falliti: 'AAAA-MM-GGTHH:MM|script' o '...|manuale', separati da ';'."""
    return [t for t in (r.get("tentativi") or "").split(";") if t.strip()]


def aggiungi_tentativo(r, modo, ora=None):
    """Registra un tentativo fallito. Restituisce False se e' troppo vicino al precedente: in quel caso
    non conta, perche' riprovare dopo un minuto non e' 'tornarci a fine analisi'."""
    ora = ora or dt.datetime.now()
    lista = tentativi(r)
    if lista:
        prec = dt.datetime.fromisoformat(lista[-1].split("|")[0])
        if (ora - prec).total_seconds() < GAP_TENTATIVI_MIN * 60:
            return False
    lista.append("%s|%s" % (ora.strftime("%Y-%m-%dT%H:%M"), modo))
    r["tentativi"] = ";".join(lista)
    return True


def puo_chiudere_non_raggiungibile(r):
    lista = tentativi(r)
    return len(lista) >= MIN_TENTATIVI and any(t.endswith("|manuale") for t in lista)


def stato_tentativi(r):
    lista = tentativi(r)
    manuali = sum(1 for t in lista if t.endswith("|manuale"))
    return "%d tentativi su %d (di cui a mano %d, ne serve almeno 1)" % (len(lista), MIN_TENTATIVI, manuali)


def a_data(testo):
    """Restituisce una datetime.date (UTC) o None."""
    if not testo:
        return None
    testo = testo.strip()
    try:
        d = email.utils.parsedate_to_datetime(testo)
    except Exception:
        d = None
    if d is None:
        try:
            d = dt.datetime.fromisoformat(testo.replace("Z", "+00:00"))
        except Exception:
            return None
    if d.tzinfo is not None:
        d = d.astimezone(dt.timezone.utc)
    return d.date()


def pulisci_html(s, n=240):
    s = re.sub(r"<[^>]+>", " ", html.unescape(s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n]


def parse_feed(data):
    """Atom (YouTube) o RSS (Substack e altri). Lancia ET.ParseError se non e' XML."""
    root = ET.fromstring(data)
    items = []
    tag = root.tag.lower()
    if tag.endswith("feed"):
        ns = {"a": "http://www.w3.org/2005/Atom", "m": "http://search.yahoo.com/mrss/"}
        for e in root.findall("a:entry", ns):
            link = e.find("a:link", ns)
            st = e.find(".//m:statistics", ns)
            views = None
            if st is not None and str(st.get("views", "")).isdigit():
                views = int(st.get("views"))
            items.append({
                "titolo": (e.findtext("a:title", "", ns) or "").strip(),
                "url": link.get("href") if link is not None else "",
                "data": a_data(e.findtext("a:published", "", ns) or e.findtext("a:updated", "", ns)),
                "views": views,
                "estratto": pulisci_html(e.findtext(".//m:description", "", ns)),
            })
    elif tag.endswith("rss"):
        enc = "{http://purl.org/rss/1.0/modules/content/}encoded"
        for it in root.iter("item"):
            corpo = it.findtext(enc) or ""
            items.append({
                "titolo": (it.findtext("title") or "").strip(),
                "url": (it.findtext("link") or "").strip(),
                "data": a_data(it.findtext("pubDate")),
                "views": None,
                "estratto": pulisci_html(it.findtext("description")),
                # Substack: un post a pagamento arriva nel feed troncato e finisce con "Read more".
                # Euristica verificata sul feed di Category Pirates (2026-11-14), non una garanzia.
                "troncato": "Read more" in corpo[-600:],
            })
    else:
        raise ET.ParseError("radice XML non riconosciuta: " + root.tag)
    return items


# ----------------------------------------------------------------------------- watchlist

def dividi_riga(riga):
    return [c.strip() for c in riga.strip().strip("|").split("|")]


def leggi_tabelle(testo):
    righe = testo.splitlines()
    tabelle = []
    i = 0
    while i < len(righe):
        if (righe[i].lstrip().startswith("|") and i + 1 < len(righe)
                and re.match(r"^\s*\|[\s\-:|]+\|\s*$", righe[i + 1])):
            intest = dividi_riga(righe[i])
            corpo = []
            j = i + 2
            while j < len(righe) and righe[j].lstrip().startswith("|"):
                corpo.append(dividi_riga(righe[j]))
                j += 1
            tabelle.append((intest, corpo))
            i = j
        else:
            i += 1
    return tabelle


URL_RE = re.compile(r"^(https?://\S+|(?:www\.)?(?:linkedin|twitter|x|instagram|youtube)\.com/\S+)")


def bersaglio(cella, canale):
    """URL monitorabile di una cella, oppure None.

    Convenzione (vedi watchlist.md): una cella e' monitorata solo se INIZIA con un URL (o, per X, con
    un @handle). Qualunque altra cosa ("—", "non trovato", "escluso", "nessun canale", ...) significa
    che quel canale non si legge."""
    c = cella.strip()
    m = URL_RE.match(c)
    if m:
        url = m.group(1).rstrip(".,;)")
        return url if url.startswith("http") else "https://" + url
    if canale == "x":
        m = re.match(r"^@([A-Za-z0-9_]{1,30})\b", c)
        if m:
            return "https://x.com/" + m.group(1)
    return None


def costruisci_righe(testo):
    tabelle = leggi_tabelle(testo)
    autori = [t for t in tabelle if t[0] and t[0][0].lower() == "autore"]
    temi = [t for t in tabelle if t[0] and t[0][0].lower() == "tema"]
    if len(autori) != 1:
        fail("nella watchlist deve esserci esattamente una tabella con prima colonna 'Autore' "
             "(trovate: %d)" % len(autori))
    if len(temi) != 1:
        fail("nella watchlist deve esserci esattamente una tabella con prima colonna 'Tema' "
             "(trovate: %d)" % len(temi))
    intest, corpo = autori[0]
    idx = {}
    for k, nome in enumerate(intest):
        n = nome.lower()
        for chiave, canale in CANALI.items():
            if n.startswith(chiave):
                idx[canale] = k
    mancanti = [c for c in CANALI.values() if c not in idx]
    if mancanti:
        fail("colonne mancanti nella tabella autori: " + ", ".join(mancanti))
    righe = []
    for r in corpo:
        if len(r) != len(intest):
            fail("riga autori malformata (%d celle invece di %d): %s"
                 % (len(r), len(intest), r[0] if r else "?"))
        nome = r[0]
        base = slug(nome.split("(")[0])
        for canale, k in idx.items():
            url = bersaglio(r[k], canale)
            if not url:
                continue
            righe.append({"id": "%s-%s" % (base, canale), "tipo": "autore", "voce": nome,
                          "canale": canale, "url": url, "cella": r[k]})
    for r in temi[0][1]:
        if len(r) < 2:
            fail("riga temi malformata: %s" % r)
        righe.append({"id": "tema-" + slug(r[0]), "tipo": "tema", "voce": r[0], "canale": "web",
                      "url": "", "cella": r[1]})
    visti = set()
    for r in righe:
        if r["id"] in visti:
            fail("id duplicato nel registro: " + r["id"])
        visti.add(r["id"])
    n_aut = len({r["voce"] for r in righe if r["tipo"] == "autore"})
    if n_aut == 0 or not any(r["tipo"] == "tema" for r in righe):
        fail("watchlist vuota: nessun autore o nessun tema")
    return righe


# ----------------------------------------------------------------------------- lettura

def suggerimento_manuale(r):
    c = r["canale"]
    if r["tipo"] == "tema":
        return "WebSearch sugli ultimi 7-10 giorni. Query base: " + r["cella"]
    if c == "linkedin":
        return "Chrome loggato: " + r["url"].rstrip("/") + "/recent-activity/all/"
    if c == "x":
        return "WebSearch sul profilo " + r["url"] + ", poi citazioni di terzi"
    if c == "instagram":
        return "WebSearch/WebFetch; spesso poco recuperabile, dichiaralo"
    if c == "newsletter":
        return "Nessun feed trovato: cerca l'ultimo numero via web " + r["url"]
    return ""


def finestra_ok(d, dal, al):
    return d is not None and dal <= d <= al


# Pagina canale: fallback quando il feed RSS non risponde. Il consenso cookie europeo si salta con il
# cookie SOCS; hl=en rende le eta' relative leggibili ("3d ago", "2w ago").
YT_BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/130.0 Safari/537.36",
    "Accept": "text/html,*/*", "Accept-Language": "en-US,en;q=0.9", "Cookie": "SOCS=CAI"}
ETA_RE = re.compile(r"^(\d+)\s*(min|h|d|w|mo|y)\b")
GIORNI_UNITA = {"min": 0, "h": 0, "d": 1, "w": 7, "mo": 30, "y": 365}


def numero_views(s):
    m = re.match(r"^([\d.,]+)\s*([KMB]?)", (s or "").replace(",", ""))
    if not m:
        return None
    n = float(m.group(1))
    return int(n * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2)])


def lockups(o, acc):
    if isinstance(o, dict):
        if "lockupViewModel" in o:
            v = o["lockupViewModel"]
            meta = v.get("metadata", {}).get("lockupMetadataViewModel", {})
            parti = [p.get("text", {}).get("content", "")
                     for row in meta.get("metadata", {}).get("contentMetadataViewModel", {})
                     .get("metadataRows", []) for p in row.get("metadataParts", [])]
            acc.append((v.get("contentId"), meta.get("title", {}).get("content", ""), parti))
        for x in o.values():
            lockups(x, acc)
    elif isinstance(o, list):
        for x in o:
            lockups(x, acc)
    return acc


def shorts(o, acc):
    if isinstance(o, dict):
        if "shortsLockupViewModel" in o:
            v = o["shortsLockupViewModel"]
            ov = v.get("overlayMetadata", {})
            vid = (v.get("entityId") or "").replace("shorts-shelf-item-", "")
            acc.append((vid, ov.get("primaryText", {}).get("content", ""),
                        (ov.get("secondaryText", {}).get("content", "") or "").replace(" views", "")))
            return acc
        for x in o.values():
            shorts(x, acc)
    elif isinstance(o, list):
        for x in o:
            shorts(x, acc)
    return acc


def initial_data(url):
    data, err = fetch(url, headers=YT_BROWSER_HEADERS)
    if data is None:
        return None, str(err)
    m = re.search(r"ytInitialData\s*=\s*(\{.*?\});\s*</script>", data.decode("utf-8", "replace"), re.S)
    if not m:
        return None, "senza ytInitialData (pagina di consenso o layout cambiato)"
    try:
        return json.loads(m.group(1)), None
    except ValueError as e:
        return None, "JSON illeggibile: %s" % e


def data_esatta(vid):
    w, _ = fetch("https://www.youtube.com/watch?v=%s&hl=en" % vid, headers=YT_BROWSER_HEADERS)
    md = re.search(r'"(?:publishDate|uploadDate)":"([^"]+)"', w.decode("utf-8", "replace")) if w else None
    return a_data(md.group(1)) if md else None


def leggi_pagina_canale(channel_id, oggi, dal, max_short=8):
    """Fallback del feed: legge le schede Video e Short della pagina canale. Restituisce (items, errore)
    nello stesso formato di parse_feed. Le date esatte vengono dalla pagina del singolo video: per il
    video piu' recente sempre (serve a dire se il canale e' fermo), per quelli entro tre settimane, e per
    gli Short fino al primo piu' vecchio dell'inizio finestra (la scheda Short non mostra date).
    Le visualizzazioni arrivano arrotondate (7.2K). Gli Short hanno il titolo prefissato con [Short],
    come promemoria che la mediana del canale mescola i due formati (vale anche per il feed)."""
    base = "https://www.youtube.com/channel/%s/%s?hl=en&gl=US"
    d_video, err_v = initial_data(base % (channel_id, "videos"))
    d_short, err_s = initial_data(base % (channel_id, "shorts"))
    if d_video is None and d_short is None:
        return None, "pagina canale: video %s, short %s" % (err_v, err_s)
    items = []
    limite = None   # la scheda e' dal piu' recente: una data stimata non puo' superare quella sopra
    for k, (vid, titolo, parti) in enumerate(lockups(d_video, []) if d_video else []):
        if not vid:
            continue
        eta = next((p for p in parti if ETA_RE.match(p or "")), "")
        me = ETA_RE.match(eta)
        giorni = int(me.group(1)) * GIORNI_UNITA[me.group(2)] if me else None
        data_v = oggi - dt.timedelta(days=giorni) if giorni is not None else None
        esatta = data_esatta(vid) if (k == 0 or (giorni is not None and giorni <= 21)) else None
        if esatta is None and data_v is not None and limite is not None:
            data_v = min(data_v, limite)
        limite = esatta or data_v or limite
        items.append({"titolo": titolo, "url": "https://www.youtube.com/watch?v=" + vid,
                      "data": esatta or data_v, "data_stimata": esatta is None,
                      "views": numero_views(parti[0]) if parti else None,
                      "estratto": "" if esatta else "eta' '%s' dalla pagina canale" % eta})
    for vid, titolo, viste in (shorts(d_short, []) if d_short else [])[:max_short]:
        if not vid:
            continue
        d = data_esatta(vid)
        items.append({"titolo": "[Short] " + titolo, "url": "https://www.youtube.com/shorts/" + vid,
                      "data": d, "data_stimata": d is None, "views": numero_views(viste),
                      "estratto": "" if d else "data non leggibile"})
        if d is not None and d < dal:
            break   # la scheda e' in ordine dal piu' recente: oltre la finestra si smette
    if not items:
        return None, "pagina canale letta ma nessun video trovato (layout cambiato?)"
    return items, None


def leggi_youtube(r, dal, al, oggi, contenuti):
    m = re.search(r"\bID\s+(UC[0-9A-Za-z_-]{22})", r["cella"]) or \
        re.search(r"/channel/(UC[0-9A-Za-z_-]{22})", r["cella"])
    if not m:
        r["modo"], r["esito"], r["nota"] = "manuale", "da_leggere", \
            "ID canale mancante nella cella YouTube della watchlist"
        return None
    feed = "https://www.youtube.com/feeds/videos.xml?channel_id=" + m.group(1)
    data, err = fetch(feed, tentativi=3, riprova_404=True)
    r["modo"] = "script"
    fonte = []
    items = None
    if data is not None:
        try:
            items = parse_feed(data)
        except ET.ParseError as e:
            err = "feed illeggibile: %s" % e
    if items is None:
        # Feed rotto non vuol dire canale fermo: si guarda la pagina del canale prima di decidere.
        items, err2 = leggi_pagina_canale(m.group(1), oggi, dal)
        if items is None:
            aggiungi_tentativo(r, "script")
            r["esito"], r["nota"] = DA_RIPROVARE, (
                "feed RSS: %s; %s. Riprova a fine Fase 5 con 'riprova', poi a mano da Chrome "
                "(schede Video E Short). %s" % (err, err2, stato_tentativi(r)))
            return None
        fonte.append("FEED RSS ROTTO (%s), letto dalla pagina canale: views arrotondate%s" % (
            err, ", alcune date stimate" if any(i.get("data_stimata") for i in items) else ""))
    # Short e video lunghi hanno visualizzazioni di ordini diversi: ognuno si confronta con la mediana
    # del suo formato (sul feed gli Short si riconoscono dal link /shorts/).
    def short(i):
        return "/shorts/" in i["url"]
    mediane = {}
    for fmt in (True, False):
        v = [i["views"] for i in items if i["views"] is not None and short(i) == fmt]
        mediane[fmt] = median(v) if v else None
    nuovi = [i for i in items if finestra_ok(i["data"], dal, al)]
    for i in nuovi:
        med = mediane[short(i)]
        rap = round(i["views"] / med, 2) if (i["views"] is not None and med) else ""
        titolo = i["titolo"] if (not short(i) or i["titolo"].startswith("[Short]")) else "[Short] " + i["titolo"]
        contenuti.append([r["voce"], "youtube", i["data"].isoformat(), titolo, i["url"],
                          "" if i["views"] is None else i["views"],
                          "" if med is None else med, rap, i["estratto"]])
        i["rapporto"] = rap
    note = list(fonte)
    ultimo = max((i["data"] for i in items if i["data"]), default=None)
    if not items:
        note.append("feed vuoto: il canale non ha video pubblici")
    elif ultimo is not None:
        sett = (oggi - ultimo).days // 7
        if sett >= SOGLIA_FERMO_SETTIMANE:
            note.append("FERMO da %d settimane (ultimo video %s, soglia %d)%s" % (
                sett, ultimo.isoformat(), SOGLIA_FERMO_SETTIMANE,
                ": tenuto su richiesta" if TENUTO in r["cella"] else
                ": candidato a uscire da YouTube"))
        else:
            note.append("ultimo video %s" % ultimo.isoformat())
    fuori = [i for i in nuovi if i.get("rapporto") not in (None, "") and i["rapporto"] >= SOGLIA_FUORI_SCALA]
    if fuori:
        note.append("%d video fuori scala (>= %.0fx la mediana del canale per lo stesso formato)" % (
            len(fuori), SOGLIA_FUORI_SCALA))
    r["n_contenuti"] = len(nuovi)
    r["esito"] = "contenuti" if nuovi else "niente_nella_finestra"
    r["nota"] = "; ".join(note)
    return ultimo


def candidati_feed(url):
    u = urlparse(url)
    origine = "%s://%s" % (u.scheme, u.netloc)
    cand = []
    base = url.rstrip("/")
    if u.netloc.endswith("substack.com") and u.path.startswith("/@"):
        return []   # profilo personale: non e' una pubblicazione, nessun feed
    for c in (base + "/feed", origine + "/feed", origine + "/rss", origine + "/rss.xml",
              origine + "/feed.xml", origine + "/index.xml"):
        if c not in cand:
            cand.append(c)
    return cand


def leggi_newsletter(r, dal, al, oggi, contenuti):
    r["modo"] = "manuale"
    errori_transitori = []
    for cand in candidati_feed(r["url"]):
        data, err = fetch(cand, tentativi=1)
        if data is None:
            # 404 su un indirizzo candidato e' normale (quel feed non esiste); timeout, 5xx o rete no.
            if err and not re.match(r"HTTP (403|404|410)$", err):
                errori_transitori.append("%s: %s" % (cand, err))
            continue
        try:
            items = parse_feed(data)
        except ET.ParseError:
            continue
        if not items:
            continue
        r["modo"] = "script"
        nuovi = [i for i in items if finestra_ok(i["data"], dal, al)]
        bloccati = [i for i in nuovi if i.get("troncato")]
        for i in nuovi:
            estratto = i["estratto"]
            if i.get("troncato"):
                estratto = "[BLOCCATO: feed troncato, chiedi a Stefano di incollare il testo] " + estratto
            contenuti.append([r["voce"], "newsletter", i["data"].isoformat(), i["titolo"], i["url"],
                              "", "", "", estratto])
        ultimo = max((i["data"] for i in items if i["data"]), default=None)
        sett = (oggi - ultimo).days // 7 if ultimo else None
        if not nuovi and (ultimo is None or sett >= SOGLIA_FEED_OBSOLETO_SETTIMANE):
            # Un feed fermo da mesi che non ha nulla nella finestra NON si chiude da solo come
            # "niente di nuovo": potrebbe essere la fonte sbagliata, e sarebbe un falso negativo.
            r["modo"] = "manuale"
            r["esito"] = "da_leggere"
            r["nota"] = ("il feed %s e' fermo dal %s (%s settimane): puo' non essere la fonte giusta. "
                         "Verifica dove pubblica oggi e leggi l'ultimo numero via web (%s)" % (
                             cand, ultimo.isoformat() if ultimo else "sempre",
                             sett if sett is not None else "?", r["url"]))
            return
        note = "feed %s; ultimo post %s" % (cand, ultimo.isoformat() if ultimo else "?")
        if nuovi:
            note += "; i post a pagamento arrivano solo con anteprima"
            if bloccati:
                note += "; BLOCCATI (%d, chiedi a Stefano di incollarli): %s" % (
                    len(bloccati), " | ".join(i["titolo"] for i in bloccati))
        elif sett is not None and sett >= SOGLIA_FERMO_SETTIMANE:
            note += ("; FERMO da %d settimane (soglia %d)%s" % (
                sett, SOGLIA_FERMO_SETTIMANE,
                ": tenuto su richiesta" if TENUTO in r["cella"] else
                ": candidato a uscire da questo canale"))
        r["n_contenuti"] = len(nuovi)
        r["esito"] = "contenuti" if nuovi else "niente_nella_finestra"
        r["nota"] = note
        return
    if errori_transitori:
        r["modo"] = "script"
        aggiungi_tentativo(r, "script")
        r["esito"] = DA_RIPROVARE
        r["nota"] = ("feed non raggiunto (%s). Riprova a fine Fase 5 con 'riprova', poi a mano. %s" % (
            "; ".join(errori_transitori[:2]), stato_tentativi(r)))
        return
    r["esito"] = "da_leggere"
    r["nota"] = suggerimento_manuale(r)


def leggi_riga_script(r, dal, al, oggi, contenuti):
    if r["tipo"] == "autore" and r["canale"] == "youtube":
        leggi_youtube(r, dal, al, oggi, contenuti)
    elif r["tipo"] == "autore" and r["canale"] == "newsletter":
        leggi_newsletter(r, dal, al, oggi, contenuti)
    else:
        r["nota"] = suggerimento_manuale(r)


def cmd_scan(a):
    wl = Path(a.watchlist)
    if not wl.exists():
        fail("watchlist non trovata: %s (usa --watchlist)" % wl)
    oggi = dt.date.fromisoformat(a.oggi) if a.oggi else dt.date.today()
    al = dt.date.fromisoformat(a.al) if a.al else oggi
    dal = dt.date.fromisoformat(a.dal) if a.dal else al - dt.timedelta(days=7)
    if dal > al:
        fail("--dal e' dopo --al")
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    f_reg = outdir / ("copertura-%s.csv" % oggi.isoformat())
    f_scan = outdir / ("scan-esterno-%s.csv" % oggi.isoformat())
    vecchio = {}
    if f_reg.exists():
        if not a.rifai:
            fail("registro di oggi gia' presente (%s). Per continuare usa 'verifica' e 'segna'. "
                 "Per rileggere i canali con feed senza perdere le righe gia' chiuse a mano usa "
                 "'scan --rifai'." % f_reg.name)
        with open(f_reg, newline="", encoding="utf-8") as fh:
            vecchio = {r["id"]: r for r in csv.DictReader(fh)}

    righe = costruisci_righe(wl.read_text(encoding="utf-8"))
    contenuti = []
    ferme = []
    out("Finestra: dal %s al %s (oggi %s). Righe dovute: %d" % (dal, al, oggi, len(righe)))
    for r in righe:
        v = vecchio.get(r["id"])
        r.update({"modo": "manuale", "esito": "da_leggere", "n_contenuti": "", "nota": "",
                  "tentativi": (v or {}).get("tentativi") or ""})
        leggi_riga_script(r, dal, al, oggi, contenuti)
        if r["modo"] == "manuale" and not r["nota"]:
            r["nota"] = suggerimento_manuale(r)
        if v and r["modo"] == "manuale" and (v.get("esito") in ESITI_CHIUSI or v.get("esito") == DA_RIPROVARE):
            r["esito"], r["n_contenuti"], r["nota"] = v["esito"], v["n_contenuti"], v["nota"]
        if "FERMO" in r["nota"] and TENUTO not in r["cella"]:
            ferme.append((r["voce"] + " [" + r["canale"] + "]", r["nota"]))

    with open(f_reg, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPI_REGISTRO, extrasaction="ignore")
        w.writeheader()
        w.writerows(righe)
    with open(f_scan, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(CAMPI_SCAN)
        w.writerows(contenuti)

    chiuse = [r for r in righe if r["esito"] in ESITI_CHIUSI]
    aperte = [r for r in righe if r["esito"] not in ESITI_CHIUSI]
    riprovare = [r for r in aperte if r["esito"] == DA_RIPROVARE]
    out("Chiuse dallo script: %d. Da leggere a mano: %d (di cui %d da riprovare)." % (
        len(chiuse), len(aperte), len(riprovare)))
    for r in riprovare:
        out("  DA RIPROVARE a fine Fase 5: %s [%s] %s" % (r["voce"], r["canale"], r["nota"]))
    nr = [r for r in chiuse if r["esito"] == "non_raggiungibile"]
    for r in nr:
        out("  NON RAGGIUNGIBILE: %s [%s] %s" % (r["voce"], r["canale"], r["nota"]))
    for voce, nota in ferme:
        out("  PROPOSTA USCITA CANALE: %s: %s" % (voce, nota))
    out("Contenuti letti dallo script: %d righe in %s" % (len(contenuti), f_scan))
    out("Registro: %s" % f_reg)
    out("Ora leggi le righe aperte e chiudile con 'segna'. Poi 'verifica' deve dare exit 0 "
        "prima della Fase 6.")
    stampa_aperte(aperte)


def stampa_aperte(aperte):
    if not aperte:
        return
    out("\nRIGHE DA LEGGERE (%d):" % len(aperte))
    for r in aperte:
        out("  %-34s %-10s %s" % (r["id"], r["canale"], r["nota"]))


# ----------------------------------------------------------------------------- registro

def trova_registro(a):
    if a.registro:
        p = Path(a.registro)
    else:
        trovati = sorted(Path(a.out).glob("copertura-*.csv"))
        if not trovati:
            fail("nessun registro in %s: lancia prima 'scan'" % a.out)
        p = trovati[-1]
    if not p.exists():
        fail("registro non trovato: %s" % p)
    return p


def leggi_registro(p):
    with open(p, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def scrivi_registro(p, righe):
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPI_REGISTRO, extrasaction="ignore")
        w.writeheader()
        w.writerows(righe)


def cmd_riprova(a):
    """Rilegge con lo script le righe da_riprovare (YouTube, newsletter con feed). Si lancia a fine
    Fase 5, dopo la lettura manuale: e' il 'tornarci a fine analisi'. Quelle che falliscono ancora
    restano aperte con un tentativo in piu'; dopo i tentativi dello script va provato a mano."""
    p = trova_registro(a)
    righe = leggi_registro(p)
    oggi = dt.date.fromisoformat(p.stem.replace("copertura-", ""))
    dal = dt.date.fromisoformat(a.dal)
    al = dt.date.fromisoformat(a.al) if a.al else oggi
    wl = {r["id"]: r for r in costruisci_righe(Path(a.watchlist).read_text(encoding="utf-8"))}
    contenuti = []
    target = [r for r in righe if r["esito"] == DA_RIPROVARE and r["modo"] == "script"]
    if not target:
        out("Nessuna riga da riprovare con lo script.")
    for r in target:
        r["cella"] = wl.get(r["id"], {}).get("cella", r.get("url", ""))
        prima = tentativi(r)
        leggi_riga_script(r, dal, al, oggi, contenuti)
        if r["esito"] == DA_RIPROVARE:
            contato = len(tentativi(r)) > len(prima)
            out("ANCORA GIU': %s [%s]. %s%s" % (r["voce"], r["canale"], stato_tentativi(r),
                "" if contato else " (tentativo non contato: meno di %d minuti dal precedente)" % GAP_TENTATIVI_MIN))
            if len(tentativi(r)) >= MIN_TENTATIVI - 1:
                out("   Ora provalo a mano da Chrome e chiudi con 'segna'.")
        else:
            out("RIUSCITA: %s [%s] -> %s" % (r["voce"], r["canale"], r["esito"]))
    scrivi_registro(p, righe)
    if contenuti:
        f_scan = p.parent / p.name.replace("copertura-", "scan-esterno-")
        with open(f_scan, "a", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(contenuti)
        out("Aggiunti %d contenuti a %s" % (len(contenuti), f_scan.name))
    stampa_aperte([r for r in righe if r["esito"] not in ESITI_CHIUSI])


def cmd_segna(a):
    esito = MAPPA_ESITI.get(a.esito)
    if not esito:
        fail("--esito deve essere contenuti, niente o non_raggiungibile")
    if not a.nota or len(a.nota.strip()) < 8:
        fail("--nota e' obbligatoria (almeno una frase): cosa hai letto davvero, o perche non hai "
             "potuto. Una riga chiusa senza nota non vale.")
    if esito == "contenuti" and (a.n is None or a.n < 1):
        fail("con esito 'contenuti' serve --n con il numero di contenuti letti (almeno 1)")
    p = trova_registro(a)
    righe = leggi_registro(p)
    for r in righe:
        if r["id"] == a.id:
            if r["modo"] == "script" and r["esito"] in ("contenuti", "niente_nella_finestra"):
                fail("la riga %s e' stata letta dallo script: rilancia 'scan --rifai' se serve. "
                     "Si puo' chiudere a mano solo una riga che lo script non ha potuto raggiungere." % a.id)
            if esito == "non_raggiungibile":
                # Un fallimento a mano e' un tentativo, non una chiusura: la riga si chiude solo
                # quando i tentativi bastano. Altrimenti resta aperta e si riprende a fine Fase 5.
                contato = aggiungi_tentativo(r, "manuale")
                if not contato:
                    fail("tentativo su %s non contato: meno di %d minuti dal precedente. Passa ad altre "
                         "righe e torna su questa a fine Fase 5. %s" % (
                             a.id, GAP_TENTATIVI_MIN, stato_tentativi(r)), code=1)
                r["nota"] = (r.get("nota", "") + " | " if r.get("nota") else "") + a.nota.strip()
                if not puo_chiudere_non_raggiungibile(r):
                    r["esito"] = DA_RIPROVARE
                    scrivi_registro(p, righe)
                    out("NON chiusa: %s resta da riprovare. %s. Torna su questa riga a fine Fase 5 "
                        "(e prova un altro metodo: Chrome, WebFetch, ricerca)." % (a.id, stato_tentativi(r)))
                    return
                r["esito"] = esito
                r["n_contenuti"] = 0
                scrivi_registro(p, righe)
                aperte = [x for x in righe if x["esito"] not in ESITI_CHIUSI]
                out("Chiusa come non raggiungibile dopo %s: %s. Restano %d righe aperte su %d." % (
                    stato_tentativi(r), a.id, len(aperte), len(righe)))
                return
            r["esito"] = esito
            r["n_contenuti"] = a.n if a.n is not None else 0
            r["nota"] = a.nota.strip()
            scrivi_registro(p, righe)
            aperte = [x for x in righe if x["esito"] not in ESITI_CHIUSI]
            out("Chiusa: %s -> %s. Restano %d righe aperte su %d." % (a.id, esito, len(aperte), len(righe)))
            return
    ids = ", ".join(r["id"] for r in righe[:6])
    fail("id non trovato: %s (esempi: %s ...)" % (a.id, ids))


def cmd_verifica(a):
    p = trova_registro(a)
    righe = leggi_registro(p)
    errori = []
    # 1. il registro deve contenere TUTTE le righe che la watchlist di oggi richiede
    wl = Path(a.watchlist)
    if wl.exists():
        dovute = {r["id"] for r in costruisci_righe(wl.read_text(encoding="utf-8"))}
        presenti = {r["id"] for r in righe}
        for i in sorted(dovute - presenti):
            errori.append("manca nel registro (watchlist modificata dopo lo scan?): " + i)
    else:
        out("Attenzione: watchlist non trovata (%s), controllo solo le righe del registro." % wl)
    # 2. ogni riga deve avere un esito chiuso e una nota
    aperte = [r for r in righe if r["esito"] not in ESITI_CHIUSI]
    senza_nota = [r for r in righe if r["esito"] in ESITI_CHIUSI and not (r["nota"] or "").strip()
                  and r["modo"] == "manuale"]
    tot = len(righe)
    conteggio = {}
    for r in righe:
        conteggio[r["esito"]] = conteggio.get(r["esito"], 0) + 1
    out("Registro %s: %d righe. %s" % (p.name, tot, ", ".join("%s=%d" % kv for kv in sorted(conteggio.items()))))
    if aperte:
        stampa_aperte(aperte)
    for r in senza_nota:
        errori.append("chiusa senza nota: " + r["id"])
    for r in righe:
        if r["esito"] == "non_raggiungibile" and not puo_chiudere_non_raggiungibile(r):
            errori.append("chiusa come non raggiungibile troppo presto: %s (%s). Riprovala." % (
                r["id"], stato_tentativi(r)))
    riprovare = [r for r in aperte if r["esito"] == DA_RIPROVARE]
    if riprovare:
        out("\nDA RIPROVARE (non abbandonarle: 'riprova' per quelle dello script, poi a mano):")
        for r in riprovare:
            out("  %-34s %s" % (r["id"], stato_tentativi(r)))
    for e in errori:
        out("  " + e)
    if aperte or errori:
        out("\nCOPERTURA INCOMPLETA: %d righe aperte, %d anomalie. NON passare alla Fase 6." %
            (len(aperte), len(errori)))
        out("Se non puoi completare: fermati, manda la notifica push e consegna il report parziale "
            "'fermato a Fase 5' elencando per nome queste righe.")
        sys.exit(1)
    nr = [r for r in righe if r["esito"] == "non_raggiungibile"]
    out("COPERTURA COMPLETA: %d/%d righe chiuse (%d non raggiungibili, dichiarate con motivo)." %
        (tot, tot, len(nr)))
    for r in nr:
        out("  non raggiungibile: %s [%s]: %s" % (r["voce"], r["canale"], r["nota"]))
    sys.exit(0)


# ----------------------------------------------------------------------------- main

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Copertura completa della Fase 5 del content-cockpit")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="cartella dei dati (repo privato)")
    ap.add_argument("--watchlist", default=str(DEFAULT_WATCHLIST))
    ap.add_argument("--registro", help="registro specifico (default: l'ultimo in --out)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="costruisce il registro e legge i canali con feed")
    s.add_argument("--dal", help="inizio finestra autori AAAA-MM-GG (default: 7 giorni fa)")
    s.add_argument("--al", help="fine finestra (default: oggi)")
    s.add_argument("--oggi", help="solo per test")
    s.add_argument("--rifai", action="store_true", help="rilegge i feed, conserva le righe chiuse a mano")
    rp = sub.add_parser("riprova", help="a fine Fase 5: rilegge le righe dello script ancora da riprovare")
    rp.add_argument("--dal", required=True, help="inizio finestra autori, lo stesso dello scan")
    rp.add_argument("--al", help="fine finestra (default: la data del registro)")
    g = sub.add_parser("segna", help="chiude una riga del registro")
    g.add_argument("--id", required=True)
    g.add_argument("--esito", required=True, help="contenuti | niente | non_raggiungibile")
    g.add_argument("--n", type=int)
    g.add_argument("--nota", required=True)
    sub.add_parser("verifica", help="exit 0 solo se la copertura e' completa")
    a = ap.parse_args()
    {"scan": cmd_scan, "segna": cmd_segna, "verifica": cmd_verifica, "riprova": cmd_riprova}[a.cmd](a)


if __name__ == "__main__":
    main()
