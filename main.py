# main.py
from data_processing.data_ingestion import get_data
from data_processing.data_cleaning import clean_data
from models.tfidf_model import train_tfidf_model
from models.matrix_factorization import train_matrix_factorization
from models.engagement_model import get_engagement_scores
from recommendation_engine.recommender import get_recommendations
from message_queue.event_listener import listen_for_events
import threading

def initialize_models():
    movie_data, user_reactions, search_history = get_data()
    movie_data, user_reactions, search_history = clean_data(movie_data, user_reactions, search_history)
    train_tfidf_model()
    train_matrix_factorization()
    get_engagement_scores()

def start_event_listener():
    listen_for_events()

def main():
    # Inicializar modelos
    initialize_models()
    
    # Iniciar el listener de eventos en un hilo separado
    listener_thread = threading.Thread(target=start_event_listener, daemon=True)
    listener_thread.start()
    
    # Generar recomendaciones para un usuario de ejemplo
    user_id = "user_123"  # Reemplaza con un ID de usuario real
    recommended_videos = get_recommendations(user_id, type="videos")
    recommended_searches = get_recommendations(user_id, type="searches")
    
    print("Videos Recomendados:", recommended_videos)
    print("Búsquedas Recomendadas:", recommended_searches)
    
    # Mantener el programa en ejecución para escuchar eventos
    listener_thread.join()

if __name__ == "__main__":
    main()
