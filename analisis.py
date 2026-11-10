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
# ## 3. Identificación de outliers  (Integrante A)

# %% [markdown]
# ## 4. Valores inconsistentes y duplicados  (Integrante B)

# %% [markdown]
# ## 5. Creación de variables  (Integrante A)

# %% [markdown]
# ## 6. Filtrado y condiciones en pandas  (Integrante B)

# %% [markdown]
# ## 7. Agrupación con groupby  (Integrante A)

# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)

# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)
```[cite: 1]