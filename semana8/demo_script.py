import requests
import json
import time

# Configuración
AUTH_URL = "http://localhost:8002/login"
API_URL = "http://localhost:8000/products"
# Credenciales correctas según app.py (email en lugar de username)
CREDENTIALS = {"email": "admin@ecomarket.com", "password": "password123"}

# Datos de prueba para crear un producto
TEST_PRODUCT = {
    "id": 999,
    "name": "Producto Demo Seguridad",
    "price": 50.0,
    "stock": 10
}

def print_step(step, message):
    print(f"\n{'='*60}")
    print(f"PASO {step}: {message}")
    print(f"{'='*60}")
    time.sleep(1.5)

def run_demo():
    print("\n🎬 INICIANDO DEMOSTRACIÓN DE SEGURIDAD JWT PARA ECOMARKET")
    print("Asegúrate de que los servicios estén corriendo...")
    time.sleep(2)

    # 1. Request sin token
    print_step(1, "Intento de acceso a ruta protegida SIN TOKEN")
    print(f"📡 Enviando solicitud POST a {API_URL} sin cabeceras de autorización...")
    try:
        # Usamos POST porque GET /products no existe, y POST está protegido
        response = requests.post(API_URL, json=TEST_PRODUCT)
        print(f"❌ Status Code: {response.status_code}")
        print(f"📄 Respuesta del servidor: {response.json()}")
        if response.status_code in [401, 403]:
            print("✅ COMPORTAMIENTO ESPERADO: Acceso denegado.")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(2)

    # 2. Login exitoso
    print_step(2, "Autenticación de Usuario (Login)")
    print(f"📡 Enviando solicitud POST a {AUTH_URL}")
    print(f"🔑 Credenciales: {CREDENTIALS}")
    token = None
    try:
        response = requests.post(AUTH_URL, json=CREDENTIALS)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Status Code: {response.status_code}")
            print("✅ Login EXITOSO.")
            print(f"🎟️ Token JWT recibido: {token[:30]}...[truncado]")
        else:
            print(f"❌ Fallo en login: {response.text}")
            return
    except Exception as e:
        print(f"Error: {e}")
        return

    time.sleep(2)

    # 3. Request con token
    print_step(3, "Intento de acceso a ruta protegida CON TOKEN")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        print(f"📡 Enviando solicitud POST a {API_URL}")
        print("🛡️ Headers: {'Authorization': 'Bearer <token_jwt>'}")
        try:
            # Intentamos crear el producto con el token
            response = requests.post(API_URL, json=TEST_PRODUCT, headers=headers)
            print(f"✅ Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Acceso AUTORIZADO. Producto creado.")
                print(f"📄 Respuesta: {response.json()}")
                
                # Limpieza (opcional)
                print("\n🧹 Limpiando datos de prueba...")
                requests.delete(f"{API_URL}/{TEST_PRODUCT['id']}", headers=headers)
                print("✅ Producto de prueba eliminado.")
            else:
                print(f"⚠️ Respuesta inesperada: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

    print("\n✨ DEMOSTRACIÓN COMPLETADA ✨")

if __name__ == "__main__":
    run_demo()