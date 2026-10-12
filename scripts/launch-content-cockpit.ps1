# launch-content-cockpit.ps1
# Avvia a mano il Content Cockpit, il report settimanale del lunedi.
#
# La pianificazione automatica NON passa da qui: e' un task pianificato dell'app Claude
# ("content-linkedin", lunedi alle 8:00). Questo script serve quando vuoi far partire un giro
# fuori orario, da terminale.
#
# Il prompt sta in scripts/prompt-content-cockpit.md ed e' lo stesso che usa il task pianificato.
# Il workflow sta nella skill: ~/.claude/skills/content-cockpit/SKILL.md
# Per cambiare cosa fa il report modifica la skill. Per cambiare il prompt modifica il file .md.
#
# Nessun percorso e' scritto a mano: le cartelle si ricavano da dove si trova questo script.
# Il repo privato deve stare accanto a questo, nella stessa cartella madre.

$RepoPath    = Split-Path -Parent $PSScriptRoot
$PrivatePath = Join-Path (Split-Path -Parent $RepoPath) 'claude-private-refs'
$PromptFile  = Join-Path $PSScriptRoot 'prompt-content-cockpit.md'

if (-not (Test-Path $PromptFile)) {
    Write-Host "Manca $PromptFile" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path (Join-Path $PrivatePath 'linkedin'))) {
    Write-Host "Non trovo il repo privato in $PrivatePath" -ForegroundColor Red
    Write-Host 'Lancia prima scripts\install-content-cockpit.ps1' -ForegroundColor Yellow
    exit 1
}

Set-Location -Path $RepoPath

Write-Host ''
Write-Host '=== CONTENT COCKPIT: report settimanale del lunedi ===' -ForegroundColor Cyan
Write-Host ''
Write-Host 'PRIMA DI PROCEDERE:' -ForegroundColor Yellow
Write-Host '  1. Chrome APERTO e LOGGATO su LinkedIn (senza login non si vedono le impressioni)' -ForegroundColor Yellow
Write-Host '  2. Connector PostHog autorizzato su claude.ai' -ForegroundColor Yellow
Write-Host ''

$Prompt = (Get-Content -Path $PromptFile -Raw -Encoding UTF8).Replace('{{FLYWHEEL}}', $RepoPath).Replace('{{PRIVATO}}', $PrivatePath)

# Avvia Claude Code interattivo con il prompt del cockpit.
& claude $Prompt
