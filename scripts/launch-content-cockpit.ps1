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
del lunedi: segui il workflow completo dalla Fase 0 alla Fase 10.

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
