# Scripts E2E simples en PowerShell para la API de ejemplo
# Requiere que la API esté corriendo en http://127.0.0.1:8000

$base = 'http://127.0.0.1:8000'

Write-Host "1) Crear producto (espera 201)"
$body = @{ name='Camiseta'; price=199.5; currency='MXN'; tags=@('ropa')} | ConvertTo-Json
$resp = Invoke-RestMethod -Method Post -Uri "$base/api/v1/products" -Body $body -ContentType 'application/json' -ErrorAction Stop
Write-Host "Respuesta crear:`n" ($resp | ConvertTo-Json -Depth 5)

Write-Host "2) Listar productos (espera 200)"
$list = Invoke-RestMethod -Method Get -Uri "$base/api/v1/products" -ErrorAction Stop
Write-Host ($list | ConvertTo-Json -Depth 5)

Write-Host "3) Caso válido / inválido"
try {
  $bad = @{ name='A'; price=-5; currency='XXX' } | ConvertTo-Json
  Invoke-RestMethod -Method Post -Uri "$base/api/v1/products" -Body $bad -ContentType 'application/json' -ErrorAction Stop
} catch {
  Write-Host "Error esperado al crear inválido:`n" $_.Exception.Response.StatusCode.value__
}

Write-Host "Fin de pruebas E2E básicas"