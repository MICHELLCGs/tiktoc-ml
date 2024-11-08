import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from models.tfidf_model import load_tfidf_model
from models.matrix_factorization import load_matrix_factorization
from models.engagement_model import load_engagement_scores
from data_processing.data_ingestion import get_data
from cache_manager import cache_set, cache_get
import pandas as pd

def get_recommendations(user_id, type="videos"):
    if type == "videos":
        return recommend_videos(user_id)
    elif type == "searches":
        return recommend_searches(user_id)
    else:
        return []

def recommend_videos(user_id):
    # Cargar modelos y datos
    svd, latent_matrix, user_id_to_idx, movie_id_to_idx = load_matrix_factorization()
    engagement = load_engagement_scores()
    
    # Obtener el índice del usuario
    user_idx = user_id_to_idx.get(user_id)
    if user_idx is None:
        return []
    
    # Calcular la puntuación de recomendación usando los factores latentes
    user_factors = latent_matrix[user_idx]
    scores = np.dot(latent_matrix, user_factors)
    
    # Incorporar el engagement score
    engagement_dict = dict(zip(engagement['movie_id'], engagement['engagement_score']))
    movie_scores = {}
    for movie_id, score in zip(movie_id_to_idx.keys(), scores):
        engagement_score = engagement_dict.get(movie_id, 0)
        movie_scores[movie_id] = score + engagement_score  # Ajusta la ponderación según sea necesario
    
    # Ordenar las películas por puntaje y filtrar ya vistas
    user_reactions = get_user_reactions(user_id)
    watched_movies = set(user_reactions['movie_id'].tolist())
    recommended = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
    recommended = [movie for movie in recommended if movie[0] not in watched_movies]
    
    # Retornar las top N recomendaciones
    return recommended[:10]

def recommend_searches(user_id):
    # Cargar TF-IDF y vectorizador
    tfidf_matrix, vectorizer = load_tfidf_model()
    
    # Obtener el historial de búsqueda del usuario
    _, _, search_history = get_data(user_id)
    if not search_history:
        return []
    
    # Procesar las búsquedas recientes
    recent_searches = [search['_source']['query'] for search in search_history]
    recent_tfidf = vectorizer.transform(recent_searches)
    
    # Calcular la media del TF-IDF para las búsquedas recientes
    mean_tfidf = recent_tfidf.mean(axis=0)
    
    # Calcular la similitud con todas las búsquedas posibles
    # Supongamos que tienes un conjunto de términos o queries populares
    # Aquí simplificamos retornando términos similares
    # Necesitarías ajustar esto según tu modelo de datos
    
    # Por ejemplo, podrías usar las palabras más relevantes del TF-IDF
    feature_array = np.array(vectorizer.get_feature_names_out())
    tfidf_sorting = np.argsort(mean_tfidf.toarray()).flatten()[::-1]
    
    top_n = feature_array[tfidf_sorting][:10]
    
    return top_n.tolist()

def get_user_reactions(user_id):
    # Implementa la función para obtener las reacciones del usuario desde PostgreSQL
    from data_processing.data_ingestion import get_user_reactions
    user_reactions = get_user_reactions()
    user_reactions = user_reactions[user_reactions['user_id'] == user_id]
    return user_reactions
