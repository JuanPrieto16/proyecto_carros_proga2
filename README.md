# proyecto_carros_proga2
## Integrantes 
-Juan David Prieto (Integrante A)
-Samuel Betancourt Merchan (Integrante B)
## Fuente de los datos
https://www.kaggle.com/datasets/CooperUnion/cardataset #se encuentran caracteristicas de todo tipo de carros, modelos, precios, autonomias.


## Estructura de los datos
Número de registros : 11,914
- Número de variables : 16
- Qué representa cada fila: Cada registro  corresponde a una versión o configuración específica de un automóvil comercializado, detallando sus características técnicas de motorización, diseño, rendimiento y su precio de venta sugerido .
- Distribución de las variables:
  - Variables categóricas: Make, Model, Engine Fuel Type, Transmission Type, Driven_Wheels, Market Category, Vehicle Size, Vehicle Style.
  - Variables numéricas continuas : Engine HP, MSRP.
  - Variables numéricas discretas : Year, Engine Cylinders, Number of Doors, highway MPG, city mpg, Popularity.

## Diccionario de datos
| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `Make` | Categórica | Fabricante o marca del vehículo. | Texto |
| `Model` | Categórica | Nombre comercial del modelo del vehículo. | Texto |
| `Year` | Numérica discreta | Año de lanzamiento o fabricación del modelo. | Años |
| `Engine Fuel Type` | Categórica | Tipo de combustible requerido por el motor. | Texto |
| `Engine HP` | Numérica continua | Potencia del motor en caballos de fuerza. | Caballos de fuerza HP |
| `Engine Cylinders` | Numérica discreta | Número de cilindros del motor. | Enteros |
| `Transmission Type` | Categórica | Sistema de transmisión del vehículo. | Texto |
| `Driven_Wheels` | Categórica | Configuración de las ruedas motrices o tracción. | Texto |
| `Number of Doors` | Numérica discreta | Cantidad de puertas del vehículo. | Enteros |
| `Market Category` | Categórica | Segmento o nicho comercial al que pertenece el vehículo. | Texto |
| `Vehicle Size` | Categórica | Clasificación del tamaño general del vehículo. | Texto |
| `Vehicle Style` | Categórica | Estilo de carrocería del automóvil. | Texto |
| `highway MPG` | Numérica discreta | Eficiencia de combustible estimada en carretera. | Millas por galón o MPGe |
| `city mpg` | Numérica discreta | Eficiencia de combustible estimada en entorno urbano. | Millas por galón o MPGe |
| `Popularity` | Numérica discreta | Índice o contador de popularidad de la marca en la plataforma. | Valores enteros positivos |
| `MSRP` | Numérica continua | Precio de venta sugerido por el fabricante o variable objetivo. | Dólares estadounidenses USD |

## Organización del repositorio
`analisis.py`: solución final del proyecto, dividida en celdas con sus conclusiones.

`cuadernos/`: cuadernos de exploración de cada integrante (`exploracion_juan.ipynb` y `exploracion_samuel.ipynb`).

`datos/`: base de datos descargada de Kaggle (`data.csv`).

## Conclusiones
1. El conjunto tiene 11.914 registros y 16 variables (8 categóricas, 4 numéricas continuas y 4 discretas). Los datos faltantes se concentran en Market Category (3.742); en Engine HP (69) y Engine Cylinders (30) son pocos y se imputaron con la mediana y la moda. Además se eliminaron los registros duplicados y se estandarizó el texto para evitar categorías repetidas.
2. Los filtros muestran que las marcas más caras son de lujo (Bugatti, Maybach, Rolls-Royce) y que los autos con más de 500 HP son deportivos de alto precio. Aun así, hay opciones accesibles: carros familiares de 4 puertas, recientes y por menos de 25.000 USD.
3. El precio está sesgado por los carros de lujo: el promedio (cerca de 40.600 USD) supera con claridad a la mediana (cerca de 29.995 USD). Hay 996 outliers (8,36 %) sobre 74.078 USD, pero son precios reales, por eso se conservaron.
4. El tipo de combustible se relaciona con el precio: la gasolina regular domina el conjunto y es la más barata en promedio (cerca de 23 mil USD), mientras que los carros que exigen gasolina premium tienen un precio promedio mucho mayor (cerca de 100 mil USD), porque ahí están los deportivos y de lujo. Los eléctricos son muy pocos, por lo que su peso en el análisis es pequeño.
5. Con las variables creadas se vio que a mayor categoría de precio hay más potencia (de cerca de 155 HP en Económico a cerca de 496 HP en Lujo) y peor consumo. La tracción delantera es la más eficiente y barata, y la trasera la más potente y cara. El precio mediano sube con los años desde 2001, y los eléctricos tienen MPG no comparables con los de gasolina, por lo que conviene analizarlos aparte.
