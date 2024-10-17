import os
import json
import time
import re
from collections import Counter

# Expresión regular para emojis y caracteres adicionales como banderas
emoji_pattern = re.compile(
    r'[\U0001F600-\U0001F64F]'  # Emoticons
    r'|[\U0001F300-\U0001F5FF]'  # Símbolos y pictogramas
    r'|[\U0001F680-\U0001F6FF]'  # Transporte y mapas
    r'|[\U0001F1E0-\U0001F1FF]'  # Banderas (parejas de letras)
    r'|[\U00002600-\U000026FF]'  # Símbolos misceláneos
    r'|[\U00002700-\U000027BF]'  # Otros símbolos
    r'|[\U0001F700-\U0001F77F]',  # Alquimia y símbolos misceláneos
    re.UNICODE
)

def is_valid_emoji(emoji: str):
    # Filtrar solo emojis que no sean letras aisladas
    if len(emoji) == 1 and emoji.isalpha():
        return False  # Excluir letras aisladas
    return True  # Aceptar emojis y combinaciones válidas

def count_emojis_in_content(file_path: str):
    start_time = time.time()

    emoji_counter = Counter()

    # Lee el archivo línea por línea y procesa cada objeto JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                tweet = json.loads(line.strip())
                content = tweet.get('content', '')
                # Encuentra todos los emojis en el contenido
                emojis_found = emoji_pattern.findall(content)
                # Filtrar solo emojis válidos
                valid_emojis = [emoji for emoji in emojis_found if is_valid_emoji(emoji)]
                emoji_counter.update(valid_emojis)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar el JSON: {e}")
                continue  # Ignorar esta línea y continuar

    # Obtener los 10 emojis más comunes
    top_10_emojis = emoji_counter.most_common(10)
    elapsed_time = time.time() - start_time

    return top_10_emojis, elapsed_time

# Ruta del archivo JSON
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '..', 'farmers-protest-tweets-2021-2-4.json')

# Llamar a la función
top_10_emojis, execution_time = count_emojis_in_content(file_path)

# Mostrar resultados
print("Top 10 emojis más comunes:")
print(top_10_emojis)
print(f"Tiempo de ejecución: {execution_time:.4f} segundos")

