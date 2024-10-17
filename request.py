import requests
import json

# Definir la URL del API
url = "https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/data-engineer"

# Crear el cuerpo del request
data = {
    "name": "Jose Rodriguez",  
    "mail": "josealbero1223@gmail.com",  
    "github_url": "https://github.com/jose12233/latam-challenge.git"
}

# Hacer el request POST
response = requests.post(url, json=data)

# Comprobar la respuesta
if response.status_code == 200:
    print("Desafío enviado exitosamente.")
else:
    print(f"Error al enviar el desafío: {response.status_code} - {response.text}")
