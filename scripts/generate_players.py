import pandas as pd
import numpy as np

np.random.seed(42)

base_data = {
    'Player': ['Vinicius Jr', 'Rodrygo', 'Bellingham', 'Camavinga', 'Valverde', 'Modric', 'Nacho', 'Militao', 'Mendy', 'Benzema', 'Kroos', 'Alaba', 'Rudiger', 'Carvajal', 'Brahim Diaz', 'Tchouameni', 'Endrick', 'Arda Guler', 'Vazquez', 'Lopez', 'Asensio', 'Ceballos', 'Garcia', 'Lunin'],
    'Age': [24, 23, 21, 22, 26, 38, 33, 26, 29, 35, 34, 32, 31, 31, 25, 24, 18, 20, 29, 25, 28, 26, 27, 25],
    'Position': ['LW', 'RW', 'CM', 'CM', 'CM', 'CM', 'CB', 'CB', 'LB', 'ST', 'CM', 'CB', 'CB', 'RB', 'RW', 'CM', 'LW', 'RW', 'RB', 'CB', 'RW', 'CM', 'LB', 'GK'],
    'Current_Value_M': [150, 90, 120, 70, 80, 15, 8, 25, 12, 20, 18, 20, 22, 15, 30, 60, 45, 40, 12, 10, 35, 25, 8, 8],
    'Market_Value_M': [175, 110, 140, 85, 95, 18, 10, 30, 15, 25, 22, 25, 28, 18, 40, 75, 60, 55, 15, 12, 45, 32, 10, 10],
    'Apps': [45, 38, 28, 42, 50, 180, 95, 80, 100, 120, 160, 120, 85, 110, 60, 35, 5, 8, 70, 50, 100, 80, 15, 25],
    'Goals': [15, 12, 8, 2, 5, 65, 2, 3, 1, 68, 15, 5, 8, 3, 10, 5, 2, 1, 2, 1, 12, 4, 0, 0],
    'Assists': [8, 7, 3, 1, 4, 20, 1, 0, 5, 20, 40, 2, 1, 5, 8, 2, 0, 1, 2, 1, 8, 8, 0, 0],
}

df_base = pd.DataFrame(base_data)

first_names = ['Carlos', 'Luis', 'Diego', 'Miguel', 'Juan', 'Pedro', 'Antonio', 'Jorge', 'Sergio', 'David', 'Pablo', 'Alejandro', 'Fernando', 'Roberto', 'Javier', 'Manuel', 'Marcos', 'Alvaro']
last_names = ['Garcia', 'Martinez', 'Lopez', 'Gonzalez', 'Rodriguez', 'Fernandez', 'Sanchez', 'Perez', 'Jimenez', 'Ramirez', 'Ruiz', 'Diaz', 'Moreno', 'Castro', 'Santos', 'Flores', 'Silva', 'Vargas']
positions = ['LW', 'RW', 'CM', 'CB', 'LB', 'RB', 'ST', 'GK']

new_rows = []

for i in range(120):
    name = first_names[i % len(first_names)] + ' ' + last_names[i % len(last_names)]
    pos = positions[i % len(positions)]
    age = int(np.random.uniform(18, 36))
    
    if age < 23:
        val = np.random.uniform(15, 60)
    elif age < 28:
        val = np.random.uniform(25, 100)
    else:
        val = np.random.uniform(10, 50)
    
    market = val * (1 + np.random.uniform(0.1, 0.35))
    apps = int(np.random.uniform(10, 150))
    
    if pos == 'ST':
        goals = int(apps * np.random.uniform(0.15, 0.25))
        asst = int(apps * np.random.uniform(0.03, 0.08))
    elif pos in ['LW', 'RW']:
        goals = int(apps * np.random.uniform(0.08, 0.15))
        asst = int(apps * np.random.uniform(0.05, 0.12))
    elif pos == 'CM':
        goals = int(apps * np.random.uniform(0.02, 0.08))
        asst = int(apps * np.random.uniform(0.04, 0.10))
    else:
        goals = int(apps * np.random.uniform(0.00, 0.04))
        asst = int(apps * np.random.uniform(0.00, 0.02))
    
    new_rows.append({
        'Player': name,
        'Age': age,
        'Position': pos,
        'Current_Value_M': round(val, 1),
        'Market_Value_M': round(market, 1),
        'Apps': apps,
        'Goals': max(0, goals),
        'Assists': max(0, asst)
    })

df_new = pd.DataFrame(new_rows)
df_combined = pd.concat([df_base, df_new], ignore_index=True)

df_combined['Potential_Gap'] = df_combined['Market_Value_M'] - df_combined['Current_Value_M']
df_combined['Potential_Pct'] = (df_combined['Potential_Gap'] / df_combined['Current_Value_M'] * 100).round(2)
df_combined['Goals_Per_App'] = (df_combined['Goals'] / df_combined['Apps'].replace(0, 1)).round(3)
df_combined['Assists_Per_App'] = (df_combined['Assists'] / df_combined['Apps'].replace(0, 1)).round(3)

df_combined.to_csv('data/players_expanded.csv', index=False)

print("DATASET EXPANDIDO CREADO")
print(f"Total jugadores: {len(df_combined)}")
print(f"Guardado: data/players_expanded.csv")
