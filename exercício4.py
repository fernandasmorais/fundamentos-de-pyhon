import requests
from dotenv import load_dotenv
import os

# Carrega API Key
load_dotenv()
API_KEY_AIRVISUAL = os.getenv("AIRVISUAL_API_KEY")

def get_aqi(city_name, country="Brazil"):  # pode precisar adaptar o país
    """Consulta o AQI da cidade usando a AirVisual API"""
    url = "http://api.airvisual.com/v2/city"
    params = {
        "city": city_name,
        "country": country,
        "state": "State",  # você pode precisar identificar o estado correto
        "key": API_KEY_AIRVISUAL
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["data"]["current"]["pollution"]["aqius"]
        else:
            print(f"Erro ao buscar AQI de {city_name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao consultar AQI de {city_name}: {e}")
        return None

def exercicio4():
    # Passo 1: cidades com mais clientes
    query_cidades = """
        SELECT 
            city.city AS cidade,
            country.country AS pais,
            COUNT(customer.customer_id) AS qtd_clientes
        FROM customer
        INNER JOIN address ON customer.address_id = address.address_id
        INNER JOIN city ON address.city_id = city.city_id
        INNER JOIN country ON city.country_id = country.country_id
        GROUP BY cidade, pais
        ORDER BY qtd_clientes DESC
        LIMIT 10;
    """
    cidades_top = run_query(query_cidades)

    cidades_poluídas = []

    # Passo 2: checar AQI de cada cidade
    for row in cidades_top:
        cidade = row['cidade']
        pais = row['pais']
        aqi = get_aqi(cidade, country=pais)
        if aqi and aqi > 150:
            cidades_poluídas.append((cidade, pais, aqi))

    if not cidades_poluídas:
        print("Nenhuma cidade com AQI > 150 encontrada.")
        return

    print("\nCidades com alta poluição (AQI > 150):")
    for cidade, pais, aqi in cidades_poluídas:
        print(f"{cidade} ({pais}) - AQI: {aqi}")

    # Passo 3: filmes mais alugados nessas cidades
    cidades_filtro = "', '".join([c[0] for c in cidades_poluídas])
    query_filmes = f"""
        SELECT 
            city.city AS cidade,
            film.title AS filme,
            COUNT(rental.rental_id) AS total_alugueis
        FROM rental
        INNER JOIN inventory ON rental.inventory_id = inventory.inventory_id
        INNER JOIN film ON inventory.film_id = film.film_id
        INNER JOIN customer ON rental.customer_id = customer.customer_id
        INNER JOIN address ON customer.address_id = address.address_id
        INNER JOIN city ON address.city_id = city.city_id
        WHERE city.city IN ('{cidades_filtro}')
        GROUP BY cidade, filme
        ORDER BY total_alugueis DESC
        LIMIT 10;
    """
    filmes_populares = run_query(query_filmes)

    print("\nFilmes mais populares em cidades poluídas:")
    for row in filmes_populares:
        print(f"{row['cidade']}: {row['filme']} ({row['total_alugueis']} aluguéis)")