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
# ## 2. Manejo de datos faltantes  (Integrante B)

# %% [markdown]
# ##3. Manejo de outliers (Juan David)
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
# ## 4. Valores inconsistentes y duplicados  (Integrante B)

# %% [markdown]
# ## 5. Creación de variables  (Juan David)
# %%
df["Avg MPG"] = (df["highway MPG"] + df["city mpg"]) / 2
df[["highway MPG", "city mpg", "Avg MPG"]].head()

# %%
df["Car Age"] = df["Year"].max() - df["Year"]
df[["Year", "Car Age"]].head()

# %%
df["Price Category"] = pd.cut(
    df["MSRP"],
    bins=[0, 20000, 40000, 80000, df["MSRP"].max()],
    labels=["Económico", "Medio", "Alto", "Lujo"]
)
df["Price Category"].value_counts()

# %% [markdown]
# Conclusión: se crearon tres variables nuevas. Avg MPG resume el consumo en un solo valor (promedio de ciudad y carretera). Car Age indica la antigüedad del carro respecto al año más reciente del dataset (2017). Price Category agrupa el precio (MSRP) en cuatro categorías: Económico (hasta 20.000 USD), Medio (20.000 a 40.000), Alto (40.000 a 80.000) y Lujo (más de 80.000). La categoría más común es Medio (alrededor del 49 % de los carros) y la menos común es Lujo (alrededor del 7,5 %), lo que muestra que la mayoría de los carros se concentra en precios medios.
# %% [markdown]
# ## 6. Filtrado y condiciones en pandas  (Integrante B)

# %% [markdown]
# ## 7. Agrupación con groupby  (juan david)
# %%
df.groupby("Make")["MSRP"].mean().sort_values(ascending=False).head(10)

# %% [markdown]
#las marcas más caras en promedio son Bugatti, Maybach y Rolls-Royce. Todas son marcas de lujo y superdeportivos, lo que confirma que los outliers de precio son reales.

# %%
df.groupby("Year")["MSRP"].median()

# %% [markdown]
#de 2001 a 2017 la mediana del precio sube de forma casi constante. Entre 1990 y 1996 la mediana es exactamente 2.000 USD, lo que parece un valor por defecto y no un precio real.

# %%
df.groupby("Driven_Wheels")[["Engine HP", "Avg MPG", "MSRP"]].mean()

# %% [markdown]
#los carros de tracción trasera tienen más potencia y los de tracción delantera son los más eficientes y los más baratos. Los de tracción total y trasera son los más caros.

# %%
df.groupby("Engine Fuel Type")["MSRP"].agg(["count", "mean"]).sort_values("count", ascending=False)

# %% [markdown]
#la gasolina regular domina el conjunto (7.172 carros) y es la más barata en promedio (cerca de 23 mil USD). Los que exigen gasolina premium tienen un precio promedio mucho mayor (cerca de 101 mil USD), porque ahi estan los carros de lujo y deportivos.

# %%
df.groupby("Price Category", observed=True)[["Engine HP", "Avg MPG", "Car Age"]].mean()

# %% [markdown]
#a mayor categoría de precio, mayor potencia, en cambio el consumo empeora en Lujo. La categoría Económico tiene la antigüedad promedio más alta, lo que muestra que los carros baratos del conjunto son viejos.
# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)

# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)