import os
import json
import re
from collections import Counter
from memory_profiler import memory_usage

# Expresión regular para encontrar menciones (@username)
mention_pattern = re.compile(r'@(\w+)')  # Captura el nombre de usuario sin el @

def count_mentions_in_content(file_path: str):
    # Inicializar el contador de menciones
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
            except json.JSONDecodeError:
                continue  # Ignorar líneas no decodificables

    # Obtener las 10 menciones más comunes
    top_10_mentions = mention_counter.most_common(10)
    return top_10_mentions

# Función envoltorio para medir el uso de memoria
def wrapper_function(file_path):
    return count_mentions_in_content(file_path)

if __name__ == '__main__':
    # Medir el uso de memoria
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'farmers-protest-tweets-2021-2-4.json')
    mem_usage = memory_usage((wrapper_function, (file_path,)))

    # Llamar a la función y obtener resultados
    top_10_mentions = wrapper_function(file_path)

    # Mostrar resultados
    print("Top 10 usuarios más mencionados (sin @):")
    print(top_10_mentions)

    # Mostrar el uso de memoria
    print(f"Uso de memoria (en MiB): {max(mem_usage) - min(mem_usage)}")

