import pandas as pd
from sqlalchemy import text
from config import engine, es

def get_movie_metadata():
    query = text("SELECT * FROM movies")  # Ajusta según tu esquema
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def get_user_reactions():
    query = text("SELECT * FROM user_reactions")  # Ajusta según tu esquema
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def get_search_history(user_id):
    # Supongamos que tienes un índice 'search_history' en Elasticsearch
    res = es.search(index="search_history", body={
        "query": {
            "term": {"user_id": user_id}
        }
    })
    return res['hits']['hits']

def get_data(user_id=None):
    movie_data = get_movie_metadata()
    user_reactions = get_user_reactions()
    if user_id:
        search_history = get_search_history(user_id)
    else:
        search_history = []
    return movie_data, user_reactions, search_history
