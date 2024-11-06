import requests
import datetime
import streamlit as st

def facebook_api_data_load(page_id, access_token, metrics, days=10):
    """Fetch page insights data from Facebook API."""
    
    # Definir datas de início e fim para o intervalo de análise
    until = datetime.date.today()
    since = until - datetime.timedelta(days=days)
    
    # Montar a URL da API
    url = f"https://graph.facebook.com/v20.0/{page_id}/insights"
    params = {
        'metric': ','.join(metrics),  # Métricas válidas definidas aqui
        'since': since.strftime('%Y-%m-%d'),
        'until': until.strftime('%Y-%m-%d'),
        'period': 'day',
        'access_token': access_token
    }
    
    # Chamada para a API do Facebook
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lança uma exceção para códigos de erro HTTP
        data = response.json()
        
        # Verificar se há erros na resposta da API
        if 'error' in data:
            st.error(f"Error fetching page insights: {data['error']['message']}")
            return None
        return data
    
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return None

# Listagem de métricas válidas ajustadas
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
page_id = "1060285064080786"  # ID da página
access_token = "YOUR_ACCESS_TOKEN"  # Token de acesso válido aqui

# Função de carregamento dos dados para exibição no Streamlit
data = facebook_api_data_load(page_id, access_token, facebook_metrics)

# Exibição de dados no Streamlit
if data:
    st.write("Dados de Insights da Página:")
    st.json(data)
