import pandas as pd
import matplotlib.pyplot as plt # for the charts later
from dataset import load_transport_data
from reliability import get_route_summary, evaluate_route

# 1. get the dataframe
df = load_transport_data()
print("=== RAW TRANSPORT DATA ===")
print(df.head(10)) # just printing top 10 so terminal isnt spammed

# 2. get route summary stats (mean, max, median)
route_stats = get_route_summary(df)

# 3. apply the reliability scoring function
route_stats[['score', 'status', 'explanation']] = route_stats.apply(evaluate_route, axis=1)

print("\n=== FULL ROUTE RELIABILITY REPORT ===")
print(route_stats[['route', 'avg_delay', 'median_delay', 'max_delay', 'score', 'status', 'explanation']])

# 4. filter and sort frequently late routes (late at least 40% of the time)
late_routes = route_stats[route_stats['late_percent'] >= 40]

# sorting by average delay to show the worst ones first
late_routes_sorted = late_routes.sort_values(by='avg_delay')

print("\n=== PROBLEMATIC ROUTES (FILTERED & SORTED) ===")
print(late_routes_sorted[['route', 'avg_delay', 'late_percent', 'status']])


# 5. weekday performance comparison (WIP - 80% done)
print("\n=== WEEKDAY AVERAGE DELAYS ===")
weekday_avg = df.groupby('day')['delay_mins'].mean()
print(weekday_avg)

# TODO for tomorrow:
# - days are printing in alphabetical order (Fri, Mon, Thu...) need to fix order
# - write if/else to compare worst weekday vs best weekday
# - make matplotlib bar chart for route avg vs median delay