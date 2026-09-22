import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # No-display backend

# Crea datos
players_data = {
    'Player': ['Vinicius Jr', 'Rodrygo', 'Bellingham', 'Camavinga', 'Valverde', 'Modric', 'Nacho', 'Militao', 'Mendy', 'Benzema', 'Kroos', 'Alaba', 'Rudiger', 'Carvajal', 'Brahim Diaz', 'Tchouameni', 'Endrick', 'Arda Guler', 'Vazquez', 'Lopez', 'Asensio', 'Ceballos', 'Garcia', 'Lunin'],
    'Age': [24, 23, 21, 22, 26, 38, 33, 26, 29, 35, 34, 32, 31, 31, 25, 24, 18, 20, 29, 25, 28, 26, 27, 25],
    'Position': ['LW', 'RW', 'CM', 'CM', 'CM', 'CM', 'CB', 'CB', 'LB', 'ST', 'CM', 'CB', 'CB', 'RB', 'RW', 'CM', 'LW', 'RW', 'RB', 'CB', 'RW', 'CM', 'LB', 'GK'],
    'Current_Value_M': [150, 90, 120, 70, 80, 15, 8, 25, 12, 20, 18, 20, 22, 15, 30, 60, 45, 40, 12, 10, 35, 25, 8, 8],
    'Market_Value_M': [175, 110, 140, 85, 95, 18, 10, 30, 15, 25, 22, 25, 28, 18, 40, 75, 60, 55, 15, 12, 45, 32, 10, 10],
    'Apps': [45, 38, 28, 42, 50, 180, 95, 80, 100, 120, 160, 120, 85, 110, 60, 35, 5, 8, 70, 50, 100, 80, 15, 25],
    'Goals': [15, 12, 8, 2, 5, 65, 2, 3, 1, 68, 15, 5, 8, 3, 10, 5, 2, 1, 2, 1, 12, 4, 0, 0],
    'Assists': [8, 7, 3, 1, 4, 20, 1, 0, 5, 20, 40, 2, 1, 5, 8, 2, 0, 1, 2, 1, 8, 8, 0, 0],
}

df = pd.DataFrame(players_data)

# Crear variables derivadas
df['Potential_Gap'] = df['Market_Value_M'] - df['Current_Value_M']
df['Potential_Pct'] = (df['Potential_Gap'] / df['Current_Value_M'] * 100).round(2)
df['Goals_Per_App'] = (df['Goals'] / df['Apps'].replace(0, 1)).round(3)
df['Assists_Per_App'] = (df['Assists'] / df['Apps'].replace(0, 1)).round(3)

print("="*50)
print("LALIGA TALENT FACTORY ANALYTICS")
print("="*50)

print("\n✓ Datos cargados correctamente")
print(f"Dataset shape: {df.shape}")

print("\n--- PRIMERAS 5 FILAS ---")
print(df.head())

print("\n--- ESTADÍSTICAS BÁSICAS ---")
print(df.describe())

print("\n--- EDAD ---")
print(f"Edad promedio: {df['Age'].mean():.1f}")
print(f"Edad máxima: {df['Age'].max()}")
print(f"Edad mínima: {df['Age'].min()}")

print("\n--- JUGADORES POR POSICIÓN ---")
print(df['Position'].value_counts())

print("\n--- TOP 10 JUGADORES POR VALOR ---")
top_10 = df.nlargest(10, 'Current_Value_M')[['Player', 'Age', 'Position', 'Current_Value_M']]
print(top_10)

print("\n--- VARIABLES DERIVADAS (PRIMERAS 5) ---")
print(df[['Player', 'Potential_Gap', 'Potential_Pct', 'Goals_Per_App', 'Assists_Per_App']].head())

# ===== VISUALIZACIÓN 1: Edad vs Valor =====
plt.figure(figsize=(10, 6))
plt.scatter(df['Age'], df['Current_Value_M'], s=100, alpha=0.6, c=df['Current_Value_M'], cmap='viridis')
plt.xlabel('Age', fontsize=12)
plt.ylabel('Current Value (M€)', fontsize=12)
plt.title('Age vs Current Market Value - LaLiga Talent', fontsize=14, fontweight='bold')
plt.colorbar(label='Value (M€)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('dashboards/age_vs_value.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfica guardada: dashboards/age_vs_value.png")
plt.close()

# ===== VISUALIZACIÓN 2: Top 10 Talentos =====
top_10_data = df.nlargest(10, 'Current_Value_M')
plt.figure(figsize=(12, 6))
plt.barh(top_10_data['Player'], top_10_data['Current_Value_M'], color='steelblue')
plt.xlabel('Current Value (M€)', fontsize=12)
plt.title('Top 10 Most Valuable Players - LaLiga Talent Factory', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('dashboards/top_10_talent.png', dpi=300, bbox_inches='tight')
print("✓ Gráfica guardada: dashboards/top_10_talent.png")
plt.close()

# ===== VISUALIZACIÓN 3: Potential Gap =====
potential_data = df.nlargest(12, 'Potential_Gap')[['Player', 'Potential_Gap']].sort_values('Potential_Gap')
plt.figure(figsize=(12, 7))
colors = ['green' if x > 0 else 'red' for x in potential_data['Potential_Gap']]
plt.barh(potential_data['Player'], potential_data['Potential_Gap'], color=colors, alpha=0.7)
plt.xlabel('Potential Gap (M€)', fontsize=12)
plt.title('Top 12 Players by Growth Potential - Market Value vs Current', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('dashboards/potential_gap.png', dpi=300, bbox_inches='tight')
print("✓ Gráfica guardada: dashboards/potential_gap.png")
plt.close()

# Guarda datos
df.to_csv('data/raw_players.csv', index=False)
print("\n✓ Datos guardados en: data/raw_players.csv")

print("\n" + "="*50)
print("ANÁLISIS COMPLETADO - DAY 3 ✓")
print("="*50)