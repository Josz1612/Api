# Write en primario -> Read en secundario -> medir lag
Set-Location -LiteralPath "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)\.."
Write-Output "Working dir: $(Get-Location)"

Write-Output "1) Ejecutando writes en primario (50 writes)..."
& ".\.venv311\Scripts\python.exe" -c "from load_test import write_load; write_load(50)"

Start-Sleep -Seconds 2

Write-Output "2) Ejecutando lecturas en secundario (200 reads)..."
& ".\.venv311\Scripts\python.exe" -c "from load_test import read_load, SECONDARY_1; read_load(SECONDARY_1, 200, 'Secundario 1')"

Start-Sleep -Seconds 1

Write-Output "3) Midiendo lag de replicación (Secundario 1)..."
& ".\.venv311\Scripts\python.exe" -c "from load_test import check_replication_lag, SECONDARY_1; print('Lag:', check_replication_lag(SECONDARY_1, 'Secundario 1'))"