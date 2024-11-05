import streamlit as st
from datetime import datetime, timedelta

def date_range():
    options = ["Últimos 10 dias", "Últimos 5 Dias", "Últimos 7 Dias", "Últimos 15 dias", "Últimos 20 dias", "Últimos 28 dias", "Últimos 2 meses", "Last 3 Months","Last 4 Months",
               "Últimos 5 meses","Últimos 6 meses","Últimos 7 meses","Últimos 8 meses","Últimos 9 meses","Últimos 10 meses",
               "Últimos 11 meses","Últimos 12 meses"]
    selected_option = st.sidebar.selectbox("Escolha uma Opção:", options, key="date_range")

    if selected_option == "Últimos 10 dias":
        selected_days = 10
    elif selected_option == "Últimos 5 Dias":
        selected_days = 5
    elif selected_option == "Últimos 7 Dias":
        selected_days = 7
    elif selected_option == "Últimos 15 dias":
        selected_days = 15
    elif selected_option == "Últimos 20 dias":
        selected_days = 20
    elif selected_option == "Últimos 28 dias":
        selected_days = 28
    elif selected_option == "Últimos 2 meses":
        selected_days = 60
    elif selected_option == "Últimos 3 meses":
        selected_days = 90
    elif selected_option == "Últimos 4 meses":
        selected_days = 120
    elif selected_option == "Últimos 5 meses":
        selected_days = 150
    elif selected_option == "Últimos 6 meses":
        selected_days = 180
    elif selected_option == "Últimos 7 meses":
        selected_days = 210
    elif selected_option == "Últimos 8 meses":
        selected_days = 240
    elif selected_option == "Últimos 9 meses":
        selected_days = 270
    elif selected_option == "Últimos 10 meses":
        selected_days = 300
    elif selected_option == "Últimos 11 meses":
        selected_days = 330
    elif selected_option == "Últimos 12 meses":
        selected_days = 360
    
    end_date = datetime.today()
    start_date = end_date - timedelta(days=selected_days)

    selected_dates = st.sidebar.date_input(
        "Selecionar Intervalo de Datas",
        value=(start_date, end_date),
        max_value=end_date,
        key="selected_date"
    )

    return selected_dates

def date_range_for_ads():
    options = ['hoje', 'ontem', 'este mês', 'mês passado', 
               'este_trimestre', 'último_3d', 
               'último_7d', 'último_14d', 'último_28d', 'último_30d', 'último_90d', 
               'última_semana_mon_dom', 'última_semana_dom_sáb', 
               'Ultimo quarto', 'ano passado', 'esta_semana_segunda_hoje', 
               'esta_semana_sol_hoje', 'este ano']
    
    selected_option = st.sidebar.selectbox("Escolha o intervalo para anúncios:", options)
    if selected_option == "hoje":
        selected_values = "today"
    elif selected_option == "ontem":
        selected_values = "yesterday"
    elif selected_option == "este mês":
        selected_values = "this_month"
    elif selected_option == "mês passado":
        selected_values = "last_month"
    elif selected_option == "este_trimestre":
        selected_values = "this_quarter"


    elif selected_option == "último_3d":
        selected_values = "last_3d"
    elif selected_option == "último_7d":
        selected_values = "last_7d"
    elif selected_option == "último_14d":
        selected_values = "last_14d"
    elif selected_option == "último_28d":
        selected_values = "last_28d"
    elif selected_option == "último_30d":
        selected_values = "last_30d"
    elif selected_option == "último_90d":
        selected_values = "last_90d"

    elif selected_option == "última_semana_mon_dom":
        selected_values = "last_week_mon_sun"
    elif selected_option == "última_semana_dom_sáb":
        selected_values = "last_week_sun_sat"
    elif selected_option == "Ultimo quarto":
        selected_values = "last_quarter"
    elif selected_option == "ano passado":
        selected_values = "last_year"
    elif selected_option == "esta_semana_segunda_hoje":
        selected_values = "this_week_mon_today"
    elif selected_option == "esta_semana_sol_hoje":
        selected_values = "this_week_sun_today"     
    elif selected_option == "este ano":
        selected_values = "this_year"

    return selected_values
