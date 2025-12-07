Observación de Rendimiento (simulada)
1. Tiempos base
1 petición GET /products: 20 ms
2. Simulación de carga
50 peticiones seguidas: promedio 22 ms, percentil 95: 30 ms
3. Latencia artificial (time.sleep(0.5))
1 petición: 500 ms
50 peticiones: promedio 505 ms, percentil 95: 510 ms
4. Hipótesis de abandono
Si el tiempo de respuesta supera 2 segundos, los usuarios probablemente abandonan la app.