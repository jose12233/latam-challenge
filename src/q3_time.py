import os
import json
import re
from collections import Counter
import time

# Expresión regular para encontrar menciones (@username)
mention_pattern = re.compile(r'@(\w+)')  # Captura el nombre de usuario sin el @

def count_mentions_in_content(file_path: str):
    start_time = time.time()

    mention_counter = Counter()

    # Lee el archivo línea por línea y procesa cada objeto JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                tweet = json.loads(line.strip())
                content = tweet.get('content', '')
                # Encuentra todas las menciones en el contenido
                mentions_found = mention_pattern.findall(content)  # Extrae solo el nombre sin @
                # Actualizar el contador de menciones
                mention_counter.update(mentions_found)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar el JSON: {e}")
                continue  # Ignorar esta línea y continuar

    # Obtener las 10 menciones más comunes
    top_10_mentions = mention_counter.most_common(10)
    elapsed_time = time.time() - start_time

    return top_10_mentions, elapsed_time

# Ruta del archivo JSON
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '..', 'farmers-protest-tweets-2021-2-4.json')

# Llamar a la función
top_10_mentions, execution_time = count_mentions_in_content(file_path)

# Mostrar resultados
print("Top 10 usuarios más mencionados (sin @):")
print(top_10_mentions)
print(f"Tiempo de ejecución: {execution_time:.4f} segundos")

