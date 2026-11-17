# %% [markdown]
# # Análisis base de datos sobre carros
# Integrantes: Juan David Prieto, Samuel Andres Betancourt

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("datos/data.csv")
# %% [markdown]
# ## 1. Carga e inspección inicial de los datos  (Juan David)
# %%
print("Filas y columnas:", df.shape)
# %%
df.head()
# %%
df.info()
# %%
df.nunique()
# %%
df.describe()
# %%
df.describe(exclude="number")
# %% [markdown]
# Clasificación de variables:
# - Categóricas (8): Make, Model, Engine Fuel Type, Transmission Type, Driven_Wheels, Market Category, Vehicle Size, Vehicle Style
# - Numéricas continuas (4): Engine HP, highway MPG, city mpg, MSRP
# - Numéricas discretas (4): Year, Engine Cylinders, Number of Doors, Popularity

# Conclusión: el conjunto tiene 11.914 registros y 16 variables. Cada fila es una versión de un modelo de carro con sus características y su precio (MSRP). Hay datos faltantes en Engine HP, Engine Cylinders, Number of Doors, Engine Fuel Type y sobre todo en Market Category. El precio promedio (40.595) es mayor que la mediana (29.995), lo que indica que unos pocos carros muy caros inflan el promedio. También hay valores raros, como highway MPG de 354 y cilindros en 0, que se revisan en el ítem 3.

# %% [markdown]
# ## 2. Manejo de datos faltantes  (Samuel Andres)

# %%
missing_df = pd.DataFrame({
    'Valores Nulos': df.isnull().sum(),
    'Porcentaje (%)': (df.isnull().sum() / len(df)) * 100
})


print(missing_df[missing_df['Valores Nulos'] > 0].sort_values(by='Porcentaje (%)', ascending=False))

# %%

plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
plt.title('Mapa de Calor General de Valores Nulos en Car Features')
plt.xlabel('Columnas del Dataset')
plt.show()

# %%
if 'Engine HP' in df.columns:
    mediana_hp = df['Engine HP'].median()
    df['Engine HP'] = df['Engine HP'].fillna(mediana_hp)


if 'Engine Cylinders' in df.columns:
    moda_cilindros = df['Engine Cylinders'].mode()[0]
    df['Engine Cylinders'] = df['Engine Cylinders'].fillna(moda_cilindros)

df.loc[:,['Engine HP','Engine Cylinders']]

# %%

if 'MSRP' in df.columns:
    filas_iniciales = len(df)
    df.dropna(subset=['MSRP'], inplace=True)

df['MSRP']
# %% [markdown]
# Conclusión: Market Category faltan 3.742 datos , ya que muchos vehículos normales o antiguos no pertenecen a ninguna categoría especial; en lugar de eliminar casi una gran parte  del dataset, se imputan como "None". En Engine HP 69 nulos y Engine Cylinders 30 nulos, , el porcentaje faltante es mínimo y sin patrones marcados en los mapas de calor, por lo que se imputan con la mediana y la moda respectivamente para conservar todos los registros sin sesgar el análisis.

# %% [markdown]
# ## 3. Manejo de outliers (Juan David)
# %%
plt.figure(figsize=(8, 4))
sns.boxplot(x=df["MSRP"])
plt.xscale("log")
plt.title("Boxplot de MSRP (escala logarítmica)")
plt.show()

# %%
Q1 = df["MSRP"].quantile(0.25)
Q3 = df["MSRP"].quantile(0.75)
IQR = Q3 - Q1
limite_sup = Q3 + 1.5 * IQR
outliers = df[df["MSRP"] > limite_sup]
print("Límite superior:", limite_sup)
print("Cantidad de outliers:", len(outliers))
print("Porcentaje:", round(len(outliers) / len(df) * 100, 2), "%")

# %%
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col in zip(axes, ["Engine HP", "highway MPG", "city mpg"]):
    sns.boxplot(y=df[col], ax=ax)
    ax.set_title(f"Boxplot de {col}")
plt.tight_layout()
plt.show()

# %%
df[df["highway MPG"] > 100][["Make", "Model", "Year", "Engine Fuel Type", "highway MPG", "city mpg"]]

# %% [markdown]
# Conclusión: en MSRP hay 996 outliers (8,36 %) por encima de 74.078 USD. Corresponden a carros de lujo y superdeportivos con precios reales, por lo que no se eliminan. Engine HP también tiene valores altos (hasta 1000 HP) que son superdeportivos reales. En highway MPG y city mpg los valores muy altos (hasta 354) corresponden a carros eléctricos, que se miden en MPGe y no son comparables con los de gasolina. Se conservan, pero al analizar el consumo conviene separar los eléctricos.

# %% [markdown]
# ## 4. Valores inconsistentes y duplicados  (Samuel Andres)
# %%

duplicados_totales = df.duplicated().sum()
print(f"Número de filas duplicadas encontradas: {duplicados_totales}")

# %%
df = df.drop_duplicates().reset_index(drop=True)

# %%

columnas_texto = df.select_dtypes(include=['object']).columns

for col in columnas_texto:
   
    df[col] = df[col].astype(str).str.strip().str.title()
    
    
    df[col] = df[col].replace(['Nan', 'None', 'Na'], np.nan)
# %%
print("Valores únicos antes de corregir en Transmission Type:")
print(df['Transmission Type'].value_counts())

#%% [markdown]
# Conclusión: La eliminación de registros duplicados evita sesgos por redundancia en el dataset, mientras que la estandarización de los campos de texto garantiza que categorías como las marcas o los tipos de transmisión no se fragmenten en múltiples entradas artificiales, asegurando la consistencia y seguridad para el análisis posterior.
# %% [markdown]
# ## 5. Creación de variables  (Integrante A)

# %% [markdown]
# ## 6. Filtrado y condiciones en pandas  (Samuel Andres)


# %%
top_marcas = df.groupby('Make')['MSRP'].mean().sort_values(ascending=False).head(5)
print(f"Marcas más caras en promedio:  {top_marcas.round(2)}")
# %% [markdown]
# Marcas como Bugatti, Maybach y Lamborghini tienen los precios más elevados por su exclusividad, lujo y calidad, ya que están dirigidas a un público con alto poder adquisitivo.

# %% 
ultra_hp = df[df['Engine HP'] > 500]
print(f"Cantidad de autos con más de 500 HP: {len(ultra_hp)}")
print(ultra_hp[['Make', 'Model', 'Engine HP', 'MSRP']])
# %% [markdown]
# Los autos que superan los 500 HP suelen ser deportivos de lujo, diseñados para ofrecer mucha potencia y velocidad. Por eso, generalmente tienen precios bastante altos.

# %%
electricos = df[df['Engine Cylinders'] == 0]
print(f" Total de vehículos con 0 cilindros: {len(electricos)}")
if len(electricos) > 0:
    print(electricos[['Make', 'Model', 'MSRP']])

# %% [markdown]
# Este filtro permite identificar principalmente los autos eléctricos, que funcionan sin un motor de combustión tradicional y muestran cómo está cambiando la industria automotriz.

# %%
familiares_accesibles = df[(df['Number of Doors'] == 4) & (df['Year'] >= 2015) & (df['MSRP'] < 25000)]
print(f"Cantidad de autos familiares modernos y accesibles: {len(familiares_accesibles)}")
print(familiares_accesibles[['Make', 'Model', 'Year', 'MSRP']])



# %% [markdown]
# Hay una buena variedad de vehículos de 4 puertas, modelos recientes y precios menores a $ 25.000. Esto demuestra que existen opciones prácticas y económicas para las familias.

# %%

deportivos_accesibles = df[(df['Number of Doors'] == 2) & (df['MSRP'] < 25000)]
print(f"Cantidad de autos deportivos de 2 puertas por menos de $25,000: {len(deportivos_accesibles)}")
print(deportivos_accesibles[['Make', 'Model', 'Year', 'MSRP']])

# %% [markdown]
# Aunque muchos autos de dos puertas son costosos, también existen modelos deportivos y compactos por menos de $25.000, pensados para personas que buscan un diseño más deportivo sin gastar tanto.
# %% [markdown]
# ## 7. Agrupación con groupby  (Integrante A)

# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)

# %%
sns.set_theme(style="whitegrid")

plt.figure(figsize=(10, 5))
sns.histplot(df[df['MSRP'] <= 150000]['MSRP'], bins=40, kde=True, color='royalblue')
plt.title('1. Distribución de Precios (MSRP <= $150,000)')
plt.xlabel('Precio (USD)')
plt.ylabel('Frecuencia')
plt.show()

# %% [markdown]
# La mayoría de los vehículos tienen precios entre $20.000 y $45.000 dólares pero  también hay algunos autos de lujo con precios mucho más altos, aunque son menos comunes.



# %%
plt.figure(figsize=(10, 5))
sns.scatterplot(data=df, x='Engine HP', y='MSRP', alpha=0.5, color='crimson')
plt.title('2. Potencia del Motor (HP) vs. Precio (MSRP)')
plt.xlabel('Caballos de Fuerza (HP)')
plt.ylabel('Precio (USD)')


# %% [markdown]
# Se observa que, en general, mientras más potencia tiene un vehículo, más alto es su precio. Esto se nota especialmente en los autos que superan los 400 HP.


# %%
plt.figure(figsize=(10, 5))
top_10_marcas = df['Make'].value_counts().head(10)
sns.barplot(x=top_10_marcas.values, y=top_10_marcas.index, hue=top_10_marcas.index, palette='viridis', legend=False)
plt.title('3. Top 10 Marcas con Mayor Presencia en el Dataset')
plt.xlabel('Cantidad de Vehículos')
plt.ylabel('Marca')
plt.show()


# %% [markdown]
# Chevrolet, Ford y Volkswagen son algunas de las marcas con mayor cantidad de vehículos en los datos. Esto muestra que las marcas más comerciales tienen una mayor presencia que las marcas de lujo.


# %%
plt.figure(figsize=(10, 5))
sns.boxplot(data=df[df['highway MPG'] < 60], x='Transmission Type', y='highway MPG', hue='Transmission Type', palette='Set2', legend=False)
plt.title('4. Rendimiento en Carretera por Tipo de Transmisión')
plt.xlabel('Tipo de Transmisión')
plt.ylabel('MPG en Carretera')
plt.xticks(rotation=25)
plt.show()



# %% [markdown]
# Los autos eléctricos e híbridos con transmisión directa muestran un mejor rendimiento energético. Por otro lado, los vehículos automáticos y manuales tienen resultados bastante parecidos.


# %%
plt.figure(figsize=(10, 6))
cols_numericas = ['Year', 'Engine HP', 'Engine Cylinders', 'highway MPG', 'city mpg', 'Popularity', 'MSRP']
corr = df[cols_numericas].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('5. Matriz de Correlación de Variables Numéricas')
plt.show()


# %% [markdown]
# Se observa que los autos con más caballos de fuerza suelen tener más cilindros. También hay una relación entre el consumo en ciudad y carretera. Además, los vehículos más potentes tienden a gastar más combustible.

# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)
```[cite: 1]