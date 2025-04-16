import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from statsmodels.stats.weightstats import ztest

plt.switch_backend('TkAgg')

df = pd.read_csv(r"C:\Users\alwin\OneDrive\Desktop\directory\Python\DataScience Toolbox\pollution_dataset.csv")

print(df.isnull().sum())
print(df.isnull().sum().sum())

print("\nAfter cleaning.\n")
df.fillna(df.mean(numeric_only=True), inplace=True)
print(df.isnull().sum())

city_pollution = df.groupby('city')['pollutant_avg'].mean().sort_values(ascending=False)
top_10_most = city_pollution.head(10)
top_10_least = city_pollution.tail(10)[::-1]


fig6 = plt.figure(figsize=(8, 5))
plt.get_current_fig_manager().window.wm_geometry("1200x700")
sns.barplot(y=top_10_most.values, x=top_10_most.index, palette='Reds_r')
plt.title('Top 10 Most Polluted Cities', fontweight='bold')
plt.xlabel('Average Pollution Level')
plt.tight_layout()
plt.show()

fig7 = plt.figure(figsize=(8, 5))
plt.get_current_fig_manager().window.wm_geometry("1200x700")
sns.barplot(x=top_10_least.values, y=top_10_least.index, palette='Greens_r')
plt.title('Top 10 Least Polluted Cities', fontweight='bold')
plt.xlabel('Average Pollution Level')
plt.tight_layout()
plt.show()

stations_per_state = df.groupby('state')['station'].nunique()

plt.figure(figsize=(12, 6))
plt.get_current_fig_manager().window.wm_geometry("1200x700")
sns.barplot(x=stations_per_state.index, y=stations_per_state.values, palette='viridis')
plt.title("Number of Stations in Each State", fontsize=14, fontweight='bold')
plt.xlabel("State", fontsize=12)
plt.ylabel("Number of Stations", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

df['pollutant_avg'] = df['pollutant_avg'].fillna(df['pollutant_avg'].mean())

top_states = df.groupby('state')['pollutant_avg'].mean().nlargest(10)
top_states_data = df[df['state'].isin(top_states.index)]

plt.figure(figsize=(12, 8))
plt.get_current_fig_manager().window.wm_geometry("1200x700")
sns.boxplot(x='state', y='pollutant_avg', data=top_states_data, palette='Reds')
plt.title("Pollution Level Distribution in Top 10 States")
plt.xlabel("State")
plt.ylabel("Pollution Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

pollutant_avg = df.groupby('pollutant_id')['pollutant_avg'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
plt.get_current_fig_manager().window.wm_geometry("1200x700")
sns.barplot(x=pollutant_avg.index, y=pollutant_avg.values, palette='viridis')
plt.title("Average Pollutant Levels by Pollutant Type")
plt.xlabel("Pollutant Type")
plt.ylabel("Average Pollution Level")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

state_pollutant_avg = df.groupby(['state', 'pollutant_id'])['pollutant_avg'].mean().reset_index()

plt.figure(figsize=(14, 8))
plt.get_current_fig_manager().window.wm_geometry("1200x700")
sns.scatterplot(data=state_pollutant_avg, x='state', y='pollutant_avg', hue='pollutant_id', s=100)
plt.title("State-wise Pollutant Type Variation")
plt.xlabel("State")
plt.ylabel("Average Pollution Level")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

'''
pollutant_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'OZONE', 'CO']
pollutant_data = df[pollutant_cols]
correlation_matrix = pollutant_data.corr()

plt.figure(figsize=(10, 7))
plt.get_current_fig_manager().window.wm_geometry("1200x700")
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of Pollutants")
plt.tight_layout()
plt.show()
'''

custom_greys = LinearSegmentedColormap.from_list(
    "custom_greys", ["#B0B0B0", "#3A3A3A"]
)

plt.figure(figsize=(8, 10))
plt.get_current_fig_manager().window.wm_geometry("500x600+700+300")
plt.gca().set_facecolor('#E8E8E8')
plt.gcf().set_facecolor('#E8E8E8')

scatter = plt.scatter(
    df['longitude'],
    df['latitude'],
    c=df['pollutant_avg'],
    cmap=custom_greys,
    s=20,
    alpha=0.8
)

cbar = plt.colorbar(scatter, label='Average Pollution Level')
cbar.ax.yaxis.label.set_color('black')
cbar.ax.tick_params(colors='black')

plt.title("Pollution Distribution by Latitude and Longitude", color='black')
plt.xlabel("Longitude", color='black')
plt.ylabel("Latitude", color='black')
plt.xticks(color='black')
plt.yticks(color='black')
plt.tight_layout()

plt.show()

state1_pollution = df[df['state'] == 'Delhi']['pollutant_avg'].dropna()
state2_pollution = df[df['state'] == 'Gujarat']['pollutant_avg'].dropna()

print(f"State1 entries: {len(state1_pollution)}, State2 entries: {len(state2_pollution)}")

if len(state1_pollution) > 0 and len(state2_pollution) > 0:
    z_stat, p_val = ztest(state1_pollution, state2_pollution)
    print(f"\nZ-statistic: {z_stat:.2f}, P-value: {p_val:.4f}")
    if p_val < 0.05:
        print("Significant difference in pollution levels between State1 and State2.")
    else:
        print("No significant difference found.")
else:
    print("Not enough data to perform Z-test.")
