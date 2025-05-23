#   Exercício 8 – Perfil de Clima por Cliente
# 	•	Para cada cliente, crie um perfil com:
# 	•	cidade, temperatura, AQI, total de aluguéis, gasto total.
# 	•	Agrupe os perfis por faixa etária (simulada ou fictícia) e avalie padrões.
# 	•	Objetivo: conectar comportamento de consumo e ambiente.

import random

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
    except:
        pass
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
    except:
        pass
    return None

def exercicio8():
    # 1) Query para dados do cliente, cidade, soma aluguéis e gasto total
    query = """
    SELECT
        customer.customer_id,
        customer.first_name || ' ' || customer.last_name AS cliente,
        city.city AS cidade,
        COUNT(rental.rental_id) AS total_alugueis,
        SUM(payment.amount) AS gasto_total
    FROM customer
    INNER JOIN address ON customer.address_id = address.address_id
    INNER JOIN city ON address.city_id = city.city_id
    LEFT JOIN rental ON customer.customer_id = rental.customer_id
    LEFT JOIN payment ON rental.rental_id = payment.rental_id
    GROUP BY customer.customer_id, cliente, cidade
    ORDER BY cliente;
    """

    dados = run_query(query)

    perfis = []

    for row in dados:
        cliente = row["cliente"]
        cidade = row["cidade"]
        total_alugueis = row["total_alugueis"] or 0
        gasto_total = row["gasto_total"] or 0.0

        temp = get_temperature(cidade)
        aqi = get_aqi(cidade)

        # Simula faixa etária
        idade = random.randint(18, 65)
        if idade < 30:
            faixa = "Jovem"
        elif idade < 50:
            faixa = "Adulto"
        else:
            faixa = "Sênior"

        perfis.append({
            "cliente": cliente,
            "cidade": cidade,
            "temperatura": temp,
            "AQI": aqi,
            "total_alugueis": total_alugueis,
            "gasto_total": gasto_total,
            "idade": idade,
            "faixa_etaria": faixa
        })

    # Agrupa por faixa etária 
    resumo_faixas = {}
    for p in perfis:
        faixa = p["faixa_etaria"]
        if faixa not in resumo_faixas:
            resumo_faixas[faixa] = {
                "total_alugueis": 0,
                "gasto_total": 0.0,
                "count": 0
            }
        resumo_faixas[faixa]["total_alugueis"] += p["total_alugueis"]
        resumo_faixas[faixa]["gasto_total"] += p["gasto_total"]
        resumo_faixas[faixa]["count"] += 1

    print("Resumo por faixa etária:")
    for faixa, vals in resumo_faixas.items():
        media_alugueis = vals["total_alugueis"] / vals["count"]
        media_gasto = vals["gasto_total"] / vals["count"]
        print(f"{faixa}: Média Aluguéis={media_alugueis:.2f}, Média Gasto=R$ {media_gasto:.2f}")
