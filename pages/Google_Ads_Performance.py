import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import datetime, timedelta
from logics.fetch_google_analytics_data import *
from logics.date_range import *
from plots.plots_Google_Ads_Performance import *
from plots.cards import *
import os
from dotenv import load_dotenv
from logics.utilis import load_google_api


from logics.load_data import google_api_data_load
from logics.export_data import export_data


st.sidebar.page_link("main.py", label="Overview", icon="🏠")
st.sidebar.page_link("pages/Google_Ads_Performance.py",       label="Google",       icon="👥", disabled=False)
st.sidebar.page_link("pages/facebook_ads.py",                 label="Facebook",     icon="👥", disabled=False)
st.sidebar.page_link("pages/instagram_data.py",               label="Instagram",    icon="👥", disabled=False)

st.sidebar.divider()
start_date, end_date = date_range()



export_button = st.sidebar.toggle("Export_Data")
if export_button:
    export_data(start_date, end_date)







try:
    client, property_id, dimensions, metrics = load_google_api()
    data_, total_data_ = google_api_data_load(start_date, end_date, client, property_id)

    data       = pd.DataFrame(data_)
    total_data = pd.DataFrame(total_data_)

    data['date']      = pd.to_datetime(data['date'], format='%Y%m%d')
    data['date']      = data['date'].dt.strftime('%Y-%m-%d')
    data['dayOfWeek'] = pd.to_datetime(data['date']).dt.day_name()
    data['month']     = pd.to_datetime(data['date']).dt.month_name()

    total_compaigns        = data['campaignName'].nunique()
    returnOnAdSpend_Values = data['returnOnAdSpend']
    

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        title = "Total de Usuários"
        cards(title , int(total_data['totalUsers'].nunique()))
    with col2:
        title = "Total de Campanhas"
        cards(title , total_compaigns)
    with col3:
        title = "Retorno sobre Investimento em Anúncios"
        cards(title , int(returnOnAdSpend_Values.sum()))
    with col4:
        title = "Receita Total"
        cards(title , int(total_data['totalRevenue'].nunique()))
    with col5:
        title = "Receita Média por Compra"
        cards(title , int(total_data['averagePurchaseRevenue'].nunique()))    
    st.divider()
    google_ads_impressions_clicks(data)
    google_ads_cost_perclick(data)
    st.divider()
    col1, col2 = st.columns([1,1])
    with col1:
        advertiserAdCostPerClick(data)
    with col2:
        returnOnAdSpend(data)
except Exception as e:
    st.error(f"Error fetching data: {e}")


