# data_processing/data_cleaning.py
import pandas as pd

def clean_movie_data(df):
    # Elimina duplicados
    df = df.drop_duplicates()
    # Rellena valores nulos
    df = df.fillna('')
    return df

def clean_user_reactions(df):
    # Elimina duplicados
    df = df.drop_duplicates()
    # Convierte tipos de datos si es necesario
    return df

def clean_search_history(search_history):
    # Convertir de Elasticsearch a DataFrame si es necesario
    if not search_history:
        return pd.DataFrame()
    df = pd.json_normalize(search_history)
    return df

def clean_data(movie_data, user_reactions, search_history):
    movie_data = clean_movie_data(movie_data)
    user_reactions = clean_user_reactions(user_reactions)
    search_history = clean_search_history(search_history)
    return movie_data, user_reactions, search_history
