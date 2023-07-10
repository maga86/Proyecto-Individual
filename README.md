![](https://blog.soyhenry.com/content/images/2021/05/PRESENTACION-3.jpg)
# Primer Proyecto Individual
## Machine Learning Operations (MLOps)
![](https://www.go4it.solutions/sites/default/files/2021-06/05.01.%20Qu%C3%A9%20es%20el%20Machine%20Learning.jpg)

El proyecto se plantea a partir de un data set con información de películas, al cual se le realizan un trabajo de Data Engineering haciendo una serie de transformaciones para luego llevar a cabo  los endpoints pedidos y un modelo de recomendación de películas utilizando Machine Learning, a través de una API.

### Dataset:

El [Dataset](https://github.com/maga86/Proyecto-Individual/blob/main/movies_dataset.xlsx) en cuestión posee información acerca de películas y distintos atributos de las mismas. El mismo cuenta con 45466 filas (representando cada fila una película) y 24 columnas (atributos de cada título).

### Diccionario de Datos:

- adult: Indica si la película tiene califiación X, exclusiva para adultos.
- belongs_to_collection: Un diccionario que indica a que franquicia o serie de películas pertenece la película.
- budget: El presupuesto de la película, en dólares.
- genres: Un diccionario que indica todos los géneros asociados a la película.
- homepage: La página web oficial de la película.
- id: ID de la película.
- imdb_id: IMDB ID de la película.
- original_language: Idioma original en la que se grabo la película.
- original_title: Título original de la película.
- overview: Pequeño resumen de la película.
- popularity: Puntaje de popularidad de la película, asignado por TMDB (TheMoviesDataBase).
- poster_path: URL del póster de la película.
- production_companies: Lista con las compañias productoras asociadas a la película.
- production_countries: Lista con los países donde se produjo la película.
- release_date: Fecha de estreno de la película.
- revenue: Recaudación de la pelicula, en dolares.
- runtime: Duración de la película, en minutos.
- spoken_languages: Lista con los idiomas que se hablan en la película.
- status: Estado de la película actual (si fue anunciada, si ya se estreno, etc).
- tagline: Frase celebre asociadaa la película.
- title: Titulo de la película.
- video: Indíca si hay o no un trailer en video disponible en TMDB.
- vote_average: Puntaje promédio de reseñas de la película.
- vote_count: Números de votos recibidos por la película, en TMDB.


### Librerias y herramientas utilizadas en el proyecto:

- Scikit Learn: Utilizado para vectorizar, tokenizar y calcular la similitud coseno.
- Python: Lenguaje de programación principal utilizado en el desarrollo del proyecto.
- Numpy: Utilizado para realizar operaciones numéricas y manipulación de datos.
- Pandas: Utilizado para la manipulación y análisis de datos estructurados.
- Matplotlib: Utilizado para la visualización de datos y generación de gráficos.
- FastAPI: Utilizado para crear la interfaz de la aplicación y procesar los parámetros de funciones.
- Uvicorn: Servidor ASGI utilizado para ejecutar la aplicación FastAPI.
- Render: Plataforma utilizada para el despliegue del modelo y la aplicación.

   ## DESARROLLO DEL PROYECTO:

### Data Engineering:

En el ámbito de la Ingeniería de Datos, se llevó a cabo un conjunto de transformaciones requeridas :

- Algunos campos, como belongs_to_collection, production_companies y otros (ver diccionario de datos) están anidados, deberan ser desanidados, o bien buscar una forma para trabajarlos anidados.

- Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.

- Los valores nulos del campo release date deben eliminarse.

- De haber fechas, deberán tener el formato AAAA-mm-dd, además deberán crear la columna release_year donde extraerán el año de la fecha de estreno.

- Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, deberá tomar el valor 0.

- Eliminar las columnas que no serán utilizadas, video,imdb_id,adult,original_title,poster_path y homepage.

Se pueden visualizar las transformaciones y los análisis realizados en el [Proyecto 1 ETL.ipynb](https://github.com/maga86/Proyecto-Individual/blob/main/Proyecto_1_ETL.ipynb)

### Desarrollo API:
Se crearon 6 funciones para los endspoint quer se consumiran en la Api utilizando el framework FastApi :

- def peliculas_idioma( Idioma: str ): Se ingresa un idioma (como están escritos en el dataset, no hay que traducirlos!). Debe devolver la cantidad de películas producidas en ese idioma.
                    Ejemplo de retorno: X cantidad de películas fueron estrenadas en idioma

- def peliculas_duracion( Pelicula: str ): Se ingresa una pelicula. Debe devolver la duracion y el año.
                    Ejemplo de retorno: X . Duración: x. Año: xx

- def franquicia( Franquicia: str ): Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio
                    Ejemplo de retorno: La franquicia X posee X peliculas, una ganancia total de x y una ganancia promedio de xx

- def peliculas_pais( Pais: str ): Se ingresa un país (como están escritos en el dataset, no hay que traducirlos!), retornando la cantidad de peliculas producidas en el mismo.
                    Ejemplo de retorno: Se produjeron X películas en el país X

- def productoras_exitosas( Productora: str ): Se ingresa la productora, entregandote el revunue total y la cantidad de peliculas que realizo.
                    Ejemplo de retorno: La productora X ha tenido un revenue de x

 - def get_director( nombre_director ): Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista.
   Se puede visualizar los Endspoints realizados en el archivo: [main.py](https://github.com/maga86/Proyecto-Individual/blob/main/main.py)

 
### Análisis exploratorio de datos:

A los efectos de poder entender los datos presentados realice una transformación,la cual no fue pedida en el trabajo, para que visualmente el dataset fuera mas accesible: renombre las columnas utilizando  el formato Camel Case Y reordene las columnas.

Se realizaron una serie de análisis y estudios sobre las variables del dataset a para  poder encontrar relaciones entre los datos y comprender la relevancia de los mismos. Dentro de los análisis efectuados se encuentran gráficos de palabras gráficos de barras comparando columna, distribuciones de frecuencias de las variables numéricas, identificación de variables categóricas y sus valores, correlación entre variables, detección de outliers, análisis temporales y por categoría.
Se puede visualizar el Análisis exploratorio en el archivo:[Proyecto1 EDA.ipynb](https://github.com/maga86/Proyecto-Individual/blob/main/Proyecto1_EDA.ipynb)


### Deployed:

Para el deploy de la API, se utilizó la plataforma Render. Los datos están listos para ser consumidos y consultados a partir del siguiente link: https://api-brrw.onrender.com/docs.

### Video:
