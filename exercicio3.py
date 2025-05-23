import requests
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
API_REST_COUNTRIES = "https://restcountries.com/v3.1/name/"

def get_population(country_name):
    """Busca a população do país usando a REST Countries API"""
    try:
        response = requests.get(f"{API_REST_COUNTRIES}{country_name}")
        if response.status_code == 200:
            data = response.json()
            return data[0]["population"]
        else:
            print(f"Erro na API para {country_name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao buscar {country_name}: {e}")
        return None

def exercicio3():
    # Consulta SQL: aluguéis por país
    query = """
        SELECT 
            country.country AS pais,
            COUNT(rental.rental_id) AS qtd_alugueis
        FROM rental
        INNER JOIN customer ON rental.customer_id = customer.customer_id
        INNER JOIN address ON customer.address_id = address.address_id
        INNER JOIN city ON address.city_id = city.city_id
        INNER JOIN country ON city.country_id = country.country_id
        GROUP BY country.country
        ORDER BY qtd_alugueis DESC;
    """
    result_query = run_query(query)

    dados_final = []
    
    for row in result_query:
        pais = row["pais"]
        qtd_alugueis = row["qtd_alugueis"]
        populacao = get_population(pais)

        if populacao and populacao > 0:
            alugueis_por_1000 = (qtd_alugueis / populacao) * 1000
            dados_final.append((pais, qtd_alugueis, populacao, alugueis_por_1000))
    
    # Ordena do mais "cinéfilo" ao menos
    dados_ordenados = sorted(dados_final, key=lambda x: x[3], reverse=True)

    print("Top países mais cinéfilos (aluguel por 1.000 habitantes):\n")
    for pais, alugueis, pop, taxa in dados_ordenados[:10]:
        print(f"{pais}: {taxa:.2f} aluguéis por 1.000 habitantes")
