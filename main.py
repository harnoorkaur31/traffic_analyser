import pandas as pd
import matplotlib.pyplot as plt
from dataset import load_transport_data
from reliability import get_route_summary, evaluate_route, get_weekday_summary

# 1. get the dataframe
df = load_transport_data()
print("=== RAW TRANSPORT DATA ===")
print(df.head(10))

# 2. get route summary stats (mean, max, median)
route_stats = get_route_summary(df)

# 3. apply the reliability scoring function
route_stats[['score', 'status', 'explanation']] = route_stats.apply(evaluate_route, axis=1)

print("\n=== FULL ROUTE RELIABILITY REPORT ===")
print(route_stats[['route', 'avg_delay', 'median_delay', 'max_delay', 'score', 'status', 'explanation']])

# 4. filter and sort frequently late routes (late at least 40% of the time)
late_routes = route_stats[route_stats['late_percent'] >= 40]
late_routes_sorted = late_routes.sort_values(by='avg_delay', ascending=False)

print("\n=== PROBLEMATIC ROUTES (FILTERED & SORTED) ===")
print(late_routes_sorted[['route', 'avg_delay', 'late_percent', 'status']])


# 5. weekday performance comparison
print("\n=== WEEKDAY PERFORMANCE COMPARISON ===")
weekday_df = get_weekday_summary(df)
print(weekday_df)

# finding worst and best day using idxmax to get the day name instead of the number
worst_day = weekday_df['avg_delay'].idxmax()
best_day = weekday_df['avg_delay'].idxmin()

print(f"\nWorst day for traffic is {worst_day} and best day is {best_day}")

# check if any day has a fake high average because of one outlier
for day, row in weekday_df.iterrows():
    if row['avg_delay'] > 10 and row['median_delay'] <= 7:
        print(f"Note: {day} has a high average delay ({row['avg_delay']}m) mostly because of 1 extreme delay, median is only {row['median_delay']}m.")
    elif row['avg_delay'] > 10:
        print(f"Note: {day} has heavy delays across multiple routes.")


# 6. plotting the delays side by side
plt.figure(figsize=(8, 5))

# shifting x positions by 0.35 so the bars dont overlap on top of each other
x = range(len(route_stats['route']))
width = 0.35

plt.bar(x, route_stats['avg_delay'], width=width, label='Average Delay', color='salmon')
plt.bar([i + width for i in x], route_stats['median_delay'], width=width, label='Median Delay', color='skyblue')

# putting the route names roughly in the middle of the two bars
plt.xticks([i + width / 2 for i in x], route_stats['route'])

plt.title('Route Delay Comparison: Average vs Median')
plt.xlabel('Route')
plt.ylabel('Delay (Minutes)')
plt.legend()

# plt.savefig('route_delays.png')
plt.show()