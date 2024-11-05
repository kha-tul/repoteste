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

def averageSessionDuration_continent(data):
        countries = data['continent'].tolist()
        durations = data['averageSessionDuration'].tolist()
        unique_data = {}
        for country, duration in zip(countries, durations):
            if country not in unique_data:
                unique_data[country] = duration
        unique_countries = list(unique_data.keys())
        unique_durations = list(unique_data.values())
        options = {
            "title": {
                "text": "Duração média da \nsessão por continente"
            },
            "tooltip": {
                "trigger": 'axis'
            },
            "xAxis": {
                "type": 'category',
                "data": unique_countries
            },
            "yAxis": {
                "type": 'value'
            },
            "series": [{
                "data": unique_durations,
                "type": 'line',
                "areaStyle": {}
            }]
        }
        st_echarts(options=options, height="400px")


def bounceRate_engagementRate_engagedSessions(data):
        countries = data['country'].tolist()
        bounce_rates = data['bounceRate'].tolist()
        engagement_rates = data['engagementRate'].tolist()
        engaged_sessions = data['engagedSessions'].tolist()
        line = (
            Line(init_opts=opts.InitOpts(width="1500px", height="500px"))
            .add_xaxis(countries)
            .add_yaxis("Taxa de Rejeição", bounce_rates, is_smooth=True, label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("Taxa de Engajamento", engagement_rates, is_smooth=True, label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("Sessões Engajadas", engaged_sessions, is_smooth=True, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=""),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
                yaxis_opts=opts.AxisOpts(type_="value"),
            )
        )
        line.set_series_opts(
            label_opts=opts.LabelOpts(
                position="left",
                formatter=JsCode(
                    "function(params){"
                    "if(params.dataIndex == params.data.length - 1) {"
                    "return params.seriesName;"
                    "} else {"
                    "return '';"
                    "}"
                    "}"
                )
            )
        )
        st_pyecharts(line)


def dauPerMau_wauPerMau(data):
    data['dauPerMau']       = data['dauPerMau'].astype(float)
    data['wauPerMau']       = data['wauPerMau'].astype(float)
    data['eventCount']      = data['eventCount'].astype(int)
    data['sessions']        = data['sessions'].astype(int)
    data['screenPageViews'] = data['screenPageViews'].astype(int)

    fig = px.choropleth(
        data,
        locations="country",
        locationmode="country names",
        color="eventCount",
        hover_name="country",
        hover_data={
            "dauPerMau": True,
            "wauPerMau": True,
            "eventCount": True,
            "sessions": True,
        },
    )
    fig.update_traces(
        hovertemplate='<b>Country:</b> %{location}<br>' +
                      '<b>DAU/MAU:</b> %{customdata[0]:.2f}<br>' +
                      '<b>WAU/MAU:</b> %{customdata[1]:.2f}<br>' +
                      '<b>SESSIONS:</b> %{customdata[2]:.2f}<br>' +
                      '<b>PAGE VIEWS:</b> %{customdata[2]:.2f}<br>' +
                      '<b>Event Count:</b> %{z}<extra></extra>',
        customdata=data[['dauPerMau', 'wauPerMau', 'sessions', 'screenPageViews']].values
    )
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        title=dict(
            text='',
            x=0.5,
            xanchor='center'
        ),
        height = 500,
        width  = 800,
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    st.plotly_chart(fig)




def engagedSessions_plot(data, metric, dimensions):
    fig = go.Figure()
    
    for dim in dimensions:
        for val in data[dim].unique():
            filtered_data = data[data[dim] == val]
            fig.add_trace(go.Bar(
                x=filtered_data[metric],
                y=filtered_data[dim],
                orientation='h',
                name=f"{dim}: {val}",
            ))
    
    fig.update_layout(
        title="User Engagement Session",
        barmode='group',
        xaxis_title=metric
    )
    return fig


def source_activeUsers(data):
    aggregated_data = data.groupby('source').sum().reset_index()
    data_for_chart = [
        {"value": row['activeUsers'], "name": row['source']}
        for index, row in aggregated_data.iterrows()
    ]
    options = {
        "title": {
            "text": "",
            "left": "center"
        },
        "tooltip": {
            "trigger": "item"
        },
        "legend": {
            "show": False
        },
        "series": [
            {
                "name": "Active Users",
                "type": "pie",
                "radius": ["30%", "75%"],
                "center": ["50%", "60%"],
                "roseType": "area",
                "itemStyle": {
                    "borderRadius": 8
                },
                "label": {
                    "show": False
                },
                "labelLine": {
                    "show": True
                },
                "data": data_for_chart
            }
        ]
    }
    st_echarts(options=options, height="400px", width="650px")

# def source_activeUsers(data):
#     aggregated_data = data.groupby('source').sum().reset_index()
#     data_for_chart = [
#         {"value": row['activeUsers'], "name": row['source']}
#         for index, row in aggregated_data.iterrows()
#     ]
#     options = {
#         "title": {
#             "text": "",
#             "left": "center"
#         },
#         "tooltip": {
#             "trigger": "item"
#         },
#         # "legend": {
#         #     # "orient": "horizontal",
#         #     # "top": "top",
#         # },
#         "series": [
#             {
#                 "name": "Active Users",
#                 "type": "pie",
#                 "radius": ["30%", "75%"],
#                 "center": ["50%", "60%"],
#                 "roseType": "area",
#                 "itemStyle": {
#                     "borderRadius": 8
#                 },
#                 "data": data_for_chart
#             }
#         ]
#     }
#     st_echarts(options=options, height="400px", width="650px")


def eventName_eventCount_eventCountPerUser(data):
        events = data['eventName'].tolist()
        event_counts = data['eventCount'].tolist()
        event_counts_per_user = data['eventCountPerUser'].tolist()
        options = {
            "title": {
                "text": " ",
                "left": "center"
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "shadow"
                }
            },
            "legend": {
                "data": ['Contagem de Eventos', 'Contagem de Eventos por Usuário'],
                "top": "0%",  # Position the legend at the bottom
                "padding": [0, 0, 0, 0] # Top, Right, Bottom, Left
            },
            "xAxis": {
                "type": "category",
                "data": events,
                "axisTick": {
                    "alignWithLabel": True
                },
                "axisLabel": {
                    "interval": 0,
                    "rotate": 45,
                    "fontSize": 8  # Adjust the font size as needed
                }
            },
            "yAxis": [
                {
                    "type": "value",
                    "name": "Contagem de Eventos"
                },
                {
                    "type": "value",
                    "name": "Contagem de Eventos\n por Usuário",
                    "position": "right",
                    "alignTicks": True,
                    "axisLine": {
                        "show": True,
                        "lineStyle": {
                            "color": "#ff0000"
                        }
                    },
                    "axisLabel": {
                        "formatter": "{value}",
                    }
                }
            ],
            "series": [
                {
                    "name": "Contagem de Eventos",
                    "type": "bar",
                    "data": event_counts,
                    "barWidth": "40%"
                },
                {
                    "name": "Contagem de Eventos por Usuário",
                    "type": "bar",
                    "data": event_counts_per_user,
                    "yAxisIndex": 1,
                    "barWidth": "40%"
                }
            ]
        }
        st_echarts(options=options, height="400px", width="650px")



def screenPageViews_operatingSystem(data):
        unique_operating_systems = data['operatingSystem'].unique()
        unique_screen_page_views = data.drop_duplicates(subset=['operatingSystem'])['screenPageViews']
        bar = (
            Bar(init_opts=opts.InitOpts(width="600px", height="400px"))
            .add_xaxis(unique_operating_systems.tolist())
            .add_yaxis("Screen Page Views", unique_screen_page_views.tolist(), label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=" ", subtitle="Comparação de Diferentes Navegadores"),
                toolbox_opts=opts.ToolboxOpts(),
                legend_opts=opts.LegendOpts(is_show=True)
            )
        )
        st_pyecharts(bar)

def sessionSourceMedium_screenPageViews(data):
    aggregated_data = data.groupby('sessionSourceMedium', as_index=False)['screenPageViews'].sum()
    data_pairs = [{"name": name, "value": value} for name, value in zip(aggregated_data['sessionSourceMedium'], aggregated_data['screenPageViews'])]

    options = {
        "title": {
            "text": 'Visualizações de Páginas/Telas',
            "left": 'center',
            "top": 20,
            "textStyle": {
                "color": '#333',
                "fontSize": 20
            }
        },
        "tooltip": {
            "trigger": 'item',
            "formatter": '{b}: {c} ({d}%)'
        },
        "legend": {
             "show": False,
            "orient": 'vertical',
            "left": 'left',
            "data": aggregated_data['sessionSourceMedium'].tolist()
        },
        "series": [
            {
                "name": 'Screen Page Views',
                "type": 'pie',
                "radius": ['40%', '70%'],
                "center": ['50%', '60%'],
                "data": data_pairs,
                "label": {
                    "show": False,
                    "formatter": '{b}\n{c} ({d}%)',
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

def session_over_time(data):
    dates                  = data['date'].tolist()
    sessions               = data['sessions'].tolist()
    engaged_sessions       = data['engagedSessions'].tolist()
    averageSessionDuration = data['averageSessionDuration'].tolist()
    engagementRate         = data['engagementRate'].tolist()
    bounceRate             = data['bounceRate'].tolist()
    screenPageViews        = data['screenPageViews'].tolist()


    options = {
        "title": {
            "text": ""
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["Sessões", "Sessões Engajadas", "Avg Session Duration", "Taxa de Engajamento", "Taxa de Rejeição", "Visualizações de Páginas/Telas"]
        },
        "xAxis": {
            "type": "category",
            "data": dates
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": "Sessões",
                "type": "line",
                "data": sessions
            },
            {
                "name": "Sessões Engajadas",
                "type": "line",
                "data": engaged_sessions
            },
            {
                "name": "Avg Session Duration",
                "type": "line",
                "data": averageSessionDuration
            },
            {
                "name": "Taxa de Engajamento",
                "type": "line",
                "data": engagementRate
            },
            {
                "name": "Taxa de Rejeição",
                "type": "line",
                "data": bounceRate
            },
            {
                "name": "Visualizações de Páginas/Telas",
                "type": "line",
                "data": screenPageViews
            }
        ]
    }
    st_echarts(options=options)

def session_over_dayOfWeeks(data):
    data['sessions'] = pd.to_numeric(data['sessions'])
    data['engagedSessions'] = pd.to_numeric(data['engagedSessions'])
    data['averageSessionDuration'] = pd.to_numeric(data['averageSessionDuration'])
    data['engagementRate'] = pd.to_numeric(data['engagementRate'])
    data['bounceRate'] = pd.to_numeric(data['bounceRate'])
    data['screenPageViews'] = pd.to_numeric(data['screenPageViews'])
    data['eventCount'] = pd.to_numeric(data['eventCount'])
    days = sorted(data['dayOfWeek'].unique().tolist())
    sessions = data.groupby('dayOfWeek')['sessions'].sum().reindex(days).tolist()
    engagedSessions = data.groupby('dayOfWeek')['engagedSessions'].sum().reindex(days).tolist()
    averageSessionDuration = data.groupby('dayOfWeek')['averageSessionDuration'].mean().reindex(days).tolist()
    engagementRate = data.groupby('dayOfWeek')['engagementRate'].mean().reindex(days).tolist()
    bounceRate = data.groupby('dayOfWeek')['bounceRate'].mean().reindex(days).tolist()
    screenPageViews = data.groupby('dayOfWeek')['screenPageViews'].sum().reindex(days).tolist()
    eventCount = data.groupby('dayOfWeek')['eventCount'].sum().reindex(days).tolist()



    # Dictionary for mapping English days to Portuguese days
    day_mapping = {
        'Wednesday': 'Quarta-feira',
        'Tuesday': 'Terça-feira',
        'Thursday': 'Quinta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo',
        'Monday': 'Segunda-feira',
        'Friday': 'Sexta-feira'
    }
    translated_days = [day_mapping[day] for day in days]


    options = {
        "title": {
            "subtext": "Sessões ao Longo dos Dias da Semana"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": ["Sessões", "Sessões Engajadas", "Avg Session Duration", 
                     "Taxa de Engajamento", "Taxa de Rejeição", "Visualizações de Páginas/Telas", 
                     "Contagem de Eventos"],
            "orient": "horizontal",
            "bottom": 0
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "containLabel": True
        },
        "xAxis": {
            "type": "value"
        },
        "yAxis": {
            "type": "category",
            "data": translated_days
        },
        "series": [
            {
                "name": "Sessões",
                "type": "bar",
                "stack": "total",
                "data": sessions
            },
            {
                "name": "Sessões Engajadas",
                "type": "bar",
                "stack": "total",
                "data": engagedSessions
            },
            {
                "name": "Avg Session Duration",
                "type": "bar",
                "stack": "total",
                "data": averageSessionDuration
            },
            {
                "name": "Taxa de Engajamento",
                "type": "bar",
                "stack": "total",
                "data": engagementRate
            },
            {
                "name": "Taxa de Rejeição",
                "type": "bar",
                "stack": "total",
                "data": bounceRate
            },
            {
                "name": "Visualizações de Páginas/Telas",
                "type": "bar",
                "stack": "total",
                "data": screenPageViews
            },
            {
                "name": "Contagem de Eventos",
                "type": "bar",
                "stack": "total",
                "data": eventCount
            }
        ]
    }
    st_echarts(options=options)

def session_over_OS_Device_Browser(data):
    fig = px.sunburst(
        data,
        path=['operatingSystem', 'browser', 'deviceCategory'],
        values='sessions',
        color='sessions',
        color_continuous_scale='Viridis',
        title='Distribuição de Sessões'
    )
    fig.update_layout(margin=dict(t=40, l=0, r=0, b=0), width=400, height=600)
    st.plotly_chart(fig)





