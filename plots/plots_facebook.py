import streamlit as st
import pandas as pd
import plotly.express as px
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType
from streamlit_echarts import st_pyecharts
from streamlit_echarts import st_echarts
from datetime import datetime, timedelta

from logics.fetch_facebook import *

def page_impression_engagement(page_post_engagements, page_impressions, page_impressions_unique, dates):
    options = {
        "title": {
            "subtext": "Insights da Página"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["Engajamentos com Publicações", "Total de Impressões", "Alcance Total"]
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {}
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": dates
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": "Engajamentos com Publicações",
                "type": "line",
                "data": page_post_engagements
            },
            {
                "name": "Total de Impressões",
                "type": "line",
                "data": page_impressions
            },
            {
                "name": "Alcance Total",
                "type": "line",
                "data": page_impressions_unique
            },
        ]
    }
    st_echarts(options=options, height=400, width=1350)



def page_fan_adds_by_paid_unpaid_unique(page_fan_adds_by_paid_non_paid_unique, dates):
    total_page_fan_adds     = page_fan_adds_by_paid_non_paid_unique['total'].tolist()
    page_fan_adds_by_paid   = page_fan_adds_by_paid_non_paid_unique['paid'].tolist()
    page_fan_adds_by_unpaid = page_fan_adds_by_paid_non_paid_unique['unpaid'].tolist()

    # Echarts options
    options = {
        "title": {
            "subtext": "Fãs da Página"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["Total de Fãs da Página", "Fãs Pagos da Página", "Fãs Orgânicos da Página"],
            # "top": "left",
            "top": "0%",  # Position the legend at the bottom
            "padding": [0, 0, 0, 0] # Top, Right, Bottom, Left
        },
        "grid": {
            "left": "0%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {}
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": dates
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": "Total de Fãs da Página",
                "type": "line",
                "data": total_page_fan_adds
            },
            {
                "name": "Fãs Pagos da Página",
                "type": "line",
                "data": page_fan_adds_by_paid
            },
            {
                "name": "Fãs Orgânicos da Página",
                "type": "line",
                "data": page_fan_adds_by_unpaid
            },
        ]
    }
    st_echarts(options=options, height=400, width=700)



def page_daily_follows_unfollow(page_daily_follows_unique, page_daily_unfollows_unique, dates):
    options = {
        "title": {
            "subtext": "Seguidores & Deixaram de Seguir"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["Seguidores", "Deixaram de Seguir"]
        },
        "grid": {
            "left": "2%",
            "right": "4%",
            "bottom": "3%",
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
            "data": dates
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": "Seguidores",
                "type": "bar",
                "data": page_daily_follows_unique,
                "barGap": '50%',  # Adjust the gap between bars
                "barCategoryGap": '70%',  # Adjust the gap between categories
            },
            {
                "name": "Deixaram de Seguir",
                "type": "bar",
                "data": page_daily_unfollows_unique,
                "barGap": '50%',  # Adjust the gap between bars
                "barCategoryGap": '70%',  # Adjust the gap between categories
            },
        ]
    }
    st_echarts(options=options, height=400, width=700)


def get_or_add_column_data(df, column_name):
    if column_name not in df.columns:
        df[column_name] = [0] * len(df)
    return df[column_name].tolist()

def ensure_length(lst, length):
    return lst + [0] * (length - len(lst))

def page_impressions_by_age_gender_male(page_impressions_by_age_gender_unique, dates):
    page_impressions_by_age_gender_unique = pd.DataFrame(page_impressions_by_age_gender_unique)
    page_impressions_by_age_gender_unique.fillna(0, inplace=True)
 
    male_18_24   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'M.18-24'), 4)
    male_25_34   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'M.25-34'), 4)
    male_35_44   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'M.35-44'), 4)
    male_45_54   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'M.45-54'), 4)
    male_55_64   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'M.55-64'), 4)
    male_55_plus = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'M.65+'), 4)

    options = {
        "title": {
            "subtext": "Impressão do público masculino nos últimos 5 dias"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "grid": {
            "left": "0%",
            "right": "0%",
            "bottom": "0%",
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
            "data": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": dates[-1],
                "type": "bar",
                "stack": "total",
                "data": [male_18_24[-1], male_25_34[-1], male_35_44[-1], male_45_54[-1], male_55_64[-1], male_55_plus[-1]]
            },
            {
                "name": dates[-2],
                "type": "bar",
                "stack": "total",
                "data": [male_18_24[-2], male_25_34[-2], male_35_44[-2], male_45_54[-2], male_55_64[-2], male_55_plus[-2]]
            },
            {
                "name": dates[-3],
                "type": "bar",
                "stack": "total",
                "data": [male_18_24[-3], male_25_34[-3], male_35_44[-3], male_45_54[-3], male_55_64[-3], male_55_plus[-3]]
            },
            {
                "name": dates[-4],
                "type": "bar",
                "stack": "total",
                "data": [male_18_24[-4], male_25_34[-4], male_35_44[-4], male_45_54[-4], male_55_64[-4], male_55_plus[-4]]
            },
            {
                "name": dates[-5],
                "type": "bar",
                "stack": "total",
                "data": [male_18_24[-5], male_25_34[-5], male_35_44[-5], male_45_54[-5], male_55_64[-5], male_55_plus[-5]]
            },
        ]
    }
    st_echarts(options=options, height=400, width=500)




def page_impressions_by_age_gender_female(page_impressions_by_age_gender_unique, dates):
    page_impressions_by_age_gender_unique = pd.DataFrame(page_impressions_by_age_gender_unique)
    page_impressions_by_age_gender_unique.fillna(0, inplace=True)

    female_18_24   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'F.18-24'), 4)
    female_25_34   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'F.25-34'), 4)
    female_35_44   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'F.35-44'), 4)
    female_45_54   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'F.45-54'), 4)
    female_65_plus = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'F.65+'), 4)
    female_55_64   = ensure_length(get_or_add_column_data(page_impressions_by_age_gender_unique, 'F.55-64'), 4)

    options = {
        "title": {
            "subtext": "Impressão do público feminino nos últimos 5 dias"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "grid": {
            "left": "0%",
            "right": "0%",
            "bottom": "0%",
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
            "data": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": dates[-1],
                "type": "bar",
                "stack": "total",
                "data": [female_18_24[-1], female_25_34[-1], female_35_44[-1], female_45_54[-1], female_55_64[-1], female_65_plus[-1]]
            },
            {
                "name": dates[-2],
                "type": "bar",
                "stack": "total",
                "data": [female_18_24[-2], female_25_34[-2], female_35_44[-2], female_45_54[-2], female_55_64[-2], female_65_plus[-2]]
            },
            {
                "name": dates[-3],
                "type": "bar",
                "stack": "total",
                "data": [female_18_24[-3], female_25_34[-3], female_35_44[-3], female_45_54[-3], female_55_64[-3], female_65_plus[-3]]
            },
            {
                "name": dates[-4],
                "type": "bar",
                "stack": "total",
                "data": [female_18_24[-4], female_25_34[-4], female_35_44[-4], female_45_54[-4], female_55_64[-4], female_65_plus[-4]]
            },
            {
                "name": dates[-5],
                "type": "bar",
                "stack": "total",
                "data": [female_18_24[-5], female_25_34[-5], female_35_44[-5], female_45_54[-5], female_55_64[-5], female_65_plus[-5]]
            },
        ]
    }
    st_echarts(options=options, height=400, width=500)


def page_impressions_organic_paid(page_impressions_organic_unique_v2, page_impressions_paid,  dates):
    options = {
        "title": {
            "subtext": "Impressões Pagas vs Orgânicas"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": [" Impressões Orgânicas", "Impressões Pagas"]
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {}
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": dates
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": " Impressões Orgânicas",
                "type": "line",
                "data": page_impressions_organic_unique_v2
            },
            {
                "name": "Impressões Pagas",
                "type": "line",
                "data": page_impressions_paid
            },
        ]
    }
    st_echarts(options=options, height=400, width=1350)


def page_actions_post_reactions(post_reactions, dates):
    df = pd.DataFrame(post_reactions)
    df.fillna(0, inplace=True)
    # Sum the values of each reaction type
    total_reactions = df.sum()
    # Calculate the percentage for each reaction type
    total = total_reactions.sum()
    percentage_reactions = (total_reactions / total) * 100
    # Prepare data for the pie chart with emojis
    emoji_labels = {
        'love' : '❤️',
        'haha' : '😂',
        'wow'  : '😮',
        'sad'  : '😢',
        'angry': '😡',
        'like' : '👍',
    }
    data = [list(z) for z in zip(percentage_reactions.index, total_reactions, percentage_reactions)]
    # Create a pie chart
    pie_chart = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1200px", height="400px"))
        .add(
            series_name="Reações",
            data_pair=[[emoji_labels.get(item[0], item[0]), item[1]] for item in data],
            radius=["40%", "75%"],
            label_opts=opts.LabelOpts(is_show=True, formatter="{b}: {d}%")
        )
        .set_global_opts(
            title_opts  = opts.TitleOpts(title="Porcentagem por Reações"),
            legend_opts = opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
    )
    st_pyecharts(pie_chart)


def page_fans_country_plot(page_fans_country, dates):
    page_fans_country = pd.DataFrame(page_fans_country)
    page_fans_country_transposed = page_fans_country.transpose().reset_index()
    page_fans_country_transposed.rename(columns={'index': 'Country Code', page_fans_country_transposed.columns[1]: 'Value'}, inplace=True)
    country_mapping = {
        'US': 'United States',
        'CA': 'Canada',
        'FR': 'France',
        'DE': 'Germany',
        'BD': 'Bangladesh',
        'PT': 'Portugal',
        'HN': 'Honduras',
        'TZ': 'Tanzania',
        'PY': 'Paraguay',
        'HR': 'Croatia',
        'DO': 'Dominican Republic',
        'LY': 'Libya',
        'BO': 'Bolivia',
        'BR': 'Brazil',
        'DZ': 'Algeria',
        'ID': 'Indonesia',
        'CA': 'Canada',
        'EC': 'Ecuador',
        'US': 'United States',
        'MM': 'Myanmar',
        'EG': 'Egypt',
        'IN': 'India',
        'SY': 'Syria',
        'ZA': 'South Africa',
        'IQ': 'Iraq',
        'MX': 'Mexico',
        'CO': 'Colombia',
        'MZ': 'Mozambique',
        'AO': 'Angola',
        'ES': 'Spain',
        'VE': 'Venezuela',
        'AR': 'Argentina',
        'CU': 'Cuba',
        'PE': 'Peru',
        'PH': 'Philippines',
        'VN': 'Vietnam',
        'NG': 'Nigeria',
        'NI': 'Nicaragua',
        'PK': 'Pakistan',
        'NL': 'Netherlands',
    }
    page_fans_country_transposed['Country'] = page_fans_country_transposed['Country Code'].map(country_mapping)
    df = pd.DataFrame(page_fans_country_transposed)
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Value",
        color_continuous_scale=[
            (0.0, "rgb(255, 245, 240)"),
            (0.1, "rgb(254, 224, 210)"),
            (0.2, "rgb(252, 187, 161)"),
            (0.3, "rgb(252, 146, 114)"),
            (0.4, "rgb(251, 106, 74)"),
            (0.5, "rgb(239, 59, 44)"),
            (0.6, "rgb(203, 24, 29)"),
            (0.7, "rgb(165, 15, 21)"),
            (1.0, "rgb(103, 0, 13)")
        ],
        title="Curtidas na \nPágina por Países",
        projection="natural earth"
    )
    fig.update_layout(
        title_font=dict(size=18, family='Arial', color='black'),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            coastlinecolor="Gray",
            showland=False,
            landcolor="white",
            showocean=True,
            oceancolor="LightBlue",
            bgcolor='rgba(255,255,255,0)',
            lakecolor='DarkBlue',
            projection_scale=1.2,
            center=dict(lat=20, lon=0),
        ),
        margin={"r":0,"t":30,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',  
        title_xanchor='left',  # Align title to the right
        width=800,  # Increase width
        height=300  # Increase height
    )
    st.plotly_chart(fig)

def page_fan_adds_remove(page_fan_adds, page_fan_removes, dates):
    options = {
        "title": {
            "subtext": "Novos Seguidores/Deixaram de Seguir a Página"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["Novos Seguidores", "Deixaram de Seguir"]
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {}
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": dates
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": "Novos Seguidores",
                "type": "line",
                "areaStyle": {},
                "data": page_fan_adds
            },
            {
                "name": "Deixaram de Seguir",
                "type": "line",
                "areaStyle": {},
                "data": page_fan_removes
            },
        ]
    }
    st_echarts(options=options, height=400, width=1350)