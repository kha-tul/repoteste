import streamlit as st
import pandas as pd

from logics.fetch_google_analytics_data import *

from pages.Google_Ads_Performance import google_api_data_load
from pages.facebook_ads import facebook_api_data_load




def export_data(start_date, end_date):
    page_id              = st.secrets["facebook"]["page_id"]

    # GOOGLE ADS
    google_ads_data_, total_google_ads_data_ = google_api_data_load()
    google_ads_data       = pd.DataFrame(google_ads_data_)


    # GOOGLE ANALYTICS
    google_analytics_dimensions = ['date','dayOfWeek','operatingSystem', 'browser', 'deviceCategory', 'country', 'continent', 'sessionSourceMedium']
    google_analytics_metrics    = ['sessions', 'engagedSessions','averageSessionDuration','engagementRate',
                                    'bounceRate', 'eventCount', 'dauPerMau','wauPerMau', 'screenPageViews']
    google_analytics_           = fetch_data(client, property_id, google_analytics_dimensions, google_analytics_metrics, str(start_date), str(end_date))
    google_analytics            = pd.DataFrame(google_analytics_)

    # FACEBOOK DATA
    (page_insights, dates, page_post_engagements, page_impressions, page_impressions_unique, 
     page_fans, unique_page_fan, page_follows, page_views, 
     page_negative_feedback_unique, page_impressions_viral, 
     page_fan_adds_by_paid_non_paid_unique, page_daily_follows_unique, 
     page_daily_unfollows_unique, page_impressions_by_age_gender_unique, 
     page_impressions_organic_unique_v2, page_impressions_paid, post_reactions, 
     page_fans_country, page_fan_adds, page_fan_removes)  = facebook_api_data_load(page_id)

    facebook_data_dictionary = {                            
                            'dates': dates,
                            'page_post_engagements':              page_post_engagements,
                            'page_impressions':                   page_impressions,
                            'page_impressions_unique':            page_impressions_unique,
                            'page_fans':                          page_fans,
                            'page_daily_follows_unique':          page_daily_follows_unique,
                            'page_daily_unfollows_unique':        page_daily_unfollows_unique,
                            'page_impressions_organic_unique_v2': page_impressions_organic_unique_v2,
                            'page_impressions_paid ':             page_impressions_paid ,
                            'post_reactions':                     post_reactions ,
                            'page_fan_adds':                      page_fan_adds,
                            'page_fan_removes':                   page_fan_removes,
                        }
    facebook_dictionary     = pd.DataFrame(facebook_data_dictionary)
    page_fans_country_data  = pd.DataFrame(page_fans_country)
    combine_facebook_data   = pd.concat([facebook_dictionary, 
                                       page_follows, page_views,
                                       page_negative_feedback_unique, page_impressions_viral,
                                       page_fan_adds_by_paid_non_paid_unique,
                                       page_impressions_by_age_gender_unique,
                                       page_fans_country_data], axis=1)




    with pd.ExcelWriter('Export/Export_Data.xlsx') as writer:
        combine_facebook_data.to_excel(writer, sheet_name='Facebook', index=False)
        google_ads_data.to_excel(writer, sheet_name='Google Ads', index=False)
        google_analytics.to_excel(writer, sheet_name='Google Anaytics', index=False)
    st.sidebar.success("Data Export Successfully")








# def export_data(combine_facebook_data, ads_insights):
#     pass
    # combine_facebook_data = pd.DataFrame(combine_facebook_data)
    # st.write(combine_facebook_data)
    
    # ads_insights = pd.DataFrame(ads_insights)
    # st.write(ads_insights)

    # # Save both dataframes in one Excel file in separate sheets
    # with pd.ExcelWriter('Export/facebook_data.xlsx') as writer:
    #     combine_facebook_data.to_excel(writer, sheet_name='Combine Facebook Data', index=False)
    #     ads_insights.to_excel(writer, sheet_name='Ads Insights', index=False)