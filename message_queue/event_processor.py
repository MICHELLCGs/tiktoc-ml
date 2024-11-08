# message_queue/event_processor.py
import json
from models.engagement_model import get_engagement_scores
from models.matrix_factorization import train_matrix_factorization
from models.tfidf_model import train_tfidf_model

def process_event(event):
    # Parsear el evento
    event_data = json.loads(event)
    
    # Dependiendo del tipo de evento, actualizar los modelos
    if event_data['type'] == 'reaction':
        # Reentrenar o actualizar el modelo de engagement
        get_engagement_scores()
        train_matrix_factorization()
    elif event_data['type'] == 'search':
        # Actualizar índices de búsqueda o modelos TF-IDF si es necesario
        train_tfidf_model()
    # Puedes añadir más tipos de eventos según tus necesidades
