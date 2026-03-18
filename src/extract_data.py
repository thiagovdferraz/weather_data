import requests
import json
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_key = 'bbccf554e55807e02c0efb895faeb031'  # This should be loaded from the .env file in a real application
url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={api_key}'

def extract_weather_data(url:str) -> list:
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        logging.error(f"Erro na requisição: {response.status_code} - {response.text}")
        return []
    
    if not data:
        logging.warning("Nenhum dado encontrado.")
        return []


    outupt_path = 'data/weather_data.json'
    outupt_dir = Path(outupt_path).parent
    outupt_dir.mkdir(parents=True, exist_ok=True)

    with open(outupt_path, 'w') as f:
        json.dump(data, f, indent=4) # Save the data to a JSON file

    logging.info(f"Dados salvos em: {outupt_path}")
    return data


extract_weather_data(url)