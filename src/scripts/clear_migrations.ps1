$projectRoot = Resolve-Path "$PSScriptRoot\.."
$appsDir = Join-Path $projectRoot "apps"
$dbPath = Join-Path $projectRoot "db.sqlite3"

Write-Host "Iniciando a limpeza dos arquivos de migração..." -ForegroundColor Yellow

if (-not (Test-Path -Path $appsDir)) {
    Write-Host "Diretório '$($appsDir.Split('\')[-1])' não encontrado. Nenhuma migração para limpar." -ForegroundColor Red
} else {
    $allApps = Get-ChildItem -Path $appsDir -Directory

    foreach ($appDir in $allApps) {
        $migrationsPath = Join-Path $appDir.FullName "migrations"
        
        if (Test-Path -Path $migrationsPath) {
            Write-Host "  - Removendo arquivos de migração do app '$($appDir.Name)'..."
            Get-ChildItem -Path $migrationsPath -File | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item -Force
        } else {
            Write-Host "  - App '$($appDir.Name)' não possui pasta de migrações."
        }
    }
}

Write-Host "Limpando pastas __pycache__ do projeto..." -ForegroundColor Yellow
$pycacheDirs = Get-ChildItem -Path $projectRoot -Directory -Recurse -Filter "__pycache__"
if ($pycacheDirs) {
    $pycacheDirs | ForEach-Object {
        Write-Host "  - Removendo $($_.FullName)..."
        Remove-Item $_.FullName -Recurse -Force
    }
} else {
    Write-Host "Nenhuma pasta __pycache__ encontrada."
}

if (Test-Path -Path $dbPath) {
    $confirm = Read-Host "Deseja apagar o banco de dados de desenvolvimento (db.sqlite3)? (s/n)"
    if ($confirm.ToLower() -eq 's') {
        Write-Host "Removendo o banco de dados..." -ForegroundColor Yellow
        Remove-Item -Path $dbPath -Force
        Write-Host "Banco de dados 'db.sqlite3' apagado." -ForegroundColor Green
    } else {
        Write-Host "O banco de dados não foi apagado."
    }
}

Write-Host "Limpeza concluída com sucesso." -ForegroundColor Green