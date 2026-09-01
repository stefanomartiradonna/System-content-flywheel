# Content Flywheel — Cervello del Sistema

Questo file è il punto di ingresso per tutte le sessioni di lavoro editoriale.
Leggilo integralmente prima di qualsiasi task.

---

## Chi sono e cosa faccio

Sono Stefano Martiradonna. Product Marketing Fractional e consulente.
Lavoro con startup tech B2B in growth (segmento principale del contenuto), startup early-stage, e PMI.

Pubblico su due canali, con ruoli distinti (hub & spoke):
- **Substack "da 0 al PMF"** (hub) — il metodo per intero: articoli long-form su positioning, product marketing, GTM. Dove chi vuole approfondisce.
- **LinkedIn** (distribuzione) — gli articoli si spacchettano in post + infografiche/grafiche impattanti. Obiettivi: nuovi lead, attenzione, restare nella testa di chi mi conosce ma non ha ancora esigenza dei miei servizi.

Concept editoriale corrente: **"Accumulo"** (2026-07) — vedi `knowledge/foundation/` (POV-master: "il tuo problema non è il copy, è una decisione di prodotto mai presa").

---

## Il Sistema

### Come funziona

Il sistema accumula conoscenza ogni volta che lavoro. Non parte da zero.

1. `CLAUDE.md` → regole, voce, workflow (questo file)
2. `knowledge/INDEX.md` → router: leggi sempre quello prima di drill-down
3. Ogni sottocartella è un dominio separato — carica solo quello che serve al task

### Divisione dei ruoli

**Stefano decide:**
- Cosa pubblicare e cosa non pubblicare
- Quale prospettiva adottare su un tema
- Opinioni, credenze, tesi personali
- Cosa eliminare dalla knowledge base
- Quali fatti necessitano doppia verifica

**Claude gestisce:**
- Ricerca e estrazione pattern
- Verifica strutturale e confronto con knowledge
- Opzioni di angolazione per un pezzo
- Update automatici dei file di conoscenza (vedi Learning Mode)
- Commit e push delle modifiche ai file knowledge (nessuna autorizzazione necessaria per i file in `knowledge/`)

---

## Skills da invocare

Quando lavoro su contenuti editoriali, usa sempre le skill dedicate come base.
La knowledge del sistema si aggiunge sopra, non sostituisce.

**Context scoping (regola):** carica SOLO i file elencati per il task, non tutta la knowledge.
La `foundation/` è la sostanza (leggila sempre prima di scrivere); il resto è forma e si aggiunge mirato.
Caricare tutto porta a context pollution — l'AI infila riferimenti che il pezzo non autorizza.

| Task | Skill da invocare | Knowledge aggiuntiva da leggere |
|------|-------------------|---------------------------------|
| Scrivi post LinkedIn | `linkedin-viral-post-writer` | `knowledge/foundation/voice-guide.md` + `pov.md` + `audience.md` + `content-strategy.md` (tipo di contenuto + trigger) + `knowledge/client-intelligence/` + `knowledge/references/` |
| Scrivi articolo Substack | `newsletter-writer` | `knowledge/foundation/` (positioning, pov, voice, content-strategy) + `metodo-catena.md` (se articolo di metodo) + `knowledge/client-intelligence/` + `knowledge/proof-library/` + `knowledge/platforms/substack/` |
| Crea carosello LinkedIn | `linkedin-carousel-creator` | `knowledge/foundation/voice-guide.md` + `pov.md` + `content-strategy.md` |
| Crea infografica di metodo | `infographic-creator` | `knowledge/foundation/metodo-catena.md` + `pov.md` |
| Analizza autore di riferimento | nessuna skill, usa Chrome MCP | `knowledge/references/` |
| Feedback su un mio pezzo | `newsletter-writer` Modalità 3 | `knowledge/foundation/pov.md` + `knowledge/posts/` + `knowledge/hypotheses/active.md` |
| Estrai insight da un engagement | nessuna skill (workflow in INDEX) | `knowledge/client-intelligence/INDEX.md` |
| Scrivi Company Teardown | `company-teardown` | `knowledge/companies/` (se esiste) |
| Radar bisettimanale contenuti (autori + temi) | `content-radar` | `knowledge/foundation/pov.md` + `content-strategy.md` + `audience.md` + `knowledge/hypotheses/active.md` — output: Google Doc + riga in `radar/log.md` |

Questo repo è **solo "da 0 al PMF"**. Marketing Ignorante (testata MarkeThings) ha il suo repo,
`marketing-ignorante-brain`, con la sua voce e la sua skill: fino a settembre 2026 viveva qui
dentro e la convivenza richiedeva di ricordarsi ogni volta di non mescolare le due voci.

Le skill stanno in `~/.claude/skills/`.

---

## Convenzione di output — dove salvare i deliverable

Ogni deliverable va salvato nella cartella dedicata al suo tipo. Non mischiarli nella root.

| Tipo di output | Cartella di destinazione | Estensioni tipiche |
|----------------|--------------------------|---------------------|
| Caroselli LinkedIn | `caroselli/` | `.pptx`, `.pdf` |
| Infografiche | `infografiche/` | `.html`, `.jsx`, `.png`, `.pdf` |
| Post LinkedIn (idee, bozze, varianti) | `post-idee/` | `.md` |
| Post LinkedIn (già pubblicati) | `post-pubblicati/` | `.md` |
| Articoli Substack (bozze) | `articoli/` (crea se manca) | `.md` |
| Company Teardown (rubrica newsletter) | `articoli/` | `.md` |
| Content Radar (report bisettimanale) | Google Doc + log in `radar/log.md` | Doc, `.md` |

**Workflow post LinkedIn:**
1. Nascita di un'idea → file in `post-idee/` (anche solo un titolo o un hook)
2. Iterazione, draft, hook, varianti → stesso file o sottocartella in `post-idee/[topic]/`
3. Quando pubblicato su LinkedIn → spostare il file in `post-pubblicati/` e (opzionale) registrare performance in `knowledge/posts/published.md`

Convenzione nome file: `[Topic-Principale]-[Angle-o-Data].ext`
Esempio: `Carosello-Moltiplicatori-GTM.pdf`, `Post-ICP-vs-ECP-2026-04.md`

Se il deliverable è multi-file (es. carosello = .pptx + .pdf), tienili insieme nella stessa cartella. Se è una serie di output correlati, crea una sottocartella dedicata.

---

## Learning Mode — Istruzioni per l'aggiornamento automatico

Quando mi chiedi di analizzare post di un autore di riferimento:

1. Naviga il profilo LinkedIn con Chrome MCP
2. Per ogni post estratto, identifica:
   - Hook: tipo, struttura, caratteri prima del "leggi di più"
   - Struttura del corpo: lista / narrative / framework / dati
   - Lunghezza approssimativa
   - Eventuali segnali di engagement (commenti, reaction) se visibili
3. Confronta con pattern già in `knowledge/references/[autore]/`
4. Se trovi un pattern nuovo → aggiungilo a `references/[autore]/patterns.md`
5. Se qualcosa "non dovrebbe funzionare" ma funziona → aggiungilo a `knowledge/craft/false_beliefs.md`
6. Se trovi evidenza per o contro un'ipotesi attiva → aggiorna `knowledge/hypotheses/active.md`
7. Commit e push (branch main) — messaggio: `chore: update knowledge — [autore]`

Quando pubblico un pezzo e mi chiedi di registrarlo:

1. Aggiungi entry in `knowledge/posts/published.md`
2. Se ci sono dati di performance (impressions, commenti, reazioni) aggiungili nel file
3. Identifica: cosa ha funzionato, quale pattern era nel pezzo
4. Aggiorna `knowledge/hypotheses/active.md` con l'evidenza
5. Commit e push — messaggio: `chore: add post — [titolo breve]`

Quando ti do gli appunti di un engagement e dico "estrai gli insight":

1. **Anonimizza all'ingresso**: rimuovi nome persona e brand; tieni ruolo, settore, scala. (**Repo pubblico: l'anonimizzazione è obbligatoria, non opzionale.**)
2. Crea/aggiorna l'entry in `knowledge/client-intelligence/insights/[slug].md` col template in `client-intelligence/INDEX.md`
3. Proponi 0-N voci per `knowledge/client-intelligence/lexicon.md` (founder-speak vs vendor-speak)
4. Se conferma/contraddice un pattern → aggiorna `client-intelligence/patterns.md`; se tocca un'ipotesi → `hypotheses/active.md` (evidenza ora da fonte MIA, non dagli autori)
5. Se c'è un risultato misurabile → riga in `knowledge/proof-library/results.md`
6. Commit e push — messaggio: `chore: add client intelligence — [slug anonimo]`

Quando edito una bozza e dico "registra i miei edit":

1. Calcola il diff git tra versione generata e versione editata
2. Estrai i pattern di correzione ricorrenti → `knowledge/craft/edit-patterns.md`
3. Se un pattern di edit si ripete 3+ volte → promuovilo a `foundation/voice-guide.md` (voce) o `craft/writing_techniques.md` (craft)

**Principi di sistema:**
- **Intelligence → multiple outputs**: una sola estrazione da engagement alimenta articolo + post + carosello E affina il positioning a monte (`foundation/`). Non è un problema di produzione, è distribuzione di intelligence. La review che promuove i pattern in `foundation/` si fa ogni 3-6 mesi: l'evidenza fa emergere, Stefano decide.
- **Human gate all'outline**: per gli articoli Substack, la revisione umana sta al livello strategico (outline/angle), non al copy-editing. Approvato l'outline, il writer scrive senza re-improvvisare la sostanza.

**Content Radar (regola):** il radar bisettimanale (`content-radar`, ogni ~15 giorni o manuale)
produce report e PROPONE candidati per la knowledge (sezione "Segnali per la knowledge" nel Doc),
ma **non modifica mai** `references/`, `hypotheses/` o `foundation/` in automatico — la promozione
la decide Stefano. Il radar committa solo `radar/log.md`.

**Non chiedere autorizzazione per aggiornare i file `knowledge/`.
Chiedi solo se devi modificare questo CLAUDE.md o i file nelle cartelle `platforms/`.**

---

## Voce e stile

Vedi skill `linkedin-viral-post-writer` → `references/mio-stile.md` per le regole complete.

Principi non negoziabili:
- Diretto, mai pomposo, mai da guru
- Specifico per early stage B2B SaaS — mai generico
- Ogni concetto ha bisogno di un esempio concreto (azienda, numero, caso)
- Mai: mindset, hustle, game changer, life-changing
- Italiano di default, mix naturale con termini tecnici inglesi

---

## Sync cross-surface

Questo repo è condiviso tra Claude Code, Cowork, e Web (via GitHub).

**Il repo è PUBBLICO su GitHub.** È una scelta: fa parte del portfolio. Tutto ciò che committi
qui è leggibile da chiunque. Vedi la "Regola di pubblicazione" nel CLAUDE.md globale per cosa
non deve mai entrare (candidature, materiale cliente non anonimizzato, importi, bozze da non
anticipare).

- **Claude Code**: analisi batch, script, update knowledge, commit
- **Cowork**: bozze, iterazione, brainstorming
- **Web/mobile**: accesso da qualsiasi dispositivo, stessa knowledge base

Regola: fai sempre `git pull` prima di iniziare una sessione se stai usando Cowork o Web.
Fai sempre `git push` dopo aver aggiornato la knowledge base.
