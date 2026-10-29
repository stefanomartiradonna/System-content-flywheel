# install-content-cockpit.ps1
# Installa (o controlla) la routine del lunedi su questo computer.
#
# Uso, da dentro il repo System-content-flywheel:
#     powershell -ExecutionPolicy Bypass -File scripts\install-content-cockpit.ps1
#
# Solo controllo, senza toccare niente:
#     powershell -ExecutionPolicy Bypass -File scripts\install-content-cockpit.ps1 -SoloControllo
#
# Cosa fa:
#   1. controlla i programmi che servono (git, Python, Node, Claude Code, Chrome)
#   2. scarica o aggiorna i tre repo: questo, claude-brain (le skill) e claude-private-refs (i dati)
#   3. installa e registra il collegamento a Chrome (chrome-devtools-mcp)
#   4. verifica che ci siano skill, dati e script
#   5. dice se il task pianificato del lunedi esiste ed e' allineato al prompt del repo
#
# Cosa NON puo' fare uno script, e resta a mano (lo ricorda alla fine):
#   login a Claude, connettori su claude.ai, login a LinkedIn in Chrome, creazione del task
#   pianificato dentro l'app Claude.
#
# Si puo' rilanciare quante volte vuoi: non cancella niente.

param(
    [string]$ClaudeHome = (Join-Path $HOME '.claude'),
    [string]$CartellaPrivata = '',
    [string]$UtenteGitHub = 'stefanomartiradonna',
    [switch]$SoloControllo
)

$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Flywheel = Split-Path -Parent $PSScriptRoot
$Base     = Split-Path -Parent $Flywheel
if (-not $CartellaPrivata) { $CartellaPrivata = Join-Path $Base 'claude-private-refs' }

$UrlBrain   = "https://github.com/$UtenteGitHub/claude-brain.git"
$UrlPrivato = "https://github.com/$UtenteGitHub/claude-private-refs.git"

$script:Problemi = New-Object System.Collections.Generic.List[string]

function Titolo([string]$t) { Write-Host ''; Write-Host "== $t ==" -ForegroundColor Cyan }
function Ok([string]$t)     { Write-Host "  [ok] $t" -ForegroundColor Green }
function Nota([string]$t)   { Write-Host "  [..] $t" -ForegroundColor Gray }
function Manca([string]$t, [string]$rimedio) {
    Write-Host "  [!!] $t" -ForegroundColor Red
    if ($rimedio) { Write-Host "       -> $rimedio" -ForegroundColor Yellow }
    $script:Problemi.Add($t)
}
function HaComando([string]$nome) { return [bool](Get-Command $nome -ErrorAction SilentlyContinue) }

Write-Host ''
Write-Host '=== ROUTINE DEL LUNEDI: installazione e controllo ===' -ForegroundColor Cyan
if ($SoloControllo) { Write-Host '(solo controllo: non scarico, non installo, non sposto niente)' -ForegroundColor Yellow }
Write-Host "  questo repo   : $Flywheel"
Write-Host "  repo privato  : $CartellaPrivata"
Write-Host "  skill e config: $ClaudeHome"

# ---------------------------------------------------------------------------------------------
Titolo '1. Programmi'

$haGit = HaComando 'git'
if ($haGit) { Ok 'git' } else { Manca 'git non installato' 'https://git-scm.com/download/win' }

$Python = $null
if (HaComando 'py') {
    & py -3 -c "import sys" 2>$null
    if ($LASTEXITCODE -eq 0) { $Python = 'py -3' }
}
if (-not $Python -and (HaComando 'python')) {
    & python -c "import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)" 2>$null
    if ($LASTEXITCODE -eq 0) { $Python = 'python' }
}
if ($Python) { Ok "Python 3 ($Python)" } else { Manca 'Python 3 non trovato' 'https://www.python.org/downloads/ (lascia spuntato "py launcher")' }

$haNpm = HaComando 'npm'
if ($haNpm) { Ok 'Node e npm' } else { Manca 'Node.js non installato' 'https://nodejs.org (serve per Claude Code e per il collegamento a Chrome)' }

$haClaude = HaComando 'claude'
if ($haClaude) { Ok 'Claude Code (comando claude)' } else { Manca 'Claude Code non installato' 'npm install -g @anthropic-ai/claude-code   oppure installa l''app desktop di Claude' }

$chromeExe = @(
    (Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe'),
    (Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe')
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if ($chromeExe) { Ok 'Google Chrome' } else { Manca 'Google Chrome non trovato' 'https://www.google.com/chrome/' }

# ---------------------------------------------------------------------------------------------
Titolo '2. I tre repo'

function AggiornaRepo([string]$cartella, [string]$nome) {
    if ($SoloControllo) { Ok "$nome presente"; return }
    & git -C $cartella pull --ff-only --quiet
    if ($LASTEXITCODE -eq 0) { Ok "$nome aggiornato" }
    else { Manca "$nome presente ma non aggiornabile in automatico" "apri $cartella e guarda git status: probabilmente ci sono modifiche locali" }
}

# 2a. questo repo
if ($haGit) { AggiornaRepo $Flywheel 'System-content-flywheel' }

# 2b. claude-brain dentro la cartella di Claude
if (-not $haGit) {
    Nota 'salto i repo: manca git'
} elseif (Test-Path (Join-Path $ClaudeHome '.git')) {
    AggiornaRepo $ClaudeHome 'claude-brain (skill)'
} elseif ($SoloControllo) {
    Manca "claude-brain non installato in $ClaudeHome" 'rilancia senza -SoloControllo'
} elseif (-not (Test-Path $ClaudeHome)) {
    & git clone --quiet $UrlBrain $ClaudeHome
    if ($LASTEXITCODE -eq 0) { Ok 'claude-brain scaricato' } else { Manca 'claude-brain: clone fallito' $UrlBrain }
} else {
    # La cartella esiste gia' (Claude la crea al primo avvio) ma non e' un repo.
    # La collego a GitHub senza cancellare niente: i file locali che il repo sovrascriverebbe
    # vengono spostati in una cartella di backup FUORI da .claude.
    Nota "$ClaudeHome esiste ma non e' collegata a GitHub: la collego"
    & git -C $ClaudeHome init --quiet
    & git -C $ClaudeHome symbolic-ref HEAD refs/heads/main
    & git -C $ClaudeHome remote add origin $UrlBrain
    & git -C $ClaudeHome fetch --quiet origin main
    if ($LASTEXITCODE -ne 0) {
        Manca 'claude-brain: non riesco a scaricare da GitHub' $UrlBrain
    } else {
        $backup = "$ClaudeHome-prima-di-claude-brain-" + (Get-Date -Format 'yyyyMMdd-HHmmss')
        $spostati = 0
        $tracciati = & git -C $ClaudeHome -c core.quotepath=false ls-tree -r --name-only origin/main
        foreach ($f in $tracciati) {
            $locale = Join-Path $ClaudeHome $f
            if (Test-Path -LiteralPath $locale) {
                $dest = Join-Path $backup $f
                New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
                Move-Item -LiteralPath $locale -Destination $dest
                $spostati++
            }
        }
        & git -C $ClaudeHome checkout --quiet -B main origin/main
        if ($LASTEXITCODE -eq 0) {
            Ok 'claude-brain collegato e scaricato'
            if ($spostati -gt 0) { Nota "$spostati file locali spostati in $backup (se ti servono sono li')" }
        } else {
            Manca 'claude-brain: checkout fallito' "guarda git status in $ClaudeHome; il backup e' in $backup"
        }
    }
}

# 2c. repo privato con i dati
if ($haGit) {
    if (Test-Path (Join-Path $CartellaPrivata '.git')) {
        AggiornaRepo $CartellaPrivata 'claude-private-refs (dati)'
    } elseif ($SoloControllo) {
        Manca "claude-private-refs non presente in $CartellaPrivata" 'rilancia senza -SoloControllo'
    } else {
        & git clone --quiet $UrlPrivato $CartellaPrivata
        if ($LASTEXITCODE -eq 0) { Ok 'claude-private-refs scaricato' }
        else { Manca 'claude-private-refs: clone fallito' "e' un repo privato: fai prima l'accesso a GitHub (gh auth login) e rilancia" }
    }
}

# ---------------------------------------------------------------------------------------------
Titolo '3. Collegamento a Chrome (serve per leggere le impressioni dei post)'

if (HaComando 'chrome-devtools-mcp') {
    Ok 'chrome-devtools-mcp installato'
} elseif ($SoloControllo -or -not $haNpm) {
    Manca 'chrome-devtools-mcp non installato' 'npm install -g chrome-devtools-mcp'
} else {
    & npm install -g chrome-devtools-mcp --silent
    if ((HaComando 'chrome-devtools-mcp')) { Ok 'chrome-devtools-mcp installato ora' } else { Manca 'chrome-devtools-mcp: installazione fallita' 'npm install -g chrome-devtools-mcp' }
}

if ($haClaude) {
    $elenco = (& claude mcp list 2>$null) -join "`n"
    if ($elenco -match 'chrome-devtools-mcp') {
        Ok 'chrome-devtools-mcp registrato in Claude'
    } elseif ($SoloControllo) {
        Manca 'chrome-devtools-mcp non registrato in Claude' 'claude mcp add --scope user chrome-devtools-mcp -- chrome-devtools-mcp --autoConnect'
    } else {
        & claude mcp add --scope user chrome-devtools-mcp -- chrome-devtools-mcp --autoConnect
        if ($LASTEXITCODE -eq 0) { Ok 'chrome-devtools-mcp registrato in Claude ora' } else { Manca 'chrome-devtools-mcp: registrazione fallita' 'claude mcp add --scope user chrome-devtools-mcp -- chrome-devtools-mcp --autoConnect' }
    }
}

# ---------------------------------------------------------------------------------------------
Titolo '4. Pezzi della routine'

$attesi = @(
    @{ Dove = $ClaudeHome;      File = 'skills\content-cockpit\SKILL.md';            Cosa = 'skill content-cockpit' },
    @{ Dove = $ClaudeHome;      File = 'skills\content-cockpit\references\watchlist.md'; Cosa = 'watchlist degli autori' },
    @{ Dove = $ClaudeHome;      File = 'skills\linkedin-viral-post-writer\SKILL.md'; Cosa = 'skill linkedin-viral-post-writer' },
    @{ Dove = $Flywheel;        File = 'CLAUDE.md';                                  Cosa = 'istruzioni del progetto' },
    @{ Dove = $Flywheel;        File = 'knowledge\INDEX.md';                         Cosa = 'knowledge base' },
    @{ Dove = $Flywheel;        File = 'scripts\prompt-content-cockpit.md';          Cosa = 'prompt della routine' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\parse_snapshot.py';                 Cosa = 'script dei dati' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\metrics.csv';                       Cosa = 'numeri dei post' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\posts-full.md';                     Cosa = 'testi dei post' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\voce-analisi.md';                   Cosa = 'analisi della voce' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\temi.csv';                          Cosa = 'temi dei post' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\conversions.md';                    Cosa = 'registro delle conversioni' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\cosa_funziona.py';                  Cosa = 'ricalcolo di cosa funziona' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\scelte.csv';                        Cosa = 'registro delle scelte sulle liste' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\esclusi.csv';                       Cosa = 'post esclusi dai confronti' },
    @{ Dove = $CartellaPrivata; File = 'linkedin\cockpit\README.md';                 Cosa = 'cartella dei report' }
)
$mancanti = 0
foreach ($a in $attesi) {
    if (-not (Test-Path (Join-Path $a.Dove $a.File))) { Manca "manca $($a.Cosa): $($a.File)" ''; $mancanti++ }
}
if ($mancanti -eq 0) { Ok "$($attesi.Count) file su $($attesi.Count) al loro posto" }

$metrics = Join-Path $CartellaPrivata 'linkedin\metrics.csv'
if (Test-Path $metrics) {
    $righe = (Get-Content $metrics | Measure-Object -Line).Lines - 1
    Nota "post in archivio: $righe"
}

# ---------------------------------------------------------------------------------------------
Titolo '5. Task pianificato del lunedi'

$promptFile = Join-Path $Flywheel 'scripts\prompt-content-cockpit.md'
$taskFile   = Join-Path $ClaudeHome 'scheduled-tasks\content-linkedin\SKILL.md'
$daCreare   = $false
if (-not (Test-Path $promptFile)) {
    Nota 'salto: manca il prompt della routine'
} elseif (-not (Test-Path $taskFile)) {
    $daCreare = $true
    Manca 'il task pianificato non esiste su questo computer' 'si crea da dentro Claude: vedi il passo qui sotto'
} else {
    $atteso  = (Get-Content -Path $promptFile -Raw -Encoding UTF8).Replace('{{FLYWHEEL}}', $Flywheel).Replace('{{PRIVATO}}', $CartellaPrivata)
    $attuale = Get-Content -Path $taskFile -Raw -Encoding UTF8
    $attuale = $attuale -replace '(?s)\A---.*?---\s*', ''
    $norm = { param($s) (($s -replace "`r", '') -split "`n" | ForEach-Object { $_.TrimEnd() }) -join "`n" }
    if ((& $norm $atteso).Trim() -eq (& $norm $attuale).Trim()) {
        Ok 'il task esiste e usa il prompt del repo'
    } else {
        $daCreare = $true
        Manca 'il task esiste ma il suo prompt e'' diverso da quello del repo' 'si aggiorna da dentro Claude: vedi il passo qui sotto'
    }
}

# ---------------------------------------------------------------------------------------------
Titolo 'Cosa resta da fare a mano'

Write-Host '  a. Apri l''app Claude e fai l''accesso con il tuo account.'
Write-Host '  b. Su claude.ai controlla che i connettori siano attivi: PostHog, Granola, Gmail, Calendar, Drive.'
Write-Host '     Sono legati all''account, non al computer: di norma li ritrovi gia'' collegati.'
Write-Host '  c. Apri Chrome, fai l''accesso a LinkedIn e attiva una volta il debug remoto:'
Write-Host '     chrome://inspect/#remote-debugging'
if ($daCreare) {
    Write-Host '  d. Apri Claude in questa cartella e scrivi:' -ForegroundColor Yellow
    Write-Host '        Installa il task pianificato del lunedi seguendo scripts/README.md' -ForegroundColor Yellow
}

Write-Host ''
if ($script:Problemi.Count -eq 0) {
    Write-Host 'TUTTO A POSTO: la routine e'' pronta su questo computer.' -ForegroundColor Green
} else {
    Write-Host "DA SISTEMARE: $($script:Problemi.Count)" -ForegroundColor Red
    foreach ($p in $script:Problemi) { Write-Host "  - $p" -ForegroundColor Red }
}
exit $script:Problemi.Count
