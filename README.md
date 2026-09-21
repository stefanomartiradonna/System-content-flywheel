# System Content Flywheel

Un sistema di produzione editoriale con memoria persistente, costruito su Claude Code e GitHub.

Produce contenuti per LinkedIn e per la newsletter Substack **"da 0 al PMF"** — senza mai ricominciare da zero.

---

## Il problema che risolve

Chi produce contenuti con AI ha sempre lo stesso problema: ogni sessione parte da zero. Il modello non ricorda cosa hai già pubblicato, non conosce il tuo stile, non sa cosa ha funzionato e cosa no. Il risultato è contenuto generico, inconsistente, che non costruisce nulla nel tempo.

Questo sistema ribalta la logica: la knowledge base cresce a ogni sessione, e il modello la usa come contesto prima di scrivere qualsiasi pezzo.

---

## Architettura

```
System-content-flywheel/
│
├── CLAUDE.md                          # Cervello del sistema — regole, workflow, divisione dei ruoli
│
└── knowledge/
    ├── INDEX.md                       # Router: dice quale dominio caricare per ogni task
    ├── references/                    # Pattern estratti da autori di riferimento analizzati
    │   ├── INDEX.md                   # Lista autori + cross-pattern rilevati
    │   ├── maja-voje/                 # patterns.md + notes.md
    │   ├── pierre-herubel/
    │   ├── alex-estner/
    │   ├── douwe-wester/
    │   └── anthony-pierri/
    ├── craft/
    │   └── writing_techniques.md      # 6 tecniche confermate + false beliefs
    ├── hypotheses/
    │   └── active.md                  # Ipotesi attive da testare con i propri post
    ├── platforms/
    │   ├── linkedin/rules.md          # Regole piattaforma LinkedIn
    │   └── substack/rules.md          # Regole piattaforma Substack
    ├── posts/
    │   ├── INDEX.md
    │   └── published.md               # Registro dei post pubblicati con performance
    └── voice/
        └── archetypes.md              # Registri tonali disponibili
```

---

## Dove vivono gli articoli di riferimento (public/private)

Il sistema copre più rubriche editoriali (in questo repo e in repo gemelli), ognuna con i
propri articoli di esempio. Non tutti gli esempi possono stare nello stesso posto:

| Cosa | Dove | Pubblico o privato |
|---|---|---|
| Tuoi articoli "da 0 al PMF" (incl. Company Teardown) | `System-content-flywheel/articoli/` | Pubblico |
| Tuoi articoli HSBG (Marketing Ignorante) | `marketing-ignorante-brain/articoli/` | Pubblico |
| Esempi di stile Company Teardown (testo di terzi: Michelon, Mastella) | `claude-private-refs/company-teardown/` | **Privato** |
| Esempi di stile HSBG (testo di terzi: Wiles) | `claude-private-refs/how-small-brands-growth/` | **Privato** |

Regola generale, non solo il caso di oggi: il lavoro tuo è pubblico per scelta di
portfolio. Il testo integrale scritto da altri, tenuto come riferimento di stile per una
skill, resta privato — la versione della skill che vive nel repo pubblico (es.
`~/.claude/skills/company-teardown/references/examples/`) cita solo le note di analisi,
mai il testo copiato per intero. Vale per ogni rubrica futura con lo stesso bisogno, non
solo per quelle di oggi.

---

## Come funziona

### 1. Sessione di scrittura

Ogni sessione di lavoro parte dalla lettura di `CLAUDE.md` e `knowledge/INDEX.md`.
Il sistema carica solo il sottoinsieme di knowledge rilevante per il task — non tutto in blocco.

Per scrivere un post LinkedIn:
1. Si invoca la skill `linkedin-viral-post-writer` (regole di stile, hook, struttura)
2. Si aggiunge il contesto da `knowledge/platforms/linkedin/` e `knowledge/references/`
3. Si scrive il pezzo con quella base contestuale

### 2. Learning Mode — come cresce il sistema

**Analisi di un autore di riferimento:**
- Claude Code naviga il profilo LinkedIn via Chrome MCP
- Estrae gli ultimi 10–20 post
- Identifica per ognuno: tipo di hook, struttura del corpo, lunghezza, pattern ricorrenti
- Confronta con quanto già in `knowledge/references/[autore]/`
- Se trova un pattern nuovo → lo aggiunge a `patterns.md`
- Se trova qualcosa che "non dovrebbe funzionare" ma funziona → lo aggiunge a `craft/false_beliefs.md`
- Commit e push automatici su GitHub

**Registrazione di un post pubblicato:**
- Nuova entry in `knowledge/posts/published.md`
- Dati di performance se disponibili (impressions, commenti, reazioni)
- Aggiornamento delle ipotesi attive in base all'evidenza
- Commit e push

### 3. Gestione delle ipotesi

Le ipotesi nascono dall'osservazione dei pattern degli autori e dai propri post.
Quando un'ipotesi si conferma 3+ volte → promossa a regola in `platforms/[platform]/rules.md`.
Quando una regola viene contraddetta da nuova evidenza → retrocessa a ipotesi.

---

## Divisione dei ruoli

| Stefano decide | Claude gestisce |
|----------------|-----------------|
| Cosa pubblicare e cosa no | Ricerca e estrazione pattern |
| Quale prospettiva adottare | Verifica strutturale e confronto con knowledge |
| Opinioni e tesi personali | Angolazioni alternative per un pezzo |
| Cosa eliminare dalla knowledge base | Update automatici dei file knowledge |
| Quali fatti richiedono verifica | Commit e push delle modifiche |

---

## Sync cross-surface

Il repository è condiviso tra tre ambienti:

| Ambiente | Uso principale |
|----------|----------------|
| **Claude Code** (CLI) | Analisi batch, scraping profili, update knowledge, commit |
| **Claude.ai Projects (Cowork)** | Bozze, iterazione, brainstorming da browser |
| **Web / mobile** | Accesso alla knowledge base da qualsiasi dispositivo |

GitHub è il punto di sincronizzazione. Prima di ogni sessione in Cowork o Web: `git pull`. Dopo ogni update della knowledge base: `git push`.

---

## Autori analizzati

| Autore | Perché | Analizzato |
|--------|--------|------------|
| **Maja Voje** | GTM strategy, AI tools, startup early stage | ✅ apr 2026 |
| **Pierre Herubel** | Content strategy B2B, caroselli, pattern hook | ✅ apr 2026 |
| **Alex Estner** | GTM strategy execution, post testuali | ✅ apr 2026 |
| **Douwe Wester** | GTM, dialogo cliente, storie con dettaglio concreto | ✅ apr 2026 |
| **Anthony Pierri** | Positioning B2B, ironia come registro editoriale | ✅ apr 2026 |

Dall'analisi cross-autore sono emersi 6 pattern ad alta evidenza (★) e 2 false beliefs documentate sulle metriche di engagement.

Vengono analizzati i nuovi contenuti degli autori in automatico da un Agente preposto ogni 15gg che sintetizza gli insight più rilevanti, in base ai like e commenti che hanno ricevuto i post di quel periodo e trasformati in argomenti da sviluppare in un doc privato. 
---

## Tecniche di scrittura documentate

Sei tecniche confermate con evidenza empirica da 3+ autori:

- **T01 — Reframe diagnostico**: "Non hai problema X. Hai problema Y."
- **T02 — Dialogo cliente + reazione emotiva**: caso reale, voce del cliente, ribaltamento
- **T03 — Lista già nell'hook**: il primo punto è visibile prima del "leggi di più"
- **T04 — Matematica semplice come proof**: affermazione → calcolo → conclusione in una riga
- **T05 — Chiusura con domanda aperta**: nessuna CTA, solo una domanda che abbassa la barriera al commento
- **T06 — Contrasto temporale**: "2025 era X. 2026 è Y."

---

## Installazione e setup

### Prerequisiti

- [Claude Code](https://claude.ai/code) installato (CLI o estensione VS Code)
- Account Claude con accesso alle Projects feature
- Git configurato localmente

### Clone e apertura

```bash
git clone https://github.com/stefanomartiradonna/System-content-flywheel.git
cd System-content-flywheel
claude  # apre Claude Code nella directory del progetto
```

### Prima sessione

```
leggi CLAUDE.md e knowledge/INDEX.md e dimmi lo stato del sistema
```

### Sessione tipica di scrittura

```
scrivi un post LinkedIn su [tema] — leggi prima CLAUDE.md e knowledge/
```

### Per analizzare un nuovo autore

```
analizza i post di [nome] su LinkedIn e aggiorna la knowledge base
```

---

## Dipendenze e skill esterne

Il sistema usa skill personalizzate di Claude Code che devono essere installate separatamente in `~/.claude/skills/`:

| Skill | Uso |
|-------|-----|
| `linkedin-viral-post-writer` | Post LinkedIn testuali |
| `newsletter-writer` | Articoli Substack long-form |
| `linkedin-carousel-creator` | Caroselli LinkedIn |

Il Learning Mode usa il **Chrome DevTools MCP** per la navigazione automatica dei profili LinkedIn.

---

## Stato del progetto

- **Avviato**: aprile 2026
- **Versione**: 0.1 (MVP operativo)
- **Autori analizzati**: 5
- **Tecniche documentate**: 6 confermate + 6 da testare
- **Post registrati**: in popolamento

Il sistema è un organismo vivo. Cresce con ogni sessione.

---

## Perché questo repository

Costruire questo sistema ha richiesto tre scelte non ovvie:

**1. La knowledge base è separata dalle istruzioni del modello.** `CLAUDE.md` contiene il workflow e le regole operative. `knowledge/` contiene ciò che si è imparato. Non sono la stessa cosa e non vanno mescolate — il primo è stabile, il secondo cresce continuamente.

**2. Il sistema è progettato per essere usato da umani con AI, non sostituire l'umano.** La divisione dei ruoli è esplicita: il modello non decide cosa pubblicare, non sceglie la prospettiva, non esprime opinioni. Gestisce la knowledge e la struttura. Questo è intenzionale — un sistema che sostituisce il giudizio editoriale non scala nel lungo periodo.

**3. Le ipotesi sono cittadine di prima classe.** Non è sufficiente raccogliere pattern — bisogna sapere quanto ci si fida di ciascuno. Il sistema distingue tra "osservato su 1 autore", "osservato su 3+ autori" e "confermato sui propri post". Questa gerarchia di evidenza cambia come si usa ogni tecnica.

---

## Autore

**Stefano Martiradonna** — Product Marketing Fractional
Newsletter: [da 0 al PMF](https://daozeroalpmf.substack.com) su Substack
LinkedIn: [linkedin.com/in/stefanomartiradonna](https://linkedin.com/in/stefanomartiradonna)
