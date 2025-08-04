# clean_migrations.ps1
#
# Este script remove as pastas de migração de todos os apps localizados
# no diretório 'apps'. Ele também limpa os diretórios __pycache__ do projeto
# e, opcionalmente, apaga o banco de dados de desenvolvimento (db.sqlite3).

# --- Configuração dos Caminhos ---
# Assume que o script está em uma pasta como .scripts/ na raiz do projeto.
$projectRoot = Resolve-Path "$PSScriptRoot\.."
$appsDir = Join-Path $projectRoot "apps"
$dbPath = Join-Path $projectRoot "db.sqlite3"

# --- 1. Limpeza das Pastas de Migração ---
Write-Host "Iniciando a limpeza das migrações..." -ForegroundColor Yellow

if (-not (Test-Path -Path $appsDir)) {
    Write-Host "Diretório '$($appsDir.Split('\')[-1])' não encontrado. Nenhuma migração para limpar." -ForegroundColor Red
} else {
    # Pega todos os subdiretórios dentro de 'apps'
    $allApps = Get-ChildItem -Path $appsDir -Directory

    foreach ($appDir in $allApps) {
        $migrationsPath = Join-Path $appDir.FullName "migrations"
        
        if (Test-Path -Path $migrationsPath) {
            Write-Host "  - Removendo migrações do app '$($appDir.Name)'..."
            Remove-Item -Path $migrationsPath -Recurse -Force
        } else {
            Write-Host "  - App '$($appDir.Name)' não possui pasta de migrações."
        }
    }
}

# --- 2. Limpeza do Cache do Python (__pycache__) ---
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


# --- 3. Exclusão do Banco de Dados de Desenvolvimento ---
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