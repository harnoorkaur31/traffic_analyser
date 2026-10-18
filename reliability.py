import pandas as pd

def get_route_summary(df):
    # grouping by route to get average, max, and median delays
    summary = df.groupby('route').agg(
        avg_delay=('delay_mins', 'mean'),
        max_delay=('delay_mins', 'max'),
        median_delay=('delay_mins', 'median'),
        late_count=('is_late', 'sum'),
        total_days=('route', 'count')
    ).reset_index()

    # arithmetic column for % of days the route was late
    summary['late_percent'] = (summary['late_count'] / summary['total_days']) * 100
    return summary


# function to calculate reliability score and give text explanation
def evaluate_route(row):
    avg_d = row['avg_delay']
    max_d = row['max_delay']
    med_d = row['median_delay']
    late_p = row['late_percent']

    # start at 100 and subtract points for delays
    # meant to use median too so outliers dont ruin score, hope this formula is right
    score = 100 - (avg_d * 1.5) - (avg_d * 0.5)

    if score < 0:
        score = 0

    # core python rules to classify the route
    if avg_d > 10 and late_p > 50:
        status = "Frequently Delayed"
        reason = "High average delay and late on most days"
    elif max_d > 30 and med_d <= 5:
        status = "Reliable (One Extreme Delay)"
        reason = "Median delay is low, avg is only high because of one bad day"
    # fixed this to >= 40 bc R404 was showing up as reliable by mistake
    elif late_p >= 40:
        status = "Inconsistent"
        reason = "Late a couple times a week, hard to predict"
    else:
        status = "Reliable"
        reason = "Stays on schedule most of the time"

    return pd.Series([round(score, 1), status, reason])


# new function for weekday comparison
def get_weekday_summary(df):
    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    
    # group by day and get mean, median, and max
    weekday_stats = df.groupby('day').agg(
        avg_delay=('delay_mins', 'mean'),
        median_delay=('delay_mins', 'median'),
        max_delay=('delay_mins', 'max'),
        late_buses=('is_late', 'sum')
    )
    
    # reindex so it prints Mon-Fri instead of alphabetical
    weekday_stats = weekday_stats.reindex(day_order)
    return weekday_stats