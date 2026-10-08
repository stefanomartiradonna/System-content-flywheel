# Posts — Archivio Pubblicazioni

Questo dominio traccia tutto ciò che hai pubblicato.
Serve per: non ripetere temi già trattati, misurare cosa funziona, alimentare le hypotheses.

---

## File disponibili

| File | Contenuto |
|------|-----------|
| `published.md` | Analisi qualitativa approfondita dei singoli pezzi. Non ci vanno tutti i post: solo quelli che valgono uno smontaggio (outlier positivi e negativi) |
| `visual-assets.md` | Asset visivi associati ai pezzi |

### Il dataset quantitativo sta altrove (repo privato)

I numeri di performance di tutti i post LinkedIn **non stanno in questo repo**, che è pubblico.
Stanno in `claude-private-refs/linkedin/` (repo privato su GitHub, si clona come gli altri):

| File | Contenuto |
|---|---|
| `linkedin/metrics.csv` | Una riga per post: data, formato, caratteri, impressions, reactions, commenti, engagement rate, hook |
| `linkedin/posts-full.md` | Testo integrale di ogni post |
| `linkedin/parse_snapshot.py` | Script che rigenera i due file sopra da uno snapshot della pagina "recent activity" |

**Perché privato:** le impressioni dei post sono dati di performance che su un repo pubblico
sarebbero leggibili da chiunque, clienti e prospect inclusi. Il repo è comunque su GitHub,
quindi cambiando computer si recupera tutto con un clone.

### Divisione del lavoro

`metrics.csv` (privato) risponde a "cosa funziona" su volume: serve massa per vedere un pattern.
`published.md` (qui) risponde a "perché ha funzionato" su pochi casi: serve profondità.
Il testo dei post pubblicati come asset editoriale sta in `post-pubblicati/`.

### Come aggiornare il dataset

Si rigenera, non si compila a mano: si apre la pagina recent-activity di LinkedIn da loggati
(le impressioni sono visibili solo al proprietario), si prende uno snapshot della pagina e si
rilancia `parse_snapshot.py`.

---

## Come registrare un nuovo pezzo pubblicato

Dopo ogni pubblicazione, dimmi: "registra questo post: [titolo o testo]"
Claude aggiunge l'entry in `published.md` e aggiorna `hypotheses/active.md` se c'è evidenza rilevante.

---

## Metriche da raccogliere

**LinkedIn post:**
- Impressioni (se disponibili)
- Reazioni
- Commenti
- Click (se link presente)

**Substack articoli:**
- Open rate
- Click rate
- Nuovi iscritti generati

Non ossessionarti con i numeri subito. Parti dal tracciare titolo, data, tema, tipo di post.
I numeri si aggiungono quando li hai.
