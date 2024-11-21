'''from data_processing.data_ingestion import get_data
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
    user_id = "user_123"
    recommended_videos = get_recommendations(user_id, type="videos")
    recommended_searches = get_recommendations(user_id, type="searches")
    
    print("Videos Recomendados:", recommended_videos)
    print("Búsquedas Recomendadas:", recommended_searches)
    

    listener_thread.join()

if __name__ == "__main__":
    main()'''

from data_processing.data_ingestion import get_data_from_db
from data_processing.data_cleaning import clean_data
from models.tfidf_model import train_tfidf_model
from models.matrix_factorization import train_matrix_factorization
from models.engagement_model import calculate_engagement_scores
from recommendation_engine.recommender import get_recommendations
from message_queue.event_listener import listen_for_events
import threading


def initialize_models():
    """
    Inicializa modelos y carga datos desde la base de datos.
    """
    # Obtener datos desde PostgreSQL
    movie_data, user_profiles, user_reactions = get_data_from_db()

    # Limpiar y procesar los datos
    movie_data, user_profiles, user_reactions = clean_data(movie_data, user_profiles, user_reactions)

    # Entrenar modelos
    print("Entrenando modelo TF-IDF...")
    train_tfidf_model(movie_data)
    print("Entrenando modelo de factorización matricial...")
    train_matrix_factorization(user_profiles, user_reactions)
    print("Calculando puntajes de engagement...")
    calculate_engagement_scores(user_profiles, movie_data)


def start_event_listener():
    """
    Inicia el servicio para escuchar eventos de la cola de mensajes.
    """
    listen_for_events()


def main():
    """
    Programa principal que inicializa los modelos, escucha eventos y genera recomendaciones.
    """
    # Inicializar modelos
    print("Inicializando modelos...")
    initialize_models()

    # Iniciar el listener de eventos en un hilo separado
    print("Iniciando el listener de eventos...")
    listener_thread = threading.Thread(target=start_event_listener, daemon=True)
    listener_thread.start()

    # Generar recomendaciones para un usuario de ejemplo
    user_id = 1  # ID de ejemplo para un usuario registrado
    print(f"Generando recomendaciones para el usuario con ID: {user_id}...")
    recommended_movies = get_recommendations(user_id, type="movies")

    # Mostrar resultados
    print("Películas recomendadas:", recommended_movies)

    # Esperar el hilo del listener (si no es deamon, puedes manejarlo distinto)
    listener_thread.join()


if __name__ == "__main__":
    main()

