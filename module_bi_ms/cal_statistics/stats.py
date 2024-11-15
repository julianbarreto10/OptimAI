
def calculate_statistics(routing_data):
    # Filtra las rutas válidas y calcula las estadísticas
    total_rutas = len(routing_data)
    total_paquetes = sum(len(item['rutas']) for item in routing_data)
    total_tiempo = sum(ruta['Tiempo'] for item in routing_data for ruta in item['rutas'])
    total_costo = sum(ruta['costo'] for item in routing_data for ruta in item['rutas'])
    total_volumen = sum(ruta['vol'] for item in routing_data for ruta in item['rutas'])
    
    # Cálculo de estadísticas promedio
    tiempo_promedio = total_tiempo / total_paquetes if total_paquetes else 0
    costo_promedio = total_costo / total_paquetes if total_paquetes else 0
    volumen_promedio = total_volumen / total_paquetes if total_paquetes else 0

    # Retornar el resultado en un diccionario
    return {
        "total_rutas": total_rutas,
        "total_paquetes": total_paquetes,
        "tiempo_promedio": tiempo_promedio,
        "costo_promedio": costo_promedio,
        "volumen_promedio": volumen_promedio
    }