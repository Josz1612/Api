# pgbadger_report.ps1
# Extrae logs del primario y ejecuta pgBadger en Docker, produce reporte_primary.html en la carpeta del repo.

Set-Location -LiteralPath "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)\.."
Write-Output "Working dir: $(Get-Location)"

$localLog = [IO.Path]::Combine((Get-Location).Path, 'artifacts', 'pg_primary.log')
if (-Not (Test-Path -LiteralPath $localLog)) {
    Write-Output "No local artifact log found at $localLog. Attempting to extract logs from container 'pg_primary'..."
    try {
        docker exec pg_primary bash -lc "cat /var/log/postgresql/postgresql-*.log" > $localLog
        Write-Output "Logs saved to $localLog"
    } catch {
        Write-Error "No local log and could not extract from container 'pg_primary'. Please run the topology and ensure container exists."; exit 1
    }
} else {
    Write-Output "Using existing log: $localLog"
}

# Prefer local pgbadger binary if available
$pgbadgerCmd = Get-Command pgbadger -ErrorAction SilentlyContinue
if ($pgbadgerCmd) {
    Write-Output "Running local pgbadger on $localLog..."
    & pgbadger $localLog -o reporte_primary.html
    if (Test-Path -LiteralPath .\reporte_primary.html) { Write-Output "Reporte generado: $(Join-Path ${PWD} 'reporte_primary.html')"; exit 0 }
    Write-Error "pgbadger ejecutado pero no generó reporte."; exit 1
}

Write-Output "Local pgbadger no disponible. Trying Docker images (darold/pgbadger, dalibo/pgbadger, tiredofit/pgbadger)"
$images = @('darold/pgbadger','dalibo/pgbadger','tiredofit/pgbadger')
$success = $false
$outPath = Join-Path (Get-Location).Path 'reporte_primary.html'
foreach ($img in $images) {
    Write-Output ("Intentando imagen: {0}" -f $img)
    try {
        # Mount current folder into /data inside container and run pgbadger on artifacts/pg_primary.log
        $hostPath = (Get-Location).Path
        # Try parsing using stderr format (common for docker logs) if pgbadger can't auto-detect
        docker run --rm -v "${hostPath}:/data" $img -f stderr /data/artifacts/pg_primary.log -o /data/reporte_primary.html
        if (Test-Path -LiteralPath $outPath) { Write-Output ("Reporte generado usando {0}: {1}" -f $img, $outPath); $success = $true; break }
    } catch {
        Write-Output ("Fallo con imagen {0}: {1}" -f $img, $_)
        continue
    }
}

if (-Not $success) {
    Write-Error "No se pudo generar reporte con pgBadger. Instala 'pgbadger' localmente or ensure one of the Docker images is pullable."; exit 1
}