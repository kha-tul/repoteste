
import streamlit as st
import pandas as pd
import plotly.express as px
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType
from streamlit_echarts import st_pyecharts
from streamlit_echarts import st_echarts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType


def inst_page_impression_reach_profile_views(impressions_values, reach_values, profile_views_values, dates):
    options = {
        "title": {
            "text": "Insights da Página"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["Impressões", "Alcance", "Visualizações de Perfil"]
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
                "name": "Impressões",
                "type": "line",
                "data": impressions_values
            },
            {
                "name": "Alcance",
                "type": "line",
                "data": reach_values
            },
            {
                "name": "Visualizações de Perfil",
                "type": "line",
                "data": profile_views_values
            },
        ]
    }
    st_echarts(options=options, height=400, width=1350)


def inst_profile_view_followers(profile_views_values, follower_count_values):
    total_profile_views = sum(profile_views_values)
    total_follower_count = sum(follower_count_values)
    total = total_profile_views + total_follower_count

    profile_views_percentage = (total_profile_views / total) * 100
    follower_count_percentage = (total_follower_count / total) * 100

    data = [
        ['Visualizações de Perfil', total_profile_views, profile_views_percentage],
        ['Contagem de Seguidores', total_follower_count, follower_count_percentage]
    ]
    pie_chart = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1200px", height="400px", is_horizontal_center= True))
        .add(
            series_name="Reactions",
            data_pair=[[item[0], item[1]] for item in data],
            radius=["40%", "75%"],
            label_opts=opts.LabelOpts(is_show=True, formatter="{b}: {d}%")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=" Percentuais de Visualizações\n de Perfil e Contagem\n de Seguidoress",
                                       pos_top="0%"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="35%", pos_left="2%"),
        )
    )
    st_pyecharts(pie_chart)




def phone_text_website_get_directions(phone_call_clicks, text_message_clicks, get_directions_clicks, website_clicks, dates):
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width=400, height=1200))
        .add_xaxis(dates)
        .add_yaxis("Cliques em Chamadas Telefônicas",     phone_call_clicks,  stack="stack2",   label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis("Cliques em Mensagens de Texto",   text_message_clicks,stack="stack2",   label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis("Cliques em Obter Direções", get_directions_clicks,stack="stack2", label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis("Cliques no Site",        website_clicks,       stack="stack2", label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            xaxis_opts=opts.AxisOpts(type_="category", name=""),
            yaxis_opts=opts.AxisOpts(type_="value", name="Cliques"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
            legend_opts=opts.LegendOpts(is_show=True, pos_bottom="0%", pos_left="center")
        )
    )
    st_pyecharts(bar)
    
def sum_phone_text_website_get_directions(phone_call_clicks, text_message_clicks, get_directions_clicks, website_clicks, dates):
    categories = ["Cliques em Chamadas Telefônicas", "Cliques em Mensagens de Texto", "Cliques em Obter Direções", "Cliques no Site"]
 
    total_phone_calls    = sum(phone_call_clicks)
    total_text_messages  = sum(text_message_clicks)
    total_get_directions = sum(get_directions_clicks)
    total_website_clicks = sum(website_clicks)

    totals = [total_phone_calls, total_text_messages, total_get_directions, total_website_clicks]

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="400", height="1200"))
        .add_xaxis(categories)
        .add_yaxis("Cliques totais", totals, label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            xaxis_opts=opts.AxisOpts(type_="value", name=" ",name_location="end", axislabel_opts=opts.LabelOpts(font_size=8,rotate=45)),
            yaxis_opts=opts.AxisOpts(type_="category", name="Categorias",             
                                     name_location="end",axislabel_opts=opts.LabelOpts(font_size=8,rotate=45)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
            legend_opts=opts.LegendOpts(is_show=True, pos_bottom="0%", pos_left="center"),
        )
        .reversal_axis()
    )
    st_pyecharts(bar)




def total_likes_by_titled_line_plot(ig_insights_by_total_values):
    titles = ig_insights_by_total_values['title'].tolist()
    values = ig_insights_by_total_values['total_value'].tolist()
    
    options = {
        "xAxis": {
            "type": "category",
            "data": titles,
            "name": "",
            "nameLocation": "middle",
            "nameTextStyle": {
                "fontSize": 16,
                "fontWeight": "bold",
                "padding": [10, 0, 0, 0]
            },
            "axisLabel": {
                "fontSize": 10,
                "fontWeight": "bold",
                # "rotate": 45
            },
        },
        "yAxis": {
            "type": "value",
            "name": "Value",
            "nameLocation": "middle",
            "nameTextStyle": {
                "fontSize": 16,
                "fontWeight": "bold",
                "padding": [0, 0, 30, 0]
            },
            "axisLabel": {
                "fontSize": 8,
                "fontWeight": "bold"
            },
        },
        "series": [
            {
                "data": values,
                "type": "scatter",
                "symbolSize": 20,
                "itemStyle": {
                    "color": "rgba(75, 0, 130, 0.8)",  # Change to your desired color
                    "borderColor": "rgba(75, 0, 130, 1)",
                    "borderWidth": 2
                }
            }
        ],
        "title": {
            "text": "Curtidas por postagem nos últimos 30 dias",
            "left": "center",
            "top": "top",
            "textStyle": {
                "fontSize": 15,
                "fontWeight": "bold"
            }
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}: {c}"
        }
    }
    st_echarts(options=options, height=400, width=1000)    


def total_likes_by_titled_pie_chart(ig_insights_by_total_values):
    titles = ig_insights_by_total_values['title'].tolist()
    values = ig_insights_by_total_values['total_value'].tolist()
    
    data = [{"name": title, "value": value} for title, value in zip(titles, values)]
    
    options = {
        "title": {
            "text": "Curtidas por postagem nos últimos 30 dias",
            "left": "center",
            "top": "top",
            "textStyle": {
                "fontSize": 15,
                "fontWeight": "bold"
            }
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "vertical",
            "left": "left",
            "data": titles
        },
        "series": [
            {
                "name": "Valor",
                "type": "pie",
                "radius": "50%",
                "data": data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                },
                "label": {
                    "normal": {
                        "show": True,
                        "formatter": "{b}: {c} ({d}%)"
                    }
                },
                "itemStyle": {
                    "normal": {
                        "borderWidth": 2,
                        "borderColor": "rgba(75, 0, 130, 1)",
                        "color": "rgba(75, 0, 130, 0.8)"
                    }
                }
            }
        ]
    }
    st_echarts(options=options, height=400, width=600)











