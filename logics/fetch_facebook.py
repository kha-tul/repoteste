from facebook_business.adobjects.page import Page

def get_page_insights(page_id, start_date, end_date):
    page = Page(page_id)
    params = {
        'metric': [
            'page_post_engagements',                    # 0
            'page_impressions',                         # 1
            'page_impressions_unique',                  # 2
            'page_fans',                                # 3
            'page_daily_follows',                       # 4
            'page_views_total',                         # 5
            'page_negative_feedback_unique',            # 6
            'page_impressions_viral',                   # 7
            'page_fan_adds_by_paid_non_paid_unique',    # 8
            'page_daily_follows_unique',                # 9
            'page_daily_unfollows_unique',              # 10
            'page_impressions_by_age_gender_unique',    # 11
            'page_impressions_organic_unique_v2',       # 12
            'page_impressions_paid',                    # 13
            'page_actions_post_reactions_total',        # 14
            'page_fans_country',                        # 15
            'page_fan_adds',                            # 16
            'page_fan_removes',                         # 17
        ],
        'since': start_date,
        'until': end_date,
        'period': 'day'
    }
    insights = page.get_insights(params=params)
    return insights
