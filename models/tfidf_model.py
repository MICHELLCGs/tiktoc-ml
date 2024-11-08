# models/tfidf_model.py
from data_processing.feature_extraction import compute_tfidf
from data_processing.data_cleaning import clean_data
from data_processing.data_ingestion import get_data
from config import redis_client
import pickle

def train_tfidf_model():
    movie_data, _, _ = get_data()
    movie_descriptions = movie_data['description']  # Ajusta según tu esquema
    tfidf_matrix, feature_names, vectorizer = compute_tfidf(movie_descriptions)
    
    # Serializar el modelo y almacenarlo en Redis
    redis_client.set("tfidf_vectorizer", pickle.dumps(vectorizer))
    redis_client.set("tfidf_matrix", tfidf_matrix.toarray().tobytes())
    
    return tfidf_matrix, feature_names, vectorizer

def load_tfidf_model():
    vectorizer = pickle.loads(redis_client.get("tfidf_vectorizer"))
    tfidf_matrix = np.frombuffer(redis_client.get("tfidf_matrix")).reshape(-1, len(vectorizer.get_feature_names_out()))
    return tfidf_matrix, vectorizer
