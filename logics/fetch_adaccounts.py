import streamlit as st
import pandas as pd
import requests


def get_ad_accounts(access_token,specific_account_id):
    url = f"https://graph.facebook.com/v17.0/me/adaccounts"
    params = {
        'access_token': access_token,
        'fields': '''account_id,
                    amount_spent,age,funding_source_details,
                    min_campaign_group_spend_cap,min_daily_budget,
                    business_name,campaigns''',

        'level': 'ad',  # Set the level to 'ad', 'campaign', 'account', etc.
        'date_preset': 'last_14d',  # Set the date preset (e.g., 'today', 'yesterday', 'last_7d', 'last_30d', etc.)
        'time_range': {  # Set a custom time range (optional, overrides date_preset)
            'since': '2024-07-01',
            'until': '2024-07-11'
        }
    }
    response = requests.get(url, params=params)
    data = response.json()
    specific_account_data = [account for account in data['data'] if account['account_id'] == specific_account_id]
    return specific_account_data


def get_insights_from_ada_account(access_token, ad_account_id, selected_range):
    url = f"https://graph.facebook.com/v17.0/{ad_account_id}/insights"
    params = {
        'access_token': access_token,
        'level': 'ad',
        'date_preset': selected_range,
        'fields': '''date_start,date_stop,reach,
                    impressions,spend,social_spend,cpm,
                    cpp,ctr,clicks,ad_name,conversion_values,conversions''',
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


def group_by_ad_name(ads_insights):
    # Convert relevant columns to numeric, handling non-numeric gracefully
    numeric_columns = ['spend', 'social_spend', 'reach', 'impressions', 'cpm', 'cpp', 'ctr', 'clicks', 'conversions']
    ads_insights[numeric_columns] = ads_insights[numeric_columns].apply(pd.to_numeric, errors='coerce')
    # Group by 'ad_name' and sum the numeric values
    ads_insights = ads_insights.groupby('ad_name', as_index=False)[numeric_columns].sum()
    return ads_insights