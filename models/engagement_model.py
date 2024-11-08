import pandas as pd
from data_processing.data_ingestion import get_data
from data_processing.data_cleaning import clean_data

def calculate_engagement(user_reactions):
    # Definir una métrica de engagement, por ejemplo, ponderar diferentes tipos de reacciones
    # Supongamos: like=1, comment=2, share=3
    reaction_weights = {'like': 1, 'comment': 2, 'share': 3}
    user_reactions['engagement_score'] = user_reactions['reaction'].map(reaction_weights)
    
    # Calcular el score total por video
    engagement = user_reactions.groupby('movie_id')['engagement_score'].sum().reset_index()
    return engagement

def get_engagement_scores():
    movie_data, user_reactions, _ = get_data()
    user_reactions = clean_data(movie_data, user_reactions, [])  # Limpieza básica
    engagement = calculate_engagement(user_reactions)
    
    # Almacenar en Redis
    redis_client.set("engagement_scores", engagement.to_json())
    
    return engagement

def load_engagement_scores():
    engagement_json = redis_client.get("engagement_scores")
    if engagement_json:
        engagement = pd.read_json(engagement_json)
        return engagement
    else:
        return get_engagement_scores()
