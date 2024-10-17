

import os
import json
import time
from collections import defaultdict, Counter
from datetime import datetime
from memory_profiler import memory_usage

def count_dates_and_users(file_path: str):
    start_time = time.time()

    # Inicializa un contador para las fechas y los usuarios
    date_user_counter = defaultdict(Counter)

    # Lee el archivo línea por línea y procesa cada objeto JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Cargar cada línea como un objeto JSON
            try:
                tweet = json.loads(line.strip())
                # Extraer la fecha y el nombre de usuario
                if 'date' in tweet and 'user' in tweet and 'username' in tweet['user']:
                    date = tweet['date'].split('T')[0]  # Extraer solo la fecha (sin hora)
                    username = tweet['user']['username']
                    date_user_counter[date][username] += 1
            except json.JSONDecodeError as e:
                print(f"Error al decodificar el JSON: {e}")
                continue  # Ignorar esta línea y continuar

    # Obtener las 10 fechas más comunes
    top_dates = Counter({date: sum(user_counter.values()) for date, user_counter in date_user_counter.items()}).most_common(10)

    # Para cada fecha, encontrar el usuario con más tweets en esa fecha
    top_dates_with_users = [
        (datetime.strptime(date, '%Y-%m-%d').date(), user_counter.most_common(1)[0][0]) 
        for date, user_counter in ((date, date_user_counter[date]) for date, _ in top_dates)
    ]

    elapsed_time = time.time() - start_time

    # Retornar la lista de tuplas y el tiempo de ejecución
    return top_dates_with_users, elapsed_time

if __name__ == '__main__':
    # Obtener la ruta del directorio actual del script
    current_dir = os.path.dirname(os.path.abspath(__file__))    

    # Construir la ruta al archivo JSON que está un nivel arriba
    file_path = os.path.join(current_dir, '..', 'farmers-protest-tweets-2021-2-4.json')

    # Monitorear el uso de memoria y llamar a la función
    mem_usage = memory_usage((count_dates_and_users, (file_path,)))

    # Llamar a la función y mostrar los resultados
    top_dates_with_users, execution_time = count_dates_and_users(file_path)

    print("Top 10 fechas más comunes con el usuario más activo:")
    print(top_dates_with_users)
    print(f"Tiempo de ejecución : {execution_time:.4f} segundos")
    print(f"Uso máximo de memoria: {max(mem_usage)} MiB")



