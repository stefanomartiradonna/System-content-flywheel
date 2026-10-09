# launch-content-cockpit.ps1
# Avvia il Content Cockpit, il report settimanale del lunedì, in modalità supervisionata.
# Chiamato dallo scheduled task Windows "Content Cockpit" (lunedì, 08:40),
# oppure lanciabile a mano quando vuoi far partire un ciclo.
#
# Modalità: launcher supervisionato, come il Content Radar. Apre Claude Code interattivo nel repo
# e avvia la skill content-cockpit. Usa il TUO Chrome (già loggato su LinkedIn) per leggere le
# impressioni dei post, che sono visibili solo al proprietario.
# Tu supervisioni e approvi i prompt (scrittura file, commit).
#
# Il workflow NON sta qui dentro: sta in ~/.claude/skills/content-cockpit/SKILL.md
# Per cambiare cosa fa il report, modifica la skill, non questo file.

$RepoPath = 'C:\Users\Utente\Documents\System-content-flywheel'

Set-Location -Path $RepoPath

Write-Host ''
Write-Host '=== CONTENT COCKPIT — report settimanale del lunedi (supervisionato) ===' -ForegroundColor Cyan
Write-Host ''
Write-Host 'PRIMA DI PROCEDERE:' -ForegroundColor Yellow
Write-Host '  1. Chrome APERTO e LOGGATO su LinkedIn (senza login non si vedono le impressioni)' -ForegroundColor Yellow
Write-Host '  2. Connector PostHog autorizzato su claude.ai' -ForegroundColor Yellow
Write-Host ''

$Prompt = @'
Esegui la skill content-cockpit in questa directory (System-content-flywheel). E' il run settimanale
del lunedi.

PRIMA DI TUTTO: carica la skill content-cockpit e confermami in una riga che l'hai letta, citando il
titolo della Fase 9. Se non riesci a caricarla, FERMATI e dimmelo invece di improvvisare: il workflow
vive li dentro, e senza quel file le fasi elencate qui sotto non esistono da nessuna parte.

Le 11 fasi, solo come indice per sapere cosa aspettarsi. Le istruzioni vere stanno nella skill e
vincono su questo elenco:

  Fase 0  Contesto: git pull, legge foundation/, hypotheses, craft, voce-analisi, temi.csv
  Fase 1  Aggiorna il dataset: snapshot LinkedIn da Chrome, rilancia parse_snapshot.py
  Fase 2  KPI dei post sulla finestra matura, migliore della settimana, trend, anti-rumore
  Fase 3  PostHog: visite al sito e click sulle CTA (attenzione al project, punto 1 sotto)
  Fase 4  Conversioni manuali: legge conversions.md (i DM, che nessun sistema vede)
  Fase 5  Radar autori di riferimento: lancia la skill content-radar se sono passati 12+ giorni
          dall'ultima riga di radar/log.md, altrimenti riusa gli angle non ancora sfruttati
  Fase 6  Temi della settimana da tre fonti: la mia settimana, il mercato, l'archivio
  Fase 7  Piano di 5 pezzi -> QUI TI FERMI E ASPETTI
  Fase 8  Scrive solo i pezzi che ho scelto, con brief immagine e link UTM
  Fase 9  Auto-miglioramento: impara dalle mie correzioni e verifica le previsioni vecchie
  Fase 10 Output: scrive il report in claude-private-refs/linkedin/cockpit/ e committa

Fermati alla Fase 7 e aspetta. Proponi il piano dei 5 pezzi e NON scrivere i post finche non ti dico
quali tengo. Scrivere cinque pezzi per pubblicarne due butta via il lavoro e mi toglie il gate
editoriale.

I cinque punti dove si sbaglia piu facilmente:

1. PostHog: il project di default e 415565 ed e il sito di un CLIENTE (un cardiologo). Il mio e
   413969, organizzazione "Mio Sito". Fai switch-organization e switch-project, poi verifica con una
   query su properties.$host che il dominio sia stefanomartiradonna.com PRIMA di riportare qualsiasi
   numero. Se non lo e, fermati e dimmelo.

2. Misura la finestra MATURA (post pubblicati tra 14 e 8 giorni fa), non quella fresca. Le impressioni
   crescono per circa una settimana: misurare i post di ieri premia chi ha pubblicato lunedi scorso
   per un artefatto di misurazione, non per merito.

3. Controllo anti-rumore obbligatorio: per ogni confronto tra gruppi, somma reazioni + commenti del
   gruppo. Sotto 30, dichiara la differenza non leggibile a meno che non superi il 50%. Scrivilo nel
   report. La mediana e 275 impressioni: la maggior parte delle oscillazioni e rumore.

4. Precedenza tra le fonti: la skill linkedin-viral-post-writer e l'autorita sulla voce (e mia, la uso
   anche fuori da questa routine). voce-analisi.md e evidenza su cosa faccio di fatto, informa ma non
   comanda. Le regole generiche di copywriting perdono sempre. Se la skill e i dati divergono, NON
   decidere: mettilo nel report e lascia che scelga io.

5. Se Chrome non risponde o un connector e giu, dichiaralo in cima al report e lavora sui dati
   esistenti segnando cosa e fermo alla settimana scorsa. Non inventare numeri e non fingere che il
   dato sia fresco.

Non pubblicare NULLA: ne post, ne commenti, ne modifiche al sito. L'output sono bozze che edito io.

Prima della Fase 1 verifica che Chrome sia aperto e loggato su LinkedIn; se non lo e, avvisami e
chiedi come procedere.
'@

# Avvia Claude Code interattivo con il prompt del cockpit.
& claude $Prompt
