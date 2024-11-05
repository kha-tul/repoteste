import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
import time
from pyecharts.charts import Pie
from pyecharts import options as opts
from math import ceil


def format_data_to_2_decimal_places(data):
    return [round(float(value), 2) for value in data]


def cpm_cpp_ctr_clicks(ads_details):   
    # Ensure data consistency by checking lengths
    ad_names     = ads_details['ad_name'].tolist()
    cpm          = format_data_to_2_decimal_places(ads_details['cpm'].tolist())
    cpp          = format_data_to_2_decimal_places(ads_details['cpp'].tolist())
    ctr          = format_data_to_2_decimal_places(ads_details['ctr'].tolist())
    clicks       = format_data_to_2_decimal_places(ads_details['clicks'].tolist())
    impressions  = format_data_to_2_decimal_places(ads_details['impressions'].tolist())
    reach        = format_data_to_2_decimal_places(ads_details['reach'].tolist())
    spend        = format_data_to_2_decimal_places(ads_details['spend'].tolist())
    social_spend = format_data_to_2_decimal_places(ads_details['social_spend'].tolist())

    options = {
        "title": {
            "subtext": "Insights por anúncios"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["CPM", "CPP", "CTR", "Cliques", "Impressões", "Alcançar", "Gastar", "Gastos sociais"]
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "15%",
            "containLabel": True
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {}
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": True,
            "data": ad_names,
            "axisLabel": {
                "rotate": 45,
                "interval": 0,
                "margin": 10,
            },
            "nameGap": 0  # Adjust this as needed
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": "CPM",
                "type": "line",
                "data": cpm
            },
            {
                "name": "CPP",
                "type": "line",
                "data": cpp
            },
            {
                "name": "CTR",
                "type": "line",
                "data": ctr
            },
            {
                "name": "Cliques",
                "type": "line",
                "data": clicks
            },
            {
                "name": "Impressões",
                "type": "line",
                "data": impressions
            },
            {
                "name": "Alcançar",
                "type": "line",
                "data": reach
            },
            {
                "name": "Gastar",
                "type": "line",
                "data": spend
            },
            {
                "name": "Gastos sociais",
                "type": "line",
                "data": social_spend
            },
        ]
    }
    st_echarts(options=options, height=400, width=1200)


def spend_on_ads(ads_details):
     
    # Ensure data consistency by checking lengths
    ad_names     = ads_details['ad_name'].tolist()
    spend        = format_data_to_2_decimal_places(ads_details['spend'].tolist())


    options = {
        "title": {
            "subtext": "Insights por anúncios"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["Gastar"]
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "15%",
            "containLabel": True
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {}
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": True,
            "data": ad_names,
            "axisLabel": {
                "rotate": 45,
                "interval": 0,
                "margin": 10,
            },
            "nameGap": 0  # Adjust this as needed
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": "Gastar",
                "type": "bar",
                "data": spend
            },
        ]
    }
    st_echarts(options=options, height=400, width=1200)

def roi_by_ad_names(ad_names, roi):
    # Convert pandas Series to lists if they are not already
    if isinstance(ad_names, pd.Series):
        ad_names = ad_names.tolist()
    if isinstance(roi, pd.Series):
        roi = roi.fillna(0)
        roi = roi.tolist()
    
    # Create data pairs
    data_pairs = [{"name": name, "value": value} for name, value in zip(ad_names, roi)]

    options = {
        "title": {
            "text": 'ROI por nomes de anúncios',
            "left": 'center',
            "top": 20,
            "textStyle": {
                "color": '#333',
                "fontSize": 20
            }
        },
        "tooltip": {
            "trigger": 'item',
            "formatter": '{b}: ({c}%)'
        },
        "legend": {
            "show": False,
            "orient": 'vertical',
            "left": 'left',
            "data": ad_names
        },
        "series": [
            {
                "name": 'ROI',
                "type": 'pie',
                "radius": ['40%', '70%'],
                "center": ['50%', '60%'],
                "data": data_pairs,
                "label": {
                    "show": False,
                    "formatter": '{b}\n ({c}%)',
                    "fontSize": 12,
                    "fontWeight": 'bold',
                    "color": '#000'
                },
                "labelLine": {
                    "show": False,
                    "smooth": 0.2,
                    "length": 10,
                    "length2": 10
                },
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": '#fff',
                    "borderWidth": 2,
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowOffsetY": 5,
                    "shadowColor": 'rgba(0, 0, 0, 0.5)'
                },
                "emphasis": {
                    "label": {
                        "show": False,
                        "fontSize": 14,
                        "fontWeight": 'bold',
                        "color": '#333'
                    }
                }
            }
        ]
    }
    st_echarts(options=options, height="300px", width="500px")

def ads_stacked_bar_chart(ad_names, roi, spend, conversions, selected_range):
    if isinstance(ad_names, pd.Series):
        ad_names = ad_names.tolist()
    if isinstance(roi, pd.Series):
        roi = roi.fillna(0)
        roi = roi.tolist()
    if isinstance(spend, pd.Series):
        spend = spend.tolist()
    if isinstance(conversions, pd.Series):
        conversions = conversions.tolist()

    # Filter the data based on spend value
    if selected_range == "last_month":
        filtered_data = [(name, r, round(s, 2), c) for name, r, s, c in zip(ad_names, roi, spend, conversions) if s > 20]
    elif selected_range == "last_28d" or selected_range == "last_30d":
        filtered_data = [(name, r, round(s, 2), c) for name, r, s, c in zip(ad_names, roi, spend, conversions) if s > 10]
    elif selected_range == "last_90d":
        filtered_data = [(name, r, round(s, 2), c) for name, r, s, c in zip(ad_names, roi, spend, conversions) if s > 60]
    elif selected_range == "this_year":
        filtered_data = [(name, r, round(s, 2), c) for name, r, s, c in zip(ad_names, roi, spend, conversions) if s > 500]
    elif selected_range == "last_year":
        filtered_data = [(name, r, round(s, 2), c) for name, r, s, c in zip(ad_names, roi, spend, conversions) if s > 300]
    elif selected_range == "last_quarter":
        filtered_data = [(name, r, round(s, 2), c) for name, r, s, c in zip(ad_names, roi, spend, conversions) if s > 200]
    else:
        filtered_data = [(name, r, round(s, 2), c) for name, r, s, c in zip(ad_names, roi, spend, conversions) if s > 3]

    # Check if there is any filtered data
    if filtered_data:
        filtered_ad_names, filtered_roi, filtered_spend, filtered_conversions = zip(*filtered_data)
    else:
        filtered_ad_names, filtered_roi, filtered_spend, filtered_conversions = [], [], [], []

    options = {
        "title": {
            "text": "Desempenho do anúncio",
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "legend": {
            "data": ["ROI", "Gastar", "Conversões"],
            "bottom": "bottom"
        },
        "xAxis": {
            "type": "category",
            "data": filtered_ad_names,
            "axisLabel": {
                # "rotate": 45,
                "interval": 0,  # Show all labels
                "fontSize": 9  # Decrease font size
            }
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": "ROI",
                "type": "bar",
                "stack": "total",
                "data": filtered_roi
            },
            {
                "name": "Gastar",
                "type": "bar",
                "stack": "total",
                "data": filtered_spend
            },
            {
                "name": "Conversões",
                "type": "bar",
                "stack": "total",
                "data": filtered_conversions
            }
        ]
    }
    st_echarts(options=options, height="400px", width="1300px")




def format_value(value):
    if value >= 1000000000000:
        return f"{value / 1000000000000:.2f}T"
    elif value >= 1000000000:
        return f"{value / 1000000000:.2f}B"
    elif value >= 1000000:
        return f"{value / 1000_000:.2f}M"
    elif value >= 1000:
        return f"{value / 1000:.2f}K"
    else:
        return f"{value:.2f}"


def total_roi_spend_conv_pie_charts(total_roi, total_spend, total_conversion):
    # Calculate the totals
    if isinstance(total_roi, pd.Series):
        total_roi = total_roi.fillna(0)
        total_roi = total_roi.tolist()
    if isinstance(total_spend, pd.Series):
        total_spend = total_spend.tolist()
    if isinstance(total_conversion, pd.Series):
        total_conversion = total_conversion.tolist()


    # Assuming the input should be the sum of the lists
    total_roi= round(sum(total_roi), 2)
    total_spend = round(sum(total_spend), 2)
    total_conversion = round(sum(total_conversion), 2)

    pie_data = [
        {"value": total_roi, "name": f"Total ROI {format_value(total_roi)}"},
        {"value": total_spend, "name": f"Total Spend {format_value(total_spend)}"},
        {"value": total_conversion, "name": f"Total Conversions {total_conversion}"}
    ]

    options = {
        "title": {
            "text": "Totais de desempenho de anúncios",
            "left": "center"
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{a} <br/>{c} ({d}%)"
        },
        "legend": {
            "bottom": "bottom",
            "data": ["Total ROI", "Total Spend", "Total Conversions"]
        },
        "series": [
            {
                "name": "Ad Performance",
                "type": "pie",
                "radius": ["20%", "80%"],
                "roseType": "area",  # Using area-based petals
                "data": pie_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                }
            }
        ]
    }
    st_echarts(options=options, height="300px", width="500px")