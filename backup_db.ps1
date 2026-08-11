$data = Get-Date -Format "yyyy-MM-dd_HH-mm"
$sursa = "db.sqlite3"
$destinatie = "backups\db_backup_$data.sqlite3"

if (-not (Test-Path "backups")) {
    New-Item -ItemType Directory -Path "backups" | Out-Null
}

Copy-Item $sursa $destinatie
Write-Host "Backup creat: $destinatie"
