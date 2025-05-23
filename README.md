## 📊 Análise Ambiental e de Consumo com Dados do Sakila

Este projeto foi desenvolvido como parte da disciplina de **Fundamentos de Python para Engenharia de Dados** do **MBA em Engenharia de Dados da PUC Minas**.

A proposta consistiu na análise de dados da base **Sakila** integrados a APIs externas, com foco em explorar correlações entre aspectos ambientais (como temperatura e qualidade do ar) e o comportamento de clientes, utilizando **Python**, **SQL**, **matplotlib**, e bibliotecas como `requests`, `openpyxl`, `dotenv`.

---

## 🔧 Tecnologias e Ferramentas

* Python 3.12
* PostgreSQL (base Sakila)
* [WeatherAPI](https://www.weatherapi.com/)
* [AirVisual API](https://www.iqair.com/world-air-quality)
* [REST Countries API](https://restcountries.com/)
* matplotlib, openpyxl, requests, python-dotenv

---

## 📂 Estrutura do Projeto

O projeto foi dividido em **nove exercícios**, cada um explorando uma faceta distinta da integração entre dados internos e fontes externas:

---

## ▶️ Como Executar

1. Clone este repositório:

   ```bash
   git clone <url>
   cd <fundamentos-de-python>
   ```

2. Ative o ambiente virtual:

   ```bash
   source dbt-venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` com suas **API keys**:

   ```env
   WEATHER_API_KEY=123456
   AIRVISUAL_API_KEY=abcdef
   ```

5. Execute os scripts:

   ```bash
   python exercicio1.py
   python exercicio9.py
   # ou script unificado
   ```

---

## 📌 Observações

* A base **Sakila** foi adaptada para PostgreSQL.
* A faixa etária dos clientes foi simulada com base em IDs.
* Algumas cidades retornadas nas APIs exigem ajuste de nomes para compatibilidade internacional.
