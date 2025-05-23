import requests
import matplotlib.pyplot as plt

def get_continent(country_name):
    """Consulta a REST Countries API para obter o continente do país"""
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Pega o continente (region)
        continent = data[0].get('region', 'Unknown')
        return continent
    except Exception as e:
        print(f"Erro ao buscar continente de {country_name}: {e}")
        return "Unknown"

def exercicio6():
    # 1) Query para receita por país
    query = """
                SELECT 
                COUNTRY.country as pais, 
                SUM(payment.amount) as receita_total
                FROM payment
                JOIN customer ON payment.customer_id = customer.customer_id
                JOIN address ON customer.address_id = address.address_id
                JOIN city ON address.city_id = city.city_id
                JOIN country  ON country.country_id = city.country_id
                GROUP BY country.country
                ORDER BY receita_total DESC
    """
    dados = run_query(query)

    # 2) Mapear continente para cada país
    receita_por_continente = {}

    for row in dados:
        pais = row['pais']
        receita = row['receita_total']
        continente = get_continent(pais)

        receita_por_continente[continente] = receita_por_continente.get(continente, 0) + receita

    # 3) Plotar gráfico pizza
    labels = list(receita_por_continente.keys())
    values = list(receita_por_continente.values())

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Receita Total por Continente')
    plt.axis('equal') 
    plt.show()