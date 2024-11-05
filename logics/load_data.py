from pages.User_Engagement_and_Activity import *

import pandas as pd

from logics.fetch_facebook import get_page_insights
from logics.date_range import datetime
from logics.fetch_google_analytics_data import fetch_data


from logics.fetch_adaccounts import *

from logics.utilis import instagram_api_data_fetch
from logics.fetch_instagram import fetch_instagram_insights, fetch_instagram_insights_with_total_values


def google_api_data_load(start_date, end_date, client, property_id):
    dimensions_total = []
    metrics_total    = ['totalUsers', 'totalRevenue', 'averagePurchaseRevenue']
    total_data_ = fetch_data(client, property_id, dimensions_total, metrics_total, str(start_date), str(end_date))

    selected_dimensions = ['date','dayOfWeek','month','campaignName']
    selected_metrics    = ['advertiserAdClicks', 'advertiserAdImpressions', 'advertiserAdCost', 'advertiserAdCostPerClick',
                        'returnOnAdSpend']
    data_       = fetch_data(client, property_id, selected_dimensions, selected_metrics, str(start_date), str(end_date))

    return data_, total_data_



def google_analytics_data_load(client, property_id, start_date, end_date):
    selected_dimensions = ['date','dayOfWeek','operatingSystem', 'browser', 'deviceCategory', 'country', 'continent', 'sessionSourceMedium']
    selected_metrics    = ['sessions', 'engagedSessions','averageSessionDuration','engagementRate',
                            'bounceRate', 'eventCount', 'dauPerMau','wauPerMau', 'screenPageViews']

    rose_pie_dimensions = ['source']
    rose_pie_metrics    = ['activeUsers', 'totalUsers']

    eventCount_dimensions = ['eventName']
    eventCount_metrics    = ['eventCount', 'eventCountPerUser']

    sunbrust_dimensions = ['operatingSystem', 'browser', 'deviceCategory']
    sunbrust_metrics    = ['sessions']

    data_            = fetch_data(client, property_id, selected_dimensions, selected_metrics, str(start_date), str(end_date))
    rose_pie_data_   = fetch_data(client, property_id, rose_pie_dimensions, rose_pie_metrics, str(start_date), str(end_date))
    eventCount_data_ = fetch_data(client, property_id, eventCount_dimensions, eventCount_metrics, str(start_date), str(end_date))
    sunbrust_data_   = fetch_data(client, property_id, sunbrust_dimensions, sunbrust_metrics, str(start_date), str(end_date))

    return data_, rose_pie_data_, eventCount_data_, sunbrust_data_


def facebook_ads_data_load(user_access_token, adaccount_account_id, adaccount_id, selected_range):
    ada_account  = get_ad_accounts(user_access_token, adaccount_account_id)
    ads_insights = get_insights_from_ada_account(user_access_token, adaccount_id, selected_range)

    ads_insights = [{
        'ad_name': ad.get('ad_name'),
        'spend': ad.get('spend'),
        'social_spend': ad.get('social_spend'),
        'reach': ad.get('reach'),
        'impressions': ad.get('impressions'),
        'cpm': ad.get('cpm'),
        'cpp': ad.get('cpp'),
        'ctr': ad.get('ctr'),
        'clicks': ad.get('clicks'),
        'conversion_values': ad.get('conversion_values'),
        'conversions': sum(int(conv.get('value', 0)) for conv in ad.get('conversions', [])),
    } for ad in ads_insights['data'] if 'ad_name' in ad]

    return ads_insights, ada_account



def facebook_api_data_load(page_id, start_date, end_date):
    page_insights = get_page_insights(page_id, str(start_date), str(end_date))
    dates = [datetime.strptime(page_insights[0]["values"][i]["end_time"][:10], "%Y-%m-%d").strftime("%Y-%m-%d") for i in range(len(page_insights[0]["values"]))]

    page_post_engagements                 = [data["value"] for data in page_insights[0]["values"]]
    page_impressions                      = [data["value"] for data in page_insights[1]["values"]]
    page_impressions_unique               = [data["value"] for data in page_insights[2]["values"]]

    page_fans                             = [data["value"] for data in page_insights[3]["values"]]
    unique_page_fan                       = list(set(page_fans))[0]

    page_follows                          = [data["value"] for data in page_insights[4]["values"]]
    page_follows                          = pd.DataFrame(page_follows)

    page_views                            = [data["value"] for data in page_insights[5]["values"]]
    page_views                            = pd.DataFrame(page_views)

    page_negative_feedback_unique         = [data["value"] for data in page_insights[6]["values"]]
    page_negative_feedback_unique         = pd.DataFrame(page_negative_feedback_unique)

    page_impressions_viral                = [data["value"] for data in page_insights[7]["values"]]
    page_impressions_viral                = pd.DataFrame(page_impressions_viral)

    page_fan_adds_by_paid_non_paid_unique = [data["value"] for data in page_insights[8]["values"]]
    page_fan_adds_by_paid_non_paid_unique = pd.DataFrame(page_fan_adds_by_paid_non_paid_unique)

    page_daily_follows_unique             = [data["value"] for data in page_insights[9]["values"]]
    page_daily_follows_unique             = pd.DataFrame(page_daily_follows_unique)

    page_daily_follows_unique             = [data["value"] for data in page_insights[9]["values"]]
    page_daily_unfollows_unique           = [data["value"] for data in page_insights[10]["values"]]

    page_impressions_by_age_gender_unique = [data["value"] for data in page_insights[11]["values"]]
    page_impressions_by_age_gender_unique = pd.DataFrame(page_impressions_by_age_gender_unique)

    page_impressions_organic_unique_v2    = [data["value"] for data in page_insights[12]["values"]]
    page_impressions_paid                 = [data["value"] for data in page_insights[13]["values"]]
    post_reactions                        = [data["value"] for data in page_insights[14]["values"]]
    page_fans_country                     = [data["value"] for data in page_insights[15]["values"]]
    page_fan_adds                         = [data["value"] for data in page_insights[16]["values"]]
    page_fan_removes                      = [data["value"] for data in page_insights[17]["values"]]


    return page_insights, dates, page_post_engagements, page_impressions, page_impressions_unique, page_fans, unique_page_fan, page_follows, page_views, page_negative_feedback_unique, page_impressions_viral, page_fan_adds_by_paid_non_paid_unique, page_daily_follows_unique, page_daily_unfollows_unique, page_impressions_by_age_gender_unique, page_impressions_organic_unique_v2, page_impressions_paid, post_reactions, page_fans_country, page_fan_adds, page_fan_removes


def instagram_data_load(instagram_user_id, access_token, start_date, end_date):

    metrics, period, lifetime = instagram_api_data_fetch()

    ig_insights = fetch_instagram_insights(instagram_user_id, access_token, start_date, end_date, metrics, period, lifetime)
    dates_data   = ig_insights['data'][0]
    dates = [datetime.strptime(data["end_time"][:10], "%Y-%m-%d").strftime("%Y-%m-%d") for data in dates_data["values"]]
    
    ig_insights_by_total_values = fetch_instagram_insights_with_total_values(instagram_user_id, access_token)
    ig_insights_by_total_values = ig_insights_by_total_values['data'][0]
    ig_insights_by_total_values = pd.DataFrame(ig_insights_by_total_values)

    impressions_values    = [data["value"] for data in ig_insights['data'][0]["values"]]
    reach_values          = [data["value"] for data in ig_insights['data'][1]["values"]]
    profile_views_values  = [data["value"] for data in ig_insights['data'][2]["values"]]
    follower_count_values = [data["value"] for data in ig_insights['data'][3]["values"]]

    email_contacts        = [data["value"] for data in ig_insights['data'][4]["values"]]
    phone_call_clicks     = [data["value"] for data in ig_insights['data'][5]["values"]]
    text_message_clicks   = [data["value"] for data in ig_insights['data'][6]["values"]]
    get_directions_clicks = [data["value"] for data in ig_insights['data'][7]["values"]]
    website_clicks        = [data["value"] for data in ig_insights['data'][8]["values"]]


    return dates,  ig_insights_by_total_values, impressions_values, reach_values, profile_views_values, follower_count_values, email_contacts, phone_call_clicks, text_message_clicks, get_directions_clicks, website_clicks