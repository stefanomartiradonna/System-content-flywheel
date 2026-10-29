# References — Autori di Riferimento

Questo dominio raccoglie i pattern estratti dagli autori che studi.
Ogni autore ha la sua cartella. Questo file è il router.

---

## Autori da analizzare (lista priorità)

Aggiungi qui gli autori che vuoi studiare, con note sul perché ti interessano.

| Autore | Profilo LinkedIn | Perché lo studi | Analizzato | Radar settimanale |
|--------|-----------------|-----------------|------------|-------------------|
| Maja Voje | linkedin.com/in/majavoje | GTM strategy, AI tools, startup early stage — segmento simile al mio | Sì (apr 2026) | ✓ |
| Pierre Herubel | linkedin.com/in/pierre-herubel-540b3949 | Content strategy B2B, caroselli — già in carousel skill, qui post testuali | Sì (apr 2026) | ✓ |
| Alex Estner | linkedin.com/in/alexander-estner | GTM strategy execution — nessun dato esistente | Sì (apr 2026) | ✓ |
| Douwe Wester | linkedin.com/in/douwewester | GTM, post testuali — placeholder nel carousel skill | Sì (apr 2026) | ✓ |
| Anthony Pierri | linkedin.com/in/anthonypierri | Positioning B2B + homepage — già in saas-homepage-analyzer skill, qui pattern LinkedIn | Sì (apr 2026) | ✓ |
| April Dunford | linkedin.com/in/aprildunford | Positioning B2B, architetture multi-product — fonte primaria del metodo (pillar architetture) | No — solo radar | ✓ |
| Rob Kaminski | linkedin.com/in/heyrobk | Positioning & messaging B2B (Fletch) — fonte framework H1/homepage, contenuti visual | No — solo radar | ✓ |

**Radar settimanale** = letto ogni lunedì dalla skill `content-cockpit` (Fase 5, report su Google Doc).
La watchlist operativa sta in `~/.claude/skills/content-cockpit/references/watchlist.md`. I cicli fino al
25/10/2026, quando il radar era una skill separata, sono in `radar/log.md`.

---

## Come analizzare un autore

1. Dimmi: "analizza i post di [nome] su LinkedIn"
2. Navigo il profilo con Chrome MCP
3. Estraggo gli ultimi 10-20 post
4. Creo `references/[nome-cognome]/patterns.md` con i pattern trovati
5. Aggiorno questo INDEX con la riga dell'autore

---

## Struttura cartella per ogni autore

```
references/
└── nome-cognome/
    ├── patterns.md     ← hook, strutture, lunghezze, format ricorrenti
    └── notes.md        ← osservazioni libere, cosa mi colpisce, perché funziona
```

---

## Pattern cross-autore

Aggiornato: aprile 2026. Basato su analisi di tutti e 5 gli autori.
Quando lo stesso pattern appare in 3+ autori → segnale forte (evidenziato con ★).

---

### ★ Reframe diagnostico — "Non hai problema X, hai problema Y"
**Presente in**: Estner (pattern dominante), Wester (top performer), Herubel (variante con parentesi)
**Formula**: riga 1 afferma la falsa diagnosi comune → riga 2 ribalta
**Adattabilità**: alta — non dipende dalla lingua, non richiede credenziali specifiche

---

### ★ Dialogo founder / cliente con punto di svolta
**Presente in**: Herubel (firma distintiva, dialogo neutro), Wester (dialogo con reazione emotiva), Estner (variante con quote dirette)
**Formula**: voce del cliente → risposta/reazione del consulente
**Differenza chiave**: Wester aggiunge la reazione emotiva ("??!!") — più autentico e immediato
**Adattabilità**: alta — ho materiale reale dalla consulenza

---

### ★ Chiusura con domanda aperta di engagement
**Presente in**: Maja Voje, Herubel, Wester, Estner
**Formula**: ultima riga del post = domanda aperta al lettore ("What's your take?", "What's missing?")
**Nota**: nessuno dei 4 chiude con CTA diretta come standard — è sempre domanda o frase manifesto
**Adattabilità**: immediata — da adottare sistematicamente

---

### ★ Lista già visibile nell'hook (primo punto esposto prima del "leggi di più")
**Presente in**: Herubel (sistematico), Maja Voje (frequente), Estner (frequente)
**Formula**: "These 5 principles: 1. [primo punto già scritto per intero]..."
**Effetto**: il lettore vede il valore del contenuto prima di cliccare
**Adattabilità**: alta

---

### Matematica semplice come proof (senza lista, senza framework)
**Presente in**: Estner (top post non-giveaway), Wester (post ICP+ACV)
**Formula**: affermazione → calcolo semplice → "stessa cosa, difficoltà completamente diversa"
**Nota**: solo 2 autori, ma entrambi con top performance — vale come segnale
**Adattabilità**: alta — ho numeri reali (CAC, ARR, mercato italiano)

---

### Storia personale breve + quote shock o milestone
**Presente in**: Herubel ("9 years + domanda assurda"), Wester ("content sucked 2 years", "2006→2026 newsletter"), Maja Voje (achievement + sistema)
**Formula**: credenziale temporale o milestone → aneddoto specifico che sorprende
**Adattabilità**: media — richiede aneddoti reali da consulenza, che ho

---

### Contrasto temporale / "era statement"
**Presente in**: Maja Voje ("2025 was the year of Prompt. 2026 is the year of Context."), Herubel ("B2B playbook changed in 3 years"), Estner ("In 2026...")
**Formula**: prima / dopo, o "X era Y. Ora è Z."
**Adattabilità**: alta — funziona su qualsiasi tema che ha avuto un'evoluzione recente

---

### ★ Credenziale quantitativa + errore sistematico
**Presente in**: Pierri ("500 homepages / 500 positioning projects"), Estner ("30+ founders"), Herubel ("9 years a marketer"), Wester ("30+ GTM Assessment Sprints")
**Formula**: "[numero alto] di [progetti/anni/clienti]. [Percentuale o affermazione] sbaglia/non capisce [cosa]."
**Top performer**: "I've written almost 500 homepages. Let me tell you..." → 959 reactions (Pierri)
**Adattabilità**: alta — ho anni di consulenza e decine di aziende. Da quantificare.

---

### Sarcasmo/ironia come registro editoriale stabile
**Presente in**: Pierri (sistematico, ~30% del feed), Wester (episodico), Maja Voje (metafora paradossale)
**Nota**: il sarcasmo puro sull'AI hype è quasi esclusivo di Pierri. Wester lo usa più come tono che come struttura
**Condizione**: funziona solo con audience che ti conosce e capisce il registro. Non per i primi post
**Adattabilità**: media — da introdurre gradualmente dopo aver costruito credibilità

---

## Cosa NON è cross-autore (specifico di 1 solo)

- **Giveaway "commenta per ricevere"**: diffuso tra Estner e Wester — tattica, non pattern editoriale
- **Sarcasmo esteso** (post interamente satirici): quasi esclusivo Pierri
- **"Zodiac / paradosso assurdo"**: solo Wester
- **Caroselli con cover testuale forte**: solo Herubel — già in linkedin-carousel-creator/references/
- **Domanda filosofica binaria** ("What comes first: X or Y?"): solo Pierri — genera alto ratio commenti/reactions
