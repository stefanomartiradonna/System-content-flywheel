# La routine del lunedì: dove vive e come si installa

Ogni lunedì alle 8:00 Claude prepara il report sui contenuti: misura i post LinkedIn della settimana
matura, legge sito e conversioni, e chiude con due liste tra cui scegliere, 5 notizie tech da leggere
con i propri pillar e 5 angoli dagli autori di riferimento. Poi si ferma e aspetta la scelta.

Questa pagina serve a una cosa: rimettere in piedi la routine, identica, su un computer nuovo
partendo solo da GitHub.

---

## Dove vive ogni pezzo

| Pezzo | Dove | Visibilità |
|---|---|---|
| Cosa fa la routine, fase per fase | repo `claude-brain`, `skills/content-cockpit/SKILL.md` | pubblico |
| Le altre skill che usa (`content-radar`, `linkedin-viral-post-writer`) | repo `claude-brain`, `skills/` | pubblico |
| Il prompt con cui parte | questo repo, `scripts/prompt-content-cockpit.md` | pubblico |
| Installer e lancio a mano | questo repo, `scripts/` | pubblico |
| Knowledge, ipotesi, log del radar | questo repo, `knowledge/` e `radar/` | pubblico |
| Numeri dei post, testi, report, bozze, frasi dalle call | repo `claude-private-refs` | **privato** |
| Quando parte (lunedì alle 8:00) | task pianificato dentro l'app Claude | solo sul computer |
| Accessi: Claude, GitHub, LinkedIn, connettori | account e browser | mai su GitHub |

Regola: su GitHub pubblico sta come è organizzata la routine, senza nomi di clienti, di persone o
loro identificativi. Tutto quello che ha una provenienza delicata sta nel repo privato.

---

## Installarla su un computer nuovo

**1. Installa i programmi.** Git, Python 3, Node.js, Google Chrome e l'app Claude. Fai l'accesso a
Claude e a GitHub (il repo dei dati è privato, senza accesso non si scarica).

**2. Scarica questo repo e lancia l'installer.**

```powershell
git clone https://github.com/stefanomartiradonna/System-content-flywheel.git
cd System-content-flywheel
powershell -ExecutionPolicy Bypass -File scripts\install-content-cockpit.ps1
```

L'installer scarica gli altri due repo (le skill nella cartella di Claude, i dati accanto a questo
repo), installa il collegamento a Chrome e controlla che ogni pezzo sia al suo posto. Non cancella
niente e si può rilanciare quante volte serve. Se la cartella di Claude esiste già, i file che
verrebbero sovrascritti finiscono in una cartella di backup accanto.

**3. Fai a mano le tre cose che uno script non può fare.**
- Su claude.ai controlla i connettori: PostHog, Granola, Gmail, Calendar, Drive. Sono legati
  all'account, di norma li ritrovi già collegati.
- In Chrome fai l'accesso a LinkedIn. Le impressioni dei post le vede solo il proprietario.
- Sempre in Chrome, attiva una volta il debug remoto: `chrome://inspect/#remote-debugging`.

**4. Crea il task pianificato.** Apri Claude in questa cartella e scrivi:

> Installa il task pianificato del lunedì seguendo scripts/README.md

**5. Controlla.** Rilancia l'installer in sola lettura. Deve finire con "TUTTO A POSTO".

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install-content-cockpit.ps1 -SoloControllo
```

La prima volta conviene far partire il task a mano dall'app ("Run now") e approvare gli strumenti
che chiede: così i lunedì successivi non si ferma in attesa di un permesso.

---

## Per Claude: creare o aggiornare il task pianificato

1. Leggi `scripts/prompt-content-cockpit.md`.
2. Sostituisci `{{FLYWHEEL}}` con il percorso assoluto di questo repo e `{{PRIVATO}}` con quello di
   `claude-private-refs`, che sta nella stessa cartella madre. Verifica che entrambe le cartelle
   esistano prima di procedere.
3. Elenca i task pianificati. Se `content-linkedin` esiste, aggiornane solo il prompt. Se non esiste,
   crealo così:
   - taskId: `content-linkedin`
   - titolo: `Content Linkedin`
   - cronExpression: `0 8 * * 1` (lunedì alle 8:00, ora locale)
   - descrizione: report settimanale sui contenuti LinkedIn, con le due liste finali tra cui scegliere
   - prompt: il testo del punto 2, senza altre modifiche
4. Rilancia l'installer con `-SoloControllo` e riporta l'esito del punto 5, "Task pianificato".

---

## Tenerla aggiornata

- **Cambiare cosa fa la routine**: si modifica la skill in `claude-brain`. Vale subito su ogni
  computer dopo un `git pull`.
- **Cambiare il prompt di partenza**: si modifica solo `scripts/prompt-content-cockpit.md`, poi si
  ripete il passo 4. L'installer avvisa quando il task e il file non coincidono più.
- **I dati**: a fine giro la routine committa e pusha il repo privato. È quella copia che permette
  di ripartire da un altro computer senza perdere lo storico.
- **Lancio fuori orario**: `scripts\launch-content-cockpit.ps1`, usa lo stesso prompt.

## Cosa non copre

- Il radar degli autori ha anche un suo avvio separato (un'attività pianificata di Windows che
  lancia `launch-content-radar.ps1`). L'installer non la crea: la routine del lunedì lancia già il
  radar da sola quando sono passati 12 giorni dall'ultimo ciclo.
- Chiavi e token non stanno su GitHub, in nessuno dei tre repo. I collegamenti che ne hanno bisogno
  vanno riconfigurati a mano.
