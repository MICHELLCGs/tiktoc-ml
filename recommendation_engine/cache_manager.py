# recommendation_engine/cache_manager.py
import pickle
from config import redis_client

def cache_set(key, value, ex=3600):
    # Serializar con pickle si es necesario
    if isinstance(value, (dict, list, pd.DataFrame)):
        value = pickle.dumps(value)
    redis_client.set(key, value, ex=ex)

def cache_get(key):
    value = redis_client.get(key)
    if value:
        try:
            return pickle.loads(value)
        except:
            return value
    return None
