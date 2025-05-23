#   Exercício 2 – Receita Bruta em Cidades com Clima Ameno
# 	•	Calcule a receita bruta por cidade.
# 	•	Use a WeatherAPI para consultar a temperatura atual.
# 	•	Filtre apenas cidades com temperatura entre 18°C e 24°C.
# 	•	Resultado: qual o faturamento total vindo dessas cidades?


# importando bibliotecas para o ex2

import os
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import requests
import seaborn as sns
from dotenv import load_dotenv


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

def exercicio2(api_key): 
    # Passo 1: calcular receita bruta por cidade
    query_ex2 = """
        SELECT 
            city.city AS cidade,
            SUM(payment.amount) AS receita_bruta
        FROM payment
        INNER JOIN rental ON payment.rental_id = rental.rental_id
        INNER JOIN customer ON rental.customer_id = customer.customer_id
        INNER JOIN address ON customer.address_id = address.address_id
        INNER JOIN city ON address.city_id = city.city_id
        GROUP BY city.city;
    """
    result_query = run_query(query_ex2)

    faturamento_total_ameno = 0
    cidades_amenas = []

    # Passo 2: consultar temperatura de cada cidade e filtrar as com clima ameno (18–24°C)
    for row in result_query:
        cidade = row['cidade']
        receita = row['receita_bruta']
        temperatura = get_temperature(cidade, api_key)

        if temperatura is not None and 18 <= temperatura <= 24:
            faturamento_total_ameno += receita
            cidades_amenas.append((cidade, temperatura, receita))

    # Exibir resultado
    print("Faturamento total de cidades com clima ameno (18°C a 24°C):")
    print(f"R$ {faturamento_total_ameno:.2f}\n")

    print("Cidades consideradas:")
    for cidade, temp, receita in cidades_amenas:
        print(f"{cidade}: {temp}°C | Receita: R$ {receita:.2f}")

