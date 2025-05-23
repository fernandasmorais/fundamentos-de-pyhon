
#   Exercício 7 – Tempo Médio de Aluguel vs Clima
# 	•	Calcule o tempo médio de aluguel por cidade (entre rental_date e return_date).
# 	•	Combine com a temperatura atual dessas cidades.
# 	•	Visualize a correlação entre temperatura e tempo médio de aluguel (scatterplot + linha de tendência).
import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def get_temperature(city, country="Brazil"):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{city},{country}",
        "aqi": "no"
    }
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data["current"]["temp_c"]
    except Exception as e:
        print(f"Erro ao buscar temperatura para {city}: {e}")
        return None

def exercicio7():
    # 1) Query para calcular tempo médio de aluguel por cidade (em dias)
    query = """
    SELECT 
        city.city AS cidade,
        AVG(DATE_PART('day', return_date - rental_date)) AS tempo_medio_aluguel
    FROM rental
    INNER JOIN customer ON rental.customer_id = customer.customer_id
    INNER JOIN address ON customer.address_id = address.address_id
    INNER JOIN city ON address.city_id = city.city_id
    WHERE return_date IS NOT NULL
    GROUP BY cidade
    ORDER BY cidade;
    """
    dados = run_query(query)

    temperaturas = []
    tempos = []
    cidades_validas = []

    for row in dados:
        cidade = row["cidade"]
        tempo_medio = row["tempo_medio_aluguel"]
        temp = get_temperature(cidade)

        if temp is not None and tempo_medio is not None:
            cidades_validas.append(cidade)
            temperaturas.append(temp)
            tempos.append(tempo_medio)

    # Plot scatterplot
    plt.figure(figsize=(10,6))
    plt.scatter(temperaturas, tempos, color='blue')

    # Linha de tendência (regressão linear)
    if len(temperaturas) > 1:
        coef = np.polyfit(temperaturas, tempos, 1)
        poly1d_fn = np.poly1d(coef) 
        plt.plot(temperaturas, poly1d_fn(temperaturas), color='red', linewidth=2, label='Linha de Tendência')

    plt.xlabel('Temperatura (°C)')
    plt.ylabel('Tempo Médio de Aluguel (dias)')
    plt.title('Correlação entre Temperatura e Tempo Médio de Aluguel por Cidade')
    plt.legend()
    plt.grid(True)
    plt.show()
