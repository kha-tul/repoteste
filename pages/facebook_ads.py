# Criar o arquivo facebook_ads.py corrigido
import streamlit as st
import pandas as pd
from facebook_business.api import FacebookAdsApi

from logics.fetch_facebook import *
from logics.date_range import *
from plots.plots_facebook import *
from plots.cards import *
from plots.plots_ads_account import *
from logics.fetch_adaccounts import *
from logics.load_data import facebook_api_data_load, facebook_ads_data_load
from logics.utilis import facebook_apis_tokens
from logics.export_data import export_data

# Configura\u00e7\u00e3o da navega\u00e7\u00e3o
st.sidebar.page_link("main.py", label="Overview", icon="\ud83c\udfe0")
st.sidebar.page_link("pages/Google_Ads_Performance.py", label="Google", icon="\ud83d\udc65")
st.sidebar.page_link("pages/facebook_ads.py", label="Facebook", icon="\ud83d\udc65")
st.sidebar.page_link("pages/instagram_data.py", label="Instagram", icon="\ud83d\udc65")

# Inicializa\u00e7\u00e3o das credenciais
(page_access_token, user_access_token, 
 page_id, adaccount_account_id, adaccount_id) = facebook_apis_tokens()

# Inicializar a API do Facebook
FacebookAdsApi.init(access_token=page_access_token)

# Configura\u00e7\u00e3o da data
st.sidebar.divider()
start_date, end_date = date_range()
selected_range = date_range_for_ads()

# Bot\u00e3o de exporta\u00e7\u00e3o
export_button = st.sidebar.toggle("Export_Data")
if export_button:
    export_data(start_date, end_date)

try:
    # Buscar insights da p\u00e1gina
    page_insights = get_page_insights(page_id, start_date, end_date)
    
    if page_insights:
        # Processamento dos dados
        metrics_data = {
            'dates': [],
            'page_impressions': [],
            'page_views_total': [],
            'page_fan_adds': [],
            'page_fan_removes': [],
            'page_impressions_unique': [],
            'page_posts_impressions': [],
            'page_posts_impressions_unique': [],
            'page_fans': [],
            'page_impressions_paid': []
        }
        
        # Extrair dados dos insights
        for insight in page_insights:
            metric_name = insight['name']
            if metric_name in metrics_data:
                for value in insight['values']:
                    if metric_name == 'dates':
                        metrics_data['dates'].append(value['end_time'][:10])
                    else:
                        metrics_data[metric_name].append(value['value'])
        
        # Converter para DataFrame
        df = pd.DataFrame(metrics_data)
        
        # Layout do Dashboard
        st.title("Facebook Insights Dashboard")
        
        # Cards com m\u00e9tricas principais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            cards("Total Impress\u00f5es", df['page_impressions'].sum())
        with col2:
            cards("Visualiza\u00e7\u00f5es", df['page_views_total'].sum())
        with col3:
            cards("Novos F\u00e3s", df['page_fan_adds'].sum())
        with col4:
            cards("Impress\u00f5es \u00danicas", df['page_impressions_unique'].sum())
            
        st.divider()
        
        # Gr\u00e1ficos
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Impress\u00f5es ao Longo do Tempo")
            st.line_chart(df.set_index('dates')['page_impressions'])
            
        with col2:
            st.subheader("Visualiza\u00e7\u00f5es da P\u00e1gina")
            st.line_chart(df.set_index('dates')['page_views_total'])
            
        # M\u00e9tricas de Engajamento
        st.subheader("M\u00e9tricas de Engajamento")
        engagement_metrics = st.columns(2)
        with engagement_metrics[0]:
            st.metric("Taxa de Engajamento", 
                     f"{(df['page_fan_adds'].sum() / df['page_impressions'].sum() * 100):.2f}%")
        with engagement_metrics[1]:
            st.metric("Taxa de Reten\u00e7\u00e3o", 
                     f"{(1 - df['page_fan_removes'].sum() / df['page_fan_adds'].sum()) * 100:.2f}%")
        
        # Impress\u00f5es Org\u00e2nicas vs Pagas
        st.subheader("Impress\u00f5es Org\u00e2nicas vs Pagas")
        paid_organic_df = pd.DataFrame({
            'Data': df['dates'],
            'Impress\u00f5es Pagas': df['page_impressions_paid'],
            'Impress\u00f5es Org\u00e2nicas': df['page_impressions'] - df['page_impressions_paid']
        })
        st.line_chart(paid_organic_df.set_index('Data')[['Impress\u00f5es Pagas', 'Impress\u00f5es Org\u00e2nicas']])
        
        # Dados de An\u00fancios (se dispon\u00edveis)
        try:
            ads_data = facebook_ads_data_load(adaccount_id, selected_range)
            if ads_data:
                st.subheader("Performance dos An\u00fancios")
                st.dataframe(ads_data)
        except Exception as ads_error:
            st.warning(f"N\u00e3o foi poss\u00edvel carregar dados de an\u00fancios: {ads_error}")
            
    else:
        st.warning("Nenhum dado dispon\u00edvel para o per\u00edodo selecionado")

except Exception as e:
    st.error(f"Erro ao buscar dados do Facebook: {e}")


# Salvar o arquivo corrigido
with open('./alfa-main/pages/facebook_ads.py', 'w') as file:
    file.write(corrected_code)

print("Arquivo facebook_ads.py atualizado com as corre\u00e7\u00f5es necess\u00e1rias")
