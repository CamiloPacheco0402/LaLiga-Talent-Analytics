import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')

df = pd.read_csv('data/raw_players.csv')

df['Potential_Gap'] = df['Market_Value_M'] - df['Current_Value_M']
df['Potential_Pct'] = (df['Potential_Gap'] / df['Current_Value_M'] * 100).round(2)
df['Goals_Per_App'] = (df['Goals'] / df['Apps'].replace(0, 1)).round(3)
df['Assists_Per_App'] = (df['Assists'] / df['Apps'].replace(0, 1)).round(3)

print("="*60)
print("DAY 4-5: CORRELATIONS & ML ANALYSIS")
print("="*60)

correlation_cols = ['Age', 'Current_Value_M', 'Market_Value_M', 'Apps', 'Goals', 'Assists', 'Potential_Gap', 'Goals_Per_App', 'Assists_Per_App']
corr_matrix = df[correlation_cols].corr()
print("\n--- MATRIZ DE CORRELACIONES ---")
print(corr_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlations Matrix - LaLiga Talent Analytics', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('dashboards/correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("\nGrafica guardada: dashboards/correlation_heatmap.png")
plt.close()

print("\n--- ML: K-MEANS CLUSTERING ---")

features_for_ml = ['Age', 'Current_Value_M', 'Potential_Gap', 'Goals_Per_App', 'Assists_Per_App']
X = df[features_for_ml].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

print("\nClusters identificados:")
for cluster_id in range(3):
    cluster_players = df[df['Cluster'] == cluster_id]
    print(f"Cluster {cluster_id}: {len(cluster_players)} players")
    print(f"  - Edad promedio: {cluster_players['Age'].mean():.1f}")
    print(f"  - Valor promedio: {cluster_players['Current_Value_M'].mean():.1f}M")
    print(f"  - Potencial promedio: {cluster_players['Potential_Gap'].mean():.1f}M")

plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['Age'], df['Current_Value_M'], c=df['Cluster'], s=200, alpha=0.6, cmap='viridis', edgecolors='black', linewidth=1)
plt.xlabel('Age', fontsize=12)
plt.ylabel('Current Value (M)', fontsize=12)
plt.title('Player Clustering - LaLiga Talent Factory', fontsize=14, fontweight='bold')
plt.colorbar(scatter, label='Cluster')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('dashboards/clustering_visualization.png', dpi=300, bbox_inches='tight')
print("\nGrafica guardada: dashboards/clustering_visualization.png")
plt.close()

print("\n--- RANKING: TOP PROSPECTS ---")

df['Talent_Score'] = ((100 - df['Age']) * 0.2 + df['Potential_Pct'] * 0.3 + (df['Goals_Per_App'] * 10) * 0.2 + (df['Assists_Per_App'] * 10) * 0.2 + (df['Cluster'] == 0) * 10).round(2)

top_prospects = df.nlargest(15, 'Talent_Score')[['Player', 'Age', 'Position', 'Current_Value_M', 'Potential_Gap', 'Potential_Pct', 'Talent_Score', 'Cluster']]

print("\nTOP 15 PROSPECTS:")
print(top_prospects.to_string(index=False))

fig, ax = plt.subplots(figsize=(12, 8))
colors = ['#2ecc71' if row['Age'] < 25 else '#3498db' for _, row in top_prospects.iterrows()]
ax.barh(top_prospects['Player'], top_prospects['Talent_Score'], color=colors, alpha=0.8)
ax.set_xlabel('Talent Score', fontsize=12)
ax.set_title('Top 15 Prospects - LaLiga Talent Factory', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('dashboards/top_prospects_ranking.png', dpi=300, bbox_inches='tight')
print("\nGrafica guardada: dashboards/top_prospects_ranking.png")
plt.close()

df.to_csv('data/players_with_analysis.csv', index=False)
print("\nDataset completo guardado: data/players_with_analysis.csv")

top_prospects.to_csv('data/top_prospects.csv', index=False)
print("Top prospects guardado: data/top_prospects.csv")

print("\n" + "="*60)
print("DAY 4-5 COMPLETADO - ANALISIS Y ML")
print("="*60)
