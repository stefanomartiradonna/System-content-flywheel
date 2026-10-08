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
del lunedi: segui il workflow completo dalla Fase 0 alla Fase 9.

Promemoria dei punti dove si sbaglia piu facilmente:
- PostHog: il project di default e 415565 ed e il sito di un CLIENTE. Il tuo e 413969, organizzazione
  "Mio Sito". Fai switch-organization e switch-project, poi verifica con una query che il dominio sia
  stefanomartiradonna.com prima di riportare qualsiasi numero.
- Misura la finestra MATURA (post di 8-14 giorni fa), non quella fresca.
- Applica il controllo anti-rumore: sotto 30 eventi di engagement per gruppo, le differenze sotto il
  50% non sono leggibili e vanno dichiarate tali.
- Se Chrome non risponde, dichiaralo e lavora sui dati esistenti. Non inventare numeri.
- Non pubblicare NULLA. Solo bozze.

Prima di iniziare la Fase 1 verifica che Chrome sia aperto e loggato su LinkedIn; se non lo e,
avvisami e chiedi come procedere.
'@

# Avvia Claude Code interattivo con il prompt del cockpit.
& claude $Prompt
