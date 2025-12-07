# Script para iniciar los servicios de EcoMarket (Central API + Auth Service + Sucursal API)

# Iniciar Auth Service en segundo plano (Puerto 8002)
Start-Process -FilePath "python" -ArgumentList "Semana8/app.py" -WindowStyle Minimized
Write-Host "Auth Service iniciado en puerto 8002..."

# Iniciar Sucursal API en segundo plano (Puerto 8001)
Start-Process -FilePath "python" -ArgumentList "Semana3/sucursal_api.py" -WindowStyle Minimized
Write-Host "Sucursal API iniciada en puerto 8001..."

# Esperar un momento
Start-Sleep -Seconds 2

# Iniciar Central API (Puerto 8000)
Write-Host "Iniciando Central API en puerto 8000..."
python "Semana3/central_api.py"