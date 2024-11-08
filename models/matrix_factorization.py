from sklearn.decomposition import TruncatedSVD
from data_processing.feature_extraction import create_user_item_matrix
from data_processing.data_ingestion import get_data
from data_processing.data_cleaning import clean_data
from config import redis_client
import pickle

def train_matrix_factorization():
    movie_data, user_reactions, _ = get_data()
    user_item_matrix, user_id_to_idx, movie_id_to_idx = create_user_item_matrix(user_reactions)
    
    # Entrenar SVD
    svd = TruncatedSVD(n_components=100)  # Ajusta el número de componentes
    latent_matrix = svd.fit_transform(user_item_matrix)
    
    # Serializar y almacenar en Redis
    redis_client.set("svd_model", pickle.dumps(svd))
    redis_client.set("user_item_matrix", user_item_matrix.tobytes())
    redis_client.set("latent_matrix", latent_matrix.tobytes())
    redis_client.set("user_id_to_idx", pickle.dumps(user_id_to_idx))
    redis_client.set("movie_id_to_idx", pickle.dumps(movie_id_to_idx))
    
    return svd, latent_matrix, user_id_to_idx, movie_id_to_idx

def load_matrix_factorization():
    svd = pickle.loads(redis_client.get("svd_model"))
    user_item_matrix = np.frombuffer(redis_client.get("user_item_matrix")).reshape(-1, len(redis_client.get("movie_id_to_idx")))
    latent_matrix = np.frombuffer(redis_client.get("latent_matrix")).reshape(-1, 100)
    user_id_to_idx = pickle.loads(redis_client.get("user_id_to_idx"))
    movie_id_to_idx = pickle.loads(redis_client.get("movie_id_to_idx"))
    return svd, latent_matrix, user_id_to_idx, movie_id_to_idx
