param([string]$appName)

$projectRoot = Resolve-Path "$PSScriptRoot\.."
$appsDir = Join-Path $projectRoot "apps"
$destPath = Join-Path $appsDir $appName
$managePyPath = Join-Path $projectRoot "manage.py"
$templatePath = Join-Path $projectRoot ".scaffolds/custom_app"

if (-not (Test-Path -Path $appsDir)) {
    New-Item -ItemType Directory -Path $appsDir
}

if (-not (Test-Path -Path $destPath)) {
    New-Item -ItemType Directory -Path $destPath
}

python $managePyPath startapp --template=$templatePath $appName $destPath

Write-Host "App $appName criado com sucesso." -ForegroundColor Green