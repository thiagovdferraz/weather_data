import requests
import json
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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