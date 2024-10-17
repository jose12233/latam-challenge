import os
import json
import time
from collections import Counter
from datetime import datetime


def count_dates_and_users(file_path: str):
    start_time = time.time()

    # Inicializa un contador para las fechas y los usuarios
    date_user_counter = {}

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
                    if date not in date_user_counter:
                        date_user_counter[date] = Counter()
                    date_user_counter[date][username] += 1
            except json.JSONDecodeError as e:
                print(f"Error al decodificar el JSON: {e}")
                continue  # Ignorar esta línea y continuar

    # Obtener las 10 fechas más comunes
    top_dates = Counter({date: sum(user_counter.values()) for date, user_counter in date_user_counter.items()}).most_common(10)

    # Para cada fecha, encontrar el usuario con más tweets en esa fecha
    top_dates_with_users = []
    for date, _ in top_dates:
        most_active_user = date_user_counter[date].most_common(1)[0][0]  # Usuario más activo
        top_dates_with_users.append((datetime.strptime(date, '%Y-%m-%d').date(), most_active_user))

    elapsed_time = time.time() - start_time

    # Retornar la lista de tuplas y el tiempo de ejecución
    return top_dates_with_users, elapsed_time

# Obtener la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))    

# Construir la ruta al archivo JSON que está un nivel arriba
file_path = os.path.join(current_dir, '..', 'farmers-protest-tweets-2021-2-4.json')

# Llamar a la función
top_dates_with_users, execution_time = count_dates_and_users(file_path)

# Mostrar los resultados
print("Top 10 fechas mas comunes con el usuario mas activo:")
print(top_dates_with_users)
print(f"Tiempo de ejecucion : {execution_time:.4f} segundos")

