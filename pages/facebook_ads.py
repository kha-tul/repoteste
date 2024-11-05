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
st.sidebar.page_link("pages/Google_Ads_Performance.py", label="Google", icon="\ud83d\udcca")
st.sidebar.page_link("pages/facebook_ads.py", label="Facebook", icon="\ud83d\udcf1")
st.sidebar.page_link("pages/instagram_data.py", label="Instagram", icon="\ud83d\udcf8")

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
    # Carregar dados do Facebook
    (page_insights, dates, page_post_engagements, page_impressions, 
     page_impressions_unique, page_fans, unique_page_fan, page_follows, 
     page_views, page_negative_feedback_unique, page_impressions_viral,
     page_fan_adds_by_paid_non_paid_unique, page_daily_follows_unique,
     page_daily_unfollows_unique, page_impressions_by_age_gender_unique,
     page_impressions_organic_unique_v2, page_impressions_paid, post_reactions,
     page_fans_country, page_fan_adds, page_fan_removes) = facebook_api_data_load(page_id, start_date, end_date)

    # Carregar dados de an\u00fancios
    try:
        (group_ads_details, ad_names, roi, spend, 
         conversions) = facebook_ads_data_load(adaccount_id, selected_range)
    except Exception as ads_error:
        st.warning(f"N\u00e3o foi poss\u00edvel carregar dados de an\u00fancios: {str(ads_error)}")
        group_ads_details, ad_names, roi, spend, conversions = None, None, None, None, None

    # Layout do Dashboard
    st.title("Facebook Insights")

    # Cards com m\u00e9tricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        title = "Engajamento"
        cards(title, page_post_engagements.sum()[0])
    with col2:
        title = "Impress\u00f5es"
        cards(title, page_impressions.sum()[0])
    with col3:
        title = "F\u00e3s"
        cards(title, page_fans.iloc[-1][0])
    with col4:
        title = "Impress\u00f5es Virais"
        cards(title, page_impressions_viral.sum()[0])

    st.divider()

    # Gr\u00e1ficos de m\u00e9tricas
    if page_insights:
        page_impression_engagement(page_post_engagements, page_impressions, 
                                 page_impressions_unique, dates)

        col1, col2 = st.columns([1,1])
        with col1:
            page_fan_adds_by_paid_unpaid_unique(page_fan_adds_by_paid_non_paid_unique, dates)
        with col2:
            page_daily_follows_unfollow(page_daily_follows_unique, 
                                      page_daily_unfollows_unique, dates)

        try:
            col1, col2 = st.columns([1,1])
            with col1:
                page_impressions_by_age_gender_male(page_impressions_by_age_gender_unique, dates)
            with col2:
                page_impressions_by_age_gender_female(page_impressions_by_age_gender_unique, dates)
        except:
            st.warning("Dados demogr\u00e1ficos n\u00e3o dispon\u00edveis")

        page_impressions_organic_paid(page_impressions_organic_unique_v2, 
                                    page_impressions_paid, dates)
        st.divider()

        col1, col2 = st.columns([1,1])
        with col1:
            page_fans_country_plot(page_fans_country, dates)
        with col2:
            page_actions_post_reactions(post_reactions, dates)
        
        page_fan_adds_remove(page_fan_adds, page_fan_removes, dates)

        st.divider()

        # Dados de An\u00fancios
        if group_ads_details is not None:
            try:
                cpm_cpp_ctr_clicks(group_ads_details)
                spend_on_ads(group_ads_details)

                col1, col2 = st.columns([1,1])
                with col1:
                    roi_by_ad_names(ad_names, roi)
                with col2:
                    total_roi_spend_conv_pie_charts(roi, spend, conversions)
                
                ads_stacked_bar_chart(ad_names, roi, spend, conversions, selected_range)
            except Exception as e:
                st.warning(f"Erro ao exibir m\u00e9tricas de an\u00fancios: {str(e)}")

    else:
        st.warning("Nenhum dado dispon\u00edvel para o per\u00edodo selecionado")

except Exception as e:
    st.error(f"Erro ao carregar dados do Facebook: {str(e)}")


# Salvar o arquivo corrigido
with open('./alfa-main/pages/facebook_ads.py', 'w') as file:
    file.write(corrected_code)

print("Arquivo facebook_ads.py atualizado com as corre\u00e7\u00f5es necess\u00e1rias. Principais mudan\u00e7as:")
print("1. Corrigidos os \u00edcones do menu lateral")
print("2. Mantida a estrutura original de carregamento de dados")
print("3. Melhorado o tratamento de erros")
print("4. Mantidos os gr\u00e1ficos e visualiza\u00e7\u00f5es originais")
print("5. Adicionadas mensagens de aviso mais informativas")
