# Script para subir EcoMarket API a GitHub
# Ejecutar este archivo después de instalar Git

Write-Host "🚀 Subiendo EcoMarket API a GitHub..." -ForegroundColor Cyan
Write-Host ""

# Configurar Git
Write-Host "⚙️ Configurando Git..." -ForegroundColor Yellow
git config --global user.name "EcoMarket Developer"
git config --global user.email "dev@ecomarket.com"

# Inicializar repositorio
Write-Host "📁 Inicializando repositorio..." -ForegroundColor Yellow
git init

# Agregar todos los archivos
Write-Host "➕ Agregando archivos..." -ForegroundColor Yellow
git add .

# Crear commit inicial
Write-Host "💾 Creando commit..." -ForegroundColor Yellow
git commit -m "📚 Documentación completa por semanas (1-9) - EcoMarket API Enterprise

Incluye:
- ✅ Semana 1: API REST Básica con FastAPI
- ✅ Semana 2: Interfaz Web (HTML/CSS/JS)
- ✅ Semana 3: Mensajería con RabbitMQ
- ✅ Semana 4: Resiliencia y Manejo de Fallos
- ✅ Semana 5: Testing (pytest, Locust)
- ✅ Semana 6: Escalabilidad (Load Balancer, Sharding)
- ✅ Semana 7: Observabilidad (Prometheus, Grafana)
- ✅ Semana 7-IA: Integración con Machine Learning
- ✅ Semana 8: Autenticación JWT y Roles
- ✅ Semana 9: HTTPS/TLS y Gestión de Secrets

Sistema completo de gestión de inventarios con arquitectura enterprise-grade."

Write-Host ""
Write-Host "✅ Commit creado exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "📌 Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Ve a: https://github.com/new" -ForegroundColor White
Write-Host "2. Nombre del repositorio: ecomarket-api" -ForegroundColor White
Write-Host "3. Descripción: Sistema Enterprise de Gestión de Inventarios" -ForegroundColor White
Write-Host "4. Selecciona: Público o Privado" -ForegroundColor White
Write-Host "5. NO marques 'Add a README file'" -ForegroundColor White
Write-Host "6. Click 'Create repository'" -ForegroundColor White
Write-Host ""
Write-Host "7. Copia los comandos que GitHub te muestre, o ejecuta:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/TU-USUARIO/ecomarket-api.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  Reemplaza 'TU-USUARIO' con tu usuario real de GitHub" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona Enter cuando hayas creado el repositorio en GitHub..." -ForegroundColor Cyan
Read-Host

# Aquí el usuario debe pegar la URL de su repositorio
Write-Host ""
Write-Host "Ingresa la URL de tu repositorio (ej: https://github.com/usuario/ecomarket-api.git):" -ForegroundColor Cyan
$repoUrl = Read-Host

if ($repoUrl) {
    Write-Host ""
    Write-Host "🔗 Conectando con GitHub..." -ForegroundColor Yellow
    git remote add origin $repoUrl
    
    Write-Host "📤 Cambiando a rama main..." -ForegroundColor Yellow
    git branch -M main
    
    Write-Host "🚀 Subiendo código a GitHub..." -ForegroundColor Yellow
    git push -u origin main
    
    Write-Host ""
    Write-Host "✅ ¡ÉXITO! Proyecto subido a GitHub" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Tu repositorio está en:" -ForegroundColor Cyan
    Write-Host $repoUrl.Replace(".git", "") -ForegroundColor White
    Write-Host ""
    Write-Host "📚 Documentación por semanas en:" -ForegroundColor Cyan
    Write-Host "$($repoUrl.Replace('.git', ''))/tree/main/docs" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ No se ingresó URL. Ejecuta estos comandos manualmente:" -ForegroundColor Red
    Write-Host ""
    Write-Host "git remote add origin https://github.com/TU-USUARIO/ecomarket-api.git" -ForegroundColor Gray
    Write-Host "git branch -M main" -ForegroundColor Gray
    Write-Host "git push -u origin main" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Presiona Enter para salir..." -ForegroundColor Cyan
Read-Host
