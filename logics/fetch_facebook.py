import requests
import datetime
import streamlit as st

def facebook_api_data_load(page_id, access_token, metrics, days=10):
    """Fetch page insights data from Facebook API."""
    
    # Define o intervalo de datas para a consulta
    until = datetime.date.today()
    since = until - datetime.timedelta(days=days)
    
    # Monta a URL e parâmetros da chamada da API
    url = f"https://graph.facebook.com/v20.0/{page_id}/insights"
    params = {
        'metric': ','.join(metrics),  # Ajuste das métricas válidas
        'since': since.strftime('%Y-%m-%d'),
        'until': until.strftime('%Y-%m-%d'),
        'period': 'day',
        'access_token': access_token
    }
    
    try:
        # Realiza a chamada para a API do Facebook
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lança exceção para códigos de erro HTTP
        data = response.json()
        
        # Verifica se há erros na resposta da API
        if 'error' in data:
            st.error(f"Error fetching page insights: {data['error']['message']}")
            return None
        
        # Retorna os dados recebidos em JSON
        return data
    
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return None

# Lista de métricas válidas para extração
facebook_metrics = [
    "page_post_engagements",
    "page_engaged_users",
    "page_impressions",
    "page_impressions_unique",
    "page_impressions_viral",
    "page_fans",
    "page_fan_adds",
    "page_fan_removes",
    "page_views_total",
    "page_negative_feedback_unique"
]

# Chamada da função no Streamlit
page_id = "1060285064080786"  # ID da página do Facebook
access_token = "EAAOBMtxoGREBOxZCQBztXV0ubEQXNm34PWOrrVGpSZCLlreoQfO5yv0fxmDxwtLSKKZASwh7GPjh5IguGG3riDF4oM4iHqONpxA2tlfjhBR3xXf2NpSFFZCbtZB6PYaOckONDfZCwWusNl36MJvg22unmZBBrnfsTP6fjAppNLAcuZCz6XZCGjxyrNkPI4GiMMQZDZD"  # Substitua pelo token de acesso válido

# Carrega os dados para exibição no Streamlit
data = facebook_api_data_load(page_id, access_token, facebook_metrics)

# Exibe os dados na interface do Streamlit
if data:
    st.write("Dados de Insights da Página:")
    st.json(data)
