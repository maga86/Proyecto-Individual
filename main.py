# Importamos las librerías
import pandas as pd 
import numpy as np
import sklearn
from fastapi import FastAPI
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.neighbors import NearestNeighbors

# Indicamos título y descripción de la API
app = FastAPI(title='PROYECTO INDIVIDUAL Nº1 ',
            description='Recomendaciones de Películas')

# Datasets
mov = pd.read_csv('final_movie.csv')
mov1 = pd.read_csv('Mov_mlops.csv')


@app.get('/Idioma_oiginal/({Idioma})')
def peliculas_idioma(Idioma:str):
    ''' Se ingresa un idioma debe devolver la cantidad de peliculas que fueron grabadas en dicho idioma'''
    count = 0
    for i in range(len(mov)):
     if mov['original_language']. iloc[i] == Idioma:
        count += 1
    resultado ={'CANTIDAD DE PELICULAS EN ESE IDIOMA': count}
    return resultado

@app.get('/Duración_Película/({Pelicula}')
def peliculas_duracion(Pelicula:str):
    '''Se ingresa una película se obtiene la película el duración y año'''
    pel_fil = mov[(mov['title']).str.contains(Pelicula, na = False)]
    duracion = pel_fil['runtime'].values[0] if not pel_fil.empty else None
    anio = pel_fil['release_year'].values[0] if not pel_fil.empty else None
    return{'PELICULA': Pelicula, 'DURACION': duracion, 'AÑO': anio}

@app.get('/Franquicia/({franquicia})')
def franquicia(franquicia:str):
    '''Se ingresa la franquicia, retornando la cantidad de películas, ganancia total y promedio.
    ''' 
   
    lista_peliculas_franquicia = mov[(mov['Franquicia'] == franquicia)].drop_duplicates(subset='id')

    
    cantidad_peliculas_franq = (lista_peliculas_franquicia).shape[0]
    revenue_franq = lista_peliculas_franquicia['revenue'].sum()
    promedio_franq = revenue_franq/cantidad_peliculas_franq

    return {'FRANQUICIA':franquicia, 'CANTIDAD':cantidad_peliculas_franq, 'GANANCIA TOTAL':revenue_franq, 'GANANCIA PROMEDIO':promedio_franq}
   
@app.get('/Películas_País/({pais})')
def peliculas_pais(pais:str):
    '''Se ingresa el país y se obtiene la cantidad de pelíulas producidas en ese país'''
    
    Filtro = mov[(mov['Country'] == pais)]
    Unicas = Filtro.drop_duplicates(subset='id')    
    Respuesta = Unicas.shape[0]
    
    return {'PAIS':pais, 'SE PRODUJERON':Respuesta}

@app.get('/Productoras_Exitosas/({productora})')
def productoras_exitosas(productora): 
    '''Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron
    ''' 
    peliculas_producidas = mov[(mov['Company'] == productora)].drop_duplicates(subset='id')

    cantidad_producida = (peliculas_producidas).shape[0]
    revenue_prod = peliculas_producidas['revenue'].sum()

    return {'PRODUCTORA':productora, 'REVENUE':revenue_prod, 'CANTIDAD':cantidad_producida}


@app.get("/Director/{director}")
def get_director(director:str):
   '''Se ingresa el nombre de un director devuelve una lista con las 5 peliculas creadas por el director pasado como parametro, devolviendo su retorno total, fecha de estreno y nombre de cada pelicula'''

   director_data = mov[mov['Director'].apply(lambda x: director in x if isinstance(x, (list, str)) else False)].head(5)
   ganancias_totales = director_data['revenue'].sum()
   peliculas = []
   for _, row in director_data.iterrows():
        titulo = row['title']
        fecha_estreno = row['release_date']
        retorno = row['return']
        costo = row['budget']
        ganancia = row['revenue']
        peliculas.append({'TITULO': titulo, 'ESTRENO': fecha_estreno, 'RETORNO':retorno, 'GANANCIA GENERADA':ganancia, 'COSTO': costo})
    
   return {'DIRECTOR': director, 'GANANCIA TOTAL': ganancias_totales, 'PELICULA': peliculas}

#SISTEMA DE RECOMENDACION:

# Aseguramos que los datos de la columna 'overview' sean strings
mov1['Overview'] = mov1['Overview'].fillna('').astype('str')

# Aseguramos que los datos de la columna 'genres' sean strings
mov1['Genre'] = mov1['Genre'].apply(lambda x: ' '.join(map(str, x)) if isinstance(x, list) else '')

# Reemplazamos los valores NaN con cadenas vacías en la columna 'production_companies'
mov1['Company'] = mov1['Company'].fillna('')

# Convertimos la columna 'production_companies' a string si es necesario
mov1['Company'] = mov1['Company'].apply(lambda x: ' '.join(map(str, x)) if isinstance(x, list) else x)

# Creamos una nueva columna combinando las características de interés
mov1['combined_features'] = mov1['Overview'] + ' ' + mov1['Genre'] + ' ' + mov1['Company']

# Convertimos todos los textos a minusculas para evitar duplicados
mov1['combined_features'] = mov1['combined_features'].str.lower()

#   Creamos una matriz de conteo usando CountVectorizer que convierte los textos en una matriz de frecuencias de palabras
cv = CountVectorizer(stop_words='english', max_features=5000)
count_matrix = cv.fit_transform(mov1['combined_features'])

# Creamos un modelo para encontrar los vecinos mas cercanos en un espacio de caracteristicas
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(count_matrix)

# Creamos un indice de titulos de peliculas y eliminamos los duplicados
indices = pd.Series(mov1.index, index=mov1[' Title']).drop_duplicates()

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    '''Ingresas un nombre de película y te recomienda 5 similares
    '''
    # Verificamos si el titulo ingresado se encuentra en el df
    if titulo not in mov1[' Title'].values:
        return 'La pelicula no se encuentra en el conjunto de la base de datos.'
    else:
        # Obtenemos el índice de la película que coincide con el título
        index = indices[titulo]

        # Obtenemos las puntuaciones de similitud de las 5 peliculas más cercanas
        distances, indices_knn = nn.kneighbors(count_matrix[index], n_neighbors=6)  

        # Obtenemos los indices de las peliculas
        movie_indices = indices_knn[0][1:]  

        # Devolvemos las 5 peliculas mas similares
        return {'lista recomendada': mov1[' Title'].iloc[movie_indices].tolist()}

