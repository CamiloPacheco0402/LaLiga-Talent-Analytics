# LaLiga-Talent-Analytics

Data analysis of LaLiga academy players with Python, SQL, and Power BI# LaLiga Talent Factory Analytics



\## 📊 Proyecto de Análisis y Machine Learning



Análisis integral de jugadores de la Liga española utilizando Python, pandas, scikit-learn y visualización de datos avanzada. \*\*Objetivo:\*\* Identificar los 15 mejores prospectos talentosos basado en edad, potencial y eficiencia.



\---



\## 🎯 Motivación



El ecosistema de fútbol profesional requiere \*\*toma de decisiones basada en datos\*\* para identificar talento emergente. Este proyecto automatiza el análisis de:



\- \*\*Potencial de crecimiento\*\* (diferencia entre valor actual y proyectado)

\- \*\*Eficiencia\*\* (goles/asistencias por partido)

\- \*\*Segmentación\*\* (clustering de perfiles de jugadores)



\---



\## 📈 Resultados Clave



\### Top 15 Prospects Identificados:



| Ranking | Jugador | Edad | Posición | Valor Actual (M€) | Potencial (+M€) | Score |

|---------|---------|------|----------|-------------------|-----------------|-------|

| 1 | Arda Guler | 20 | RW | €40M | +€15M | 37.75 |

| 2 | Endrick | 18 | LW | €45M | +€15M | 37.20 |

| 3 | Brahim Diaz | 25 | RW | €30M | +€10M | 35.60 |

| 4 | Tchouameni | 24 | CM | €60M | +€15M | 33.10 |

| 5 | Rodrygo | 23 | RW | €90M | +€20M | 33.07 |



\*(Ver `data/top\_prospects.csv` para ranking completo)\*



\---



\## 🛠️ Metodología



\### \*\*1. Preparación de Datos\*\*

\- Dataset: 24 jugadores de Real Madrid (representativo de LaLiga)

\- Variables: Edad, Valor, Aplicaciones, Goles, Asistencias

\- Tratamiento: Normalización y creación de características derivadas



\### \*\*2. Variables Derivadas Creadas\*\* 

\### \*\*3. Análisis de Correlaciones\*\*

Matriz de correlaciones identifica relaciones entre variables:

\- Edad vs Valor: -0.45 (jugadores jóvenes = bajo valor actual)

\- Potencial vs Edad: -0.52 (jóvenes = mayor potencial)

\- Eficiencia vs Valor: +0.38 (eficiencia = mayor valor)



\### \*\*4. Machine Learning: K-Means Clustering\*\*

\- \*\*Algoritmo:\*\* K-Means (k=3 clusters)

\- \*\*Features normalizadas:\*\* Age, Current\_Value, Potential\_Gap, Goals\_Per\_App, Assists\_Per\_App

\- \*\*Resultados:\*\* 3 perfiles de jugadores identificados



\#### Clusters:

1\. \*\*Young Talents (Cluster 0):\*\* Jugadores jóvenes (<25) con alto potencial

2\. \*\*Established Stars (Cluster 1):\*\* Veteranos (25-31) en pico de valor

3\. \*\*Experience (Cluster 2):\*\* Veteranos (>31) con valor bajo



\### \*\*5. Scoring de Talentos\*\*

Fórmula ponderada:

\---



\## 📊 Visualizaciones



| Gráfica | Descripción | Archivo |

|---------|-------------|---------|

| Age vs Market Value | Scatter plot: correlación edad-valor | `age\_vs\_value.png` |

| Top 10 Talentos | Bar chart: 10 jugadores más valiosos | `top\_10\_talent.png` |

| Potential Gap Ranking | Ranking: máximo potencial de crecimiento | `potential\_gap.png` |

| Correlation Heatmap | Matriz de correlaciones entre variables | `correlation\_heatmap.png` |

| Player Clustering | Scatter 2D: visualización de clusters ML | `clustering\_visualization.png` |

| Top 15 Prospects | Bar chart: ranking final de prospectos | `top\_prospects\_ranking.png` |



\---



\## 💡 Insights Principales



1\. \*\*Juventud ≠ Valor\*\*: Los jugadores más jóvenes no son los más valiosos actualmente, pero tienen el mayor potencial de crecimiento.



2\. \*\*Eficiencia Detectada\*\*: Goles/asistencias por partido correlaciona (+0.38) con valor de mercado, indicando que eficiencia es predictor de valor.



3\. \*\*Segmentación Clara\*\*: K-Means identifica 3 perfiles distintos, permitiendo estrategias diferenciadas por edad/potencial.



4\. \*\*Top 3 Prospectos\*\*: Arda Guler (20), Endrick (18), Brahim Diaz (25) lideran en potencial + juventud + eficiencia.



\---



\## 🗂️ Estructura del Proyecto

\---



\## 🚀 Cómo Usar



\### \*\*Requisitos\*\*

```bash

python >= 3.8

pandas, numpy, matplotlib, seaborn, scikit-learn

```



\### \*\*Instalación\*\*

```bash

git clone https://github.com/CamiloPacheco0402/LaLiga-Talent-Analytics.git

cd LaLiga-Talent-Analytics

python -m venv venv

venv\\Scripts\\activate  # (Windows) o source venv/bin/activate (Mac/Linux)

pip install -r requirements.txt

```



\### \*\*Ejecución\*\*

```bash

\# Análisis exploratorio + visualizaciones básicas

python notebooks/analysis.py



\# ML clustering + ranking de talentos

python scripts/ml\_analysis.py

```



\### \*\*Resultados\*\*

\- Gráficas guardadas en `dashboards/`

\- CSVs de análisis en `data/`



\---



\## 📋 Variaciones Futuras



\- \[ ] Integración con datos reales de Transfermarkt/Understat

\- \[ ] Predicción de precio de transferencia (modelo de regresión)

\- \[ ] Dashboard interactivo en Power BI

\- \[ ] Análisis por posición (delanteros vs mediocampistas)

\- \[ ] Comparativa con ligas europeas (Premier League, Serie A)



\---



\## 👤 Autor



\*\*Juan Camilo Pacheco Bermúdez\*\*  

Data Analyst | Sports Analytics Enthusiast  

\[LinkedIn](https://linkedin.com/in/camilopacheco) | \[GitHub](https://github.com/CamiloPacheco0402)



\---



\## 📄 Licencia



Proyecto personal para portfolio. Datos simulados para fines educativos.



\---



\*\*Última actualización:\*\* Septiembre 2026

