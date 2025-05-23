#   Exercício 5 – Clientes em Áreas Críticas
# 	•	Recupere os clientes com endereço em cidades com AQI acima de 130.
# 	•	Combine nome do cliente, cidade, país, temperatura e AQI.
# 	•	Classifique os clientes em “zona de atenção” com base nos critérios ambientais.
import requests
import os
from dotenv import load_dotenv

load_dotenv()
AIRVISUAL_API_KEY = os.getenv("AIRVISUAL_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_aqi(city, country="Brazil", state=None):
    url = "http://api.airvisual.com/v2/city"
    params = {
        "city": city,
        "country": country,
        "key": AIRVISUAL_API_KEY
    }
    if state:
        params["state"] = state
    try:
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            return data["data"]["current"]["pollution"]["aqius"]
        else:
            print(f"Erro AQI {city}: {resp.status_code}")
    except Exception as e:
        print(f"Erro AQI {city}: {e}")
    return None

def get_temperature(city, country="Brazil"):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{city},{country}",
        "aqi": "no"
    }
    try:
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            return data["current"]["temp_c"]
        else:
            print(f"Erro Temp {city}: {resp.status_code}")
    except Exception as e:
        print(f"Erro Temp {city}: {e}")
    return None

def exercicio5():
    # 1) Buscar clientes em cidades com AQI > 130

    # Query para buscar clientes com cidade e país
    query = """
                SELECT
                        customer.first_name as primeiro_nome,
                        customer.last_name as ultimo_nome,
                        city.city as cidade,
                        address.address as endereco
                FROM customer
                JOIN address ON customer.address_id = address.address_id
                JOIN city ON address.city_id = city.city_id
                JOIN country ON city.country_id = country.country_id;
    """
    clientes = run_query(query)

    resultados = []

    for row in clientes:
        cidade = row['cidade']
        pais = row['pais']
        cliente = row['cliente']

        aqi = get_aqi(cidade, country=pais)
        if aqi and aqi > 130:
            temp = get_temperature(cidade, country=pais)

            # Classificação:
            # Zona de atenção se AQI > 130 e temperatura > 30C
            if aqi > 130 and (temp is not None and temp > 30):
                zona = "Alerta Vermelho"
            elif aqi > 130:
                zona = "Alerta Laranja"
            else:
                zona = "Normal"

            resultados.append({
                "cliente": cliente,
                "cidade": cidade,
                "pais": pais,
                "temperatura_c": temp,
                "AQI": aqi,
                "zona": zona
            })

    # Imprime resultado
    print(f"\nClientes em áreas críticas (AQI > 130): {len(resultados)} encontrados.\n")
    for r in resultados:
        print(f"{r['cliente']} - {r['cidade']}, {r['pais']} - Temp: {r['temperatura_c']}°C - AQI: {r['AQI']} - Zona: {r['zona']}")
