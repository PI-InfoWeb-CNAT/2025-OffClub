$projectRoot = Resolve-Path "$PSScriptRoot\.."
$venvPath = Join-Path $projectRoot ".venv"
$venvActivate = Join-Path $venvPath "Scripts\Activate.ps1"
$requirementsPath = Join-Path $projectRoot "requirements.txt"

python -m venv $venvPath

if (Test-Path $venvActivate) {
    & $venvActivate

    python -m pip install --upgrade pip
    if (Test-Path $requirementsPath) {
        python -m pip install -r $requirementsPath
        Write-Host "Dependencias instaladas com sucesso." -ForegroundColor Green 
    } else {
        Write-Host "Arquivo requirements.txt nao encontrado." -ForegroundColor Red 
    }
} else {
    Write-Host "Nao foi possível ativar o ambiente virtual." -ForegroundColor Red
}