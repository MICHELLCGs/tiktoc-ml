# data_processing/feature_extraction.py
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from config import redis_client

def compute_tfidf(movie_descriptions):
    vectorizer = TfidfVectorizer(max_features=5000)  # Ajusta según tus necesidades
    tfidf_matrix = vectorizer.fit_transform(movie_descriptions)
    feature_names = vectorizer.get_feature_names_out()
    return tfidf_matrix, feature_names, vectorizer

def save_tfidf_to_redis(user_id, tfidf_matrix, vectorizer):
    # Serializar la matriz TF-IDF y el vectorizador si es necesario
    # Aquí se puede optar por almacenar el vectorizador globalmente
    redis_client.set(f"tfidf_matrix_{user_id}", tfidf_matrix.toarray().tobytes())
    # Guarda el vectorizador en otro lugar o reentrena según sea necesario

def create_user_item_matrix(user_reactions):
    # Suponiendo que user_reactions tiene columnas 'user_id', 'movie_id', 'reaction'
    user_ids = user_reactions['user_id'].unique()
    movie_ids = user_reactions['movie_id'].unique()
    user_id_to_idx = {user_id: idx for idx, user_id in enumerate(user_ids)}
    movie_id_to_idx = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}
    
    matrix = np.zeros((len(user_ids), len(movie_ids)))
    for _, row in user_reactions.iterrows():
        user_idx = user_id_to_idx[row['user_id']]
        movie_idx = movie_id_to_idx[row['movie_id']]
        matrix[user_idx, movie_idx] = row['reaction']  # Puedes ponderar las reacciones
    
    return matrix, user_id_to_idx, movie_id_to_idx
