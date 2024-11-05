import streamlit as st
import pandas as pd
from facebook_business.api import FacebookAdsApi

from logics.fetch_facebook import *
from logics.date_range import *

from plots.plots_facebook import *
from plots.cards import *
from plots.plots_ads_account import *
from logics.fetch_adaccounts import *
from logics.date_range import *


from logics.load_data import facebook_api_data_load
from logics.load_data import facebook_ads_data_load

from logics.utilis import facebook_apis_tokens

from logics.export_data import export_data

st.sidebar.page_link("main.py", label="Overview", icon="🏠")
st.sidebar.page_link("pages/Google_Ads_Performance.py",       label="Google",       icon="👥", disabled=False)
st.sidebar.page_link("pages/facebook_ads.py",                 label="Facebook",     icon="👥", disabled=False)
st.sidebar.page_link("pages/instagram_data.py",               label="Instagram",    icon="👥", disabled=False)


(page_access_token, user_access_token, 
 page_id, adaccount_account_id, adaccount_id) = facebook_apis_tokens()

# Initialize the Facebook API
FacebookAdsApi.init(access_token= page_access_token)

st.sidebar.divider()
start_date, end_date = date_range()
selected_range       = date_range_for_ads()

export_button = st.sidebar.toggle("Export_Data")
if export_button:
    export_data(start_date, end_date)


try:
    (page_insights, dates, page_post_engagements, page_impressions, page_impressions_unique, 
     page_fans, unique_page_fan, page_follows, page_views, 
     page_negative_feedback_unique, page_impressions_viral, 
     page_fan_adds_by_paid_non_paid_unique, page_daily_follows_unique, 
     page_daily_unfollows_unique, page_impressions_by_age_gender_unique, 
     page_impressions_organic_unique_v2, page_impressions_paid, post_reactions, 
     page_fans_country, page_fan_adds, page_fan_removes)  = facebook_api_data_load(page_id, start_date, end_date)


    ads_insights_, ada_account =  facebook_ads_data_load(user_access_token, adaccount_account_id, adaccount_id, selected_range)
    ads_insights  = pd.DataFrame(ads_insights_)

    group_ads_details = group_by_ad_name(ads_insights)
    group_ads_details['roi'] = round((group_ads_details['conversions'] / group_ads_details['spend']) * 100,2) # Calculate ROI
    ad_names    = group_ads_details['ad_name']
    roi         = group_ads_details['roi']
    spend       = group_ads_details['spend']
    conversions = group_ads_details['conversions']


    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        title = "Total de Visualizações de Página"
        cards(title , page_views.sum()[0])

    with col2:
        title = "Total de Seguidores"
        cards(title , page_follows.sum()[0])
    with col3:
        title = "Total de Curtidas"
        cards(title , unique_page_fan)
    with col4:
        title = "Feedbacks Negativos"
        cards(title , page_negative_feedback_unique.sum()[0])
    with col5:
        title = "Impressões Virais"
        cards(title , page_impressions_viral.sum()[0])


    st.divider()

    if page_insights:
        page_impression_engagement(page_post_engagements, page_impressions, page_impressions_unique, dates)

        col1, col2 = st.columns([1,1])
        with col1:
            page_fan_adds_by_paid_unpaid_unique(page_fan_adds_by_paid_non_paid_unique, dates)
        with col2:
            page_daily_follows_unfollow(page_daily_follows_unique, page_daily_unfollows_unique, dates)

        try:
            col1, col2 = st.columns([1,1])
            with col1:
                page_impressions_by_age_gender_male(page_impressions_by_age_gender_unique, dates)
            with col2:
                page_impressions_by_age_gender_female(page_impressions_by_age_gender_unique, dates)
        except:
            pass

        page_impressions_organic_paid(page_impressions_organic_unique_v2, page_impressions_paid,  dates)
        st.divider()

        col1, col2 = st.columns([1,1])
        with col1:
            page_fans_country_plot(page_fans_country, dates)
        with col2:
            page_actions_post_reactions(post_reactions, dates)
        
        page_fan_adds_remove(page_fan_adds,page_fan_removes, dates)

        st.divider()

        try:
            cpm_cpp_ctr_clicks(group_ads_details)
            spend_on_ads(group_ads_details)

            col1, col2 = st.columns([1,1])
            with col1:
                roi_by_ad_names(ad_names, roi)
            with col2:
                total_roi_spend_conv_pie_charts(roi, spend, conversions)
                

            ads_stacked_bar_chart(ad_names, roi, spend, conversions, selected_range)
        except:
            pass

    else:
        st.write("No insights data available")

except Exception as e:
    st.error(f"Error fetching page insights: {e}")

except:
    st.warning("No Data Found for selected range")