import pandas as pd
from streamlit_echarts import st_echarts


def google_ads_impressions_clicks(data):
    df = pd.DataFrame(data)
    df_unique = df.drop_duplicates(subset=["campaignName"])
    campaigns = df_unique["campaignName"].tolist()
    clicks = df_unique["advertiserAdClicks"].tolist()
    impressions = df_unique["advertiserAdImpressions"].tolist()
    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'cross'
            }
        },
        "legend": {
            "data": ['Ad Clicks', 'Impressão de Anúncio']
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "10%",
            "containLabel": True
        },
        "xAxis": {
            "type": 'category',
            "boundaryGap": False,
            "data": campaigns,
            "axisLabel": {
                "interval": 0,
                "rotate": 45,
                "fontSize": 8,
                "formatter": '{value}'
            },
        },
        "yAxis": {
            "type": 'value'
        },
        "series": [
            {
                "name": 'Ad Clicks',
                "type": 'line',
                "data": clicks,
                "itemStyle": {
                    "color": 'red'
                },
                "lineStyle": {
                    "color": 'red'
                }
            },
            {
                "name": 'Impressão de Anúncio',
                "type": 'line',
                "data": impressions,
                "itemStyle": {
                    "color": 'green'
                },
                "lineStyle": {
                    "color": 'green'
                }
            }
        ],
    }
    st_echarts(options=option, height=500, width=800)


def google_ads_cost_perclick(data):
    df = pd.DataFrame(data)
    df["advertiserAdCost"] = pd.to_numeric(df["advertiserAdCost"])
    df["advertiserAdCostPerClick"] = pd.to_numeric(df["advertiserAdCostPerClick"])
    df["simpleCampaignName"] = df["campaignName"].apply(lambda x: x.split(' - ')[-1])
    simple_campaigns = df["simpleCampaignName"].unique().tolist()
    days = df["dayOfWeek"].unique().tolist()

    combined_costs = {campaign: [] for campaign in simple_campaigns}

    for day in days:
        day_data = df[df["dayOfWeek"] == day]
        for campaign in simple_campaigns:
            campaign_data = day_data[day_data["simpleCampaignName"] == campaign]
            if not campaign_data.empty:
                total_cost = campaign_data["advertiserAdCost"].sum() + campaign_data["advertiserAdCostPerClick"].sum()
                combined_costs[campaign].append(total_cost)
            else:
                combined_costs[campaign].append(0)

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


    series_data = []
    for campaign in simple_campaigns:
        series_data.append({
            "name": campaign,
            "type": "bar",
            "stack": "Total",
            "label": {"show": False},
            "data": combined_costs[campaign]
        })
    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "legend": {
            "data": simple_campaigns
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "xAxis": {
            "type": "value",
            "boundaryGap": [0, 0.01]
        },
        "yAxis": {
            "type": "category",
            "data": translated_days
        },
        "series": series_data
    }
    st_echarts(options=options, height=400, width=1500)




def advertiserAdCostPerClick(data):
    df = pd.DataFrame(data)
    campaigns = df["campaignName"].unique().tolist()
    months = df["month"].unique().tolist()
    series_data = []
    for campaign in campaigns:
        campaign_data = df[df['campaignName'] == campaign]
        series_data.append({
            "name": campaign,
            "type": "line",
            "stack": "Total",
            "areaStyle": {},
            "emphasis": {
                "focus": "series"
            },
            "data": campaign_data['advertiserAdCostPerClick'].tolist()
        })
    options = {
        "title": {
            "subtext": "Custo de Anúncio Vs Custo por Clique no Anúncio (ROI)",
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross"
            }
        },
        "legend": {
            "data": campaigns,
            "orient": "horizontal",
            "top": "bottom",
            "padding": [10, 10, 10, 10],  # Increase padding around the legend
            "itemGap": 10  # Increase gap between legend items
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "25%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": months,
            "axisLabel": {
                "rotate": -45,
                "padding": [130, 0, 0, 0],  #Top, Right, Bottom, Left  Increase padding above the labels
                "lineHeight": 130  # Increase line height for the labels
            },
            "splitLine": {
                "show": True,
                "lineStyle": {
                    "color": "lightgrey"
                }
            }
        },
        "yAxis": {
            "type": "value",
            "splitLine": {
                "show": True,
                "lineStyle": {
                    "color": "lightgrey"
                }
            }
        },
        "series": series_data
    }
    st_echarts(options=options, height=500, width=800)



def returnOnAdSpend(data):
    df = pd.DataFrame(data)
    df["simpleCampaignName"] = df["campaignName"].apply(lambda x: x.split(' - ')[-1])
    summed_data = df.groupby("simpleCampaignName")["returnOnAdSpend"].sum().reset_index()
    campaigns = summed_data["simpleCampaignName"].tolist()
    return_values = summed_data["returnOnAdSpend"].tolist()
    options = {
        "title": {
            "subtext": "Retorno do Investimento em Anúncios por Campanha",
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "legend": {
            "data": ["Retorno do investimento em publicidade"],
            "top": "bottom"
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "10%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "data": campaigns,
            "axisLabel": {
                "rotate": -45,
                "interval": 0
            },
            "splitLine": {
                "show": False
            }
        },
        "yAxis": {
            "type": "value",
            "splitLine": {
                "show": False,
                "lineStyle": {
                    "color": "lightgrey"
                }
            }
        },
        "series": [
            {
                "name": "Retorno do investimento em publicidade",
                "type": "bar",
                "data": return_values,
                "itemStyle": {
                    "color": "#5470C6"
                },
                "label": {
                    "show": True,
                    "position": "top"
                }
            }
        ]
    }
    st_echarts(options=options, height=500, width=800)



def returnOnAdSpendLiquidFill(data):
    df = pd.DataFrame(data)
    df["simpleCampaignName"] = df["campaignName"].apply(lambda x: x.split(' - ')[-1])
    summed_data = df.groupby("simpleCampaignName")["returnOnAdSpend"].sum().reset_index()
    total_return_on_ad_spend = float(summed_data["returnOnAdSpend"].sum())
    options = {
        "title": {
            "subtext": "Total Return on Ad Spend",
            "left": "center"
        },
        "series": [
            {
                "type": "liquidFill",
                "data": [total_return_on_ad_spend],
                "label": {
                    "normal": {
                        "formatter": f"{total_return_on_ad_spend:.2f}",
                        "textStyle": {
                            "fontSize": 20
                        }
                    }
                },
                "outline": {
                    "borderDistance": 4,
                    "itemStyle": {
                        "borderWidth": 2,
                        "borderColor": '#1e90ff',
                        "shadowBlur": 20,
                        "shadowColor": 'rgba(0, 0, 0, 0.25)'
                    }
                },
                "backgroundStyle": {
                    "color": 'rgba(0, 0, 0, 0.05)'
                },
                "itemStyle": {
                    "opacity": 0.6,
                    "shadowBlur": 10,
                    "shadowColor": 'rgba(0, 0, 0, 0.25)'
                }
            }
        ]
    }
    st_echarts(options=options, height="400px", width="600px")