import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')

# Load the real 150+ player dataset
df = pd.read_csv('data/players_laliga_real_150.csv')

# Ensure all required columns exist
if 'Potential_Gap' not in df.columns:
    df['Potential_Gap'] = df['Market_Value_M'] - df['Current_Value_M']
if 'Potential_Pct' not in df.columns:
    df['Potential_Pct'] = (df['Potential_Gap'] / df['Current_Value_M'] * 100).round(2)
if 'Goals_Per_App' not in df.columns:
    df['Goals_Per_App'] = (df['Goals'] / df['Apps'].replace(0, 1)).round(3)
if 'Assists_Per_App' not in df.columns:
    df['Assists_Per_App'] = (df['Assists'] / df['Apps'].replace(0, 1)).round(3)

print("="*60)
print("REAL LALIGA DATA: CORRELATIONS & ML ANALYSIS")
print(f"Analyzing {len(df)} real players from {df['Team'].nunique()} teams")
print("="*60)

# Correlation analysis
correlation_cols = ['Age', 'Current_Value_M', 'Market_Value_M', 'Apps', 'Goals', 'Assists', 'Potential_Gap', 'Goals_Per_App', 'Assists_Per_App']
corr_matrix = df[correlation_cols].corr()
print("\n--- CORRELATION MATRIX ---")
print(corr_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix - LaLiga Talent Analytics (150+ Real Players)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('dashboards/correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("\n✅ Visualization saved: dashboards/correlation_heatmap.png")
plt.close()

print("\n--- K-MEANS CLUSTERING ---")

features_for_ml = ['Age', 'Current_Value_M', 'Potential_Gap', 'Goals_Per_App', 'Assists_Per_App']
X = df[features_for_ml].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

print("\nClusters Identified:")
for cluster_id in range(3):
    cluster_players = df[df['Cluster'] == cluster_id]
    print(f"\n🎯 Cluster {cluster_id}: {len(cluster_players)} players")
    print(f"   - Average Age: {cluster_players['Age'].mean():.1f}")
    print(f"   - Average Value: €{cluster_players['Current_Value_M'].mean():.1f}M")
    print(f"   - Average Potential Gap: €{cluster_players['Potential_Gap'].mean():.1f}M")
    print(f"   - Top Player: {cluster_players.nlargest(1, 'Talent_Score')['Player'].values[0]}")

# Clustering visualization
plt.figure(figsize=(12, 8))
scatter = plt.scatter(df['Age'], df['Current_Value_M'], c=df['Cluster'], s=200, alpha=0.6, cmap='viridis', edgecolors='black', linewidth=1.5)
plt.xlabel('Age', fontsize=12, fontweight='bold')
plt.ylabel('Current Value (€M)', fontsize=12, fontweight='bold')
plt.title('Player Clustering - LaLiga Talent Factory (Real Data)', fontsize=14, fontweight='bold')
plt.colorbar(scatter, label='Cluster')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('dashboards/clustering_visualization.png', dpi=300, bbox_inches='tight')
print("\n✅ Visualization saved: dashboards/clustering_visualization.png")
plt.close()

print("\n--- TOP PROSPECTS RANKING ---")

# Use existing Talent_Score if available, otherwise calculate
if 'Talent_Score' not in df.columns:
    df['Talent_Score'] = ((100 - df['Age']) * 0.2 + df['Potential_Pct'] * 0.3 + (df['Goals_Per_App'] * 10) * 0.2 + (df['Assists_Per_App'] * 10) * 0.2 + (df['Cluster'] == 0) * 10).round(2)

top_prospects = df.nlargest(15, 'Talent_Score')[['Player', 'Age', 'Position', 'Team', 'Current_Value_M', 'Potential_Gap', 'Potential_Pct', 'Talent_Score', 'Cluster']]

print("\n🏆 TOP 15 PROSPECTS:")
print(top_prospects.to_string(index=False))

# Top prospects visualization
fig, ax = plt.subplots(figsize=(12, 8))
colors = ['#2ecc71' if row['Age'] < 25 else '#3498db' for _, row in top_prospects.iterrows()]
ax.barh(top_prospects['Player'], top_prospects['Talent_Score'], color=colors, alpha=0.8, edgecolor='black', linewidth=1)
ax.set_xlabel('Talent Score', fontsize=12, fontweight='bold')
ax.set_ylabel('Player', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Prospects - LaLiga Talent Factory', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('dashboards/top_prospects_ranking.png', dpi=300, bbox_inches='tight')
print("\n✅ Visualization saved: dashboards/top_prospects_ranking.png")
plt.close()

# Age vs Value visualization
plt.figure(figsize=(12, 8))
positions = df['Position'].unique()
colors_map = {pos: plt.cm.Set3(i) for i, pos in enumerate(positions)}
for pos in positions:
    pos_data = df[df['Position'] == pos]
    plt.scatter(pos_data['Age'], pos_data['Current_Value_M'], label=pos, s=200, alpha=0.6, edgecolors='black', linewidth=1)
plt.xlabel('Age', fontsize=12, fontweight='bold')
plt.ylabel('Current Value (€M)', fontsize=12, fontweight='bold')
plt.title('Age vs Market Value by Position', fontsize=14, fontweight='bold')
plt.legend(title='Position', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('dashboards/age_vs_value.png', dpi=300, bbox_inches='tight')
print("✅ Visualization saved: dashboards/age_vs_value.png")
plt.close()

# Save processed data
df.to_csv('data/players_with_analysis.csv', index=False)
print("\n✅ Full dataset saved: data/players_with_analysis.csv")

top_prospects.to_csv('data/top_prospects.csv', index=False)
print("✅ Top prospects saved: data/top_prospects.csv")

print("\n" + "="*60)
print("✅ ANALYSIS COMPLETE - REAL LALIGA DATA PROCESSED")
print("="*60)
