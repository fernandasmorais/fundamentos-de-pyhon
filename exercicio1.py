#   Exercício 1 – Temperatura Média das Capitais dos Clientes
# 	•	Recupere as cidades dos clientes com mais de 10 transações.
# 	•	Use a WeatherAPI para buscar a temperatura atual dessas cidades.
# 	•	Calcule a temperatura média ponderada por número de clientes.
# 	•	Insight esperado: quais cidades concentram clientes e temperaturas extremas?


# importando bibliotecas para o ex1
import os
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import requests
import seaborn as sns
from dotenv import load_dotenv

# Carregar variáveis de ambiente
def get_temperature(city_name, api_key):
    """Busca a temperatura atual da cidade usando a WeatherAPI"""
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": city_name,
        "aqi": "no"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()["current"]["temp_c"]
    else:
        print(f"Erro ao buscar temperatura para {city_name}: {response.text}")
        return None

def exercicio1(f6f59664771e4402b45224429251205): 
    query_ex1 = """
        WITH CTE AS (
            SELECT 
                city.city as cidade, 
                COUNT(*) AS qtd_transacoes
            FROM rental
            INNER JOIN customer ON rental.customer_id = customer.customer_id
            INNER JOIN address ON customer.address_id = address.address_id
            INNER JOIN city ON address.city_id = city.city_id
            GROUP BY city.city
            HAVING COUNT(*) > 10
        )
        SELECT cidade, qtd_transacoes FROM CTE;
    """
    result_query = run_query(query_ex1)

    cidades_temperaturas = []
    total_transacoes = 0
    soma_ponderada_temperaturas = 0

    for row in result_query:
        cidade = row['cidade']
        qtd_transacoes = row['qtd_transacoes']
        temperatura = get_temperature(cidade, api_key)

        if temperatura is not None:
            cidades_temperaturas.append((cidade, qtd_transacoes, temperatura))
            soma_ponderada_temperaturas += temperatura * qtd_transacoes
            total_transacoes += qtd_transacoes

    temperatura_media_ponderada = (
        soma_ponderada_temperaturas / total_transacoes
        if total_transacoes > 0 else None
    )

    print("Temperatura média ponderada:", temperatura_media_ponderada)
    print("\nCidades com temperaturas extremas e alta concentração de clientes:")

    # Definir o critério de temperaturas extremas (usando por exemplo: <15°C e >30°C)
    for cidade, qtd, temp in cidades_temperaturas:
        if temp < 15 or temp > 30:
            print(f"{cidade}: {temp}°C com {qtd} transações")
