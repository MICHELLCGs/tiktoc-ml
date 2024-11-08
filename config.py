import os
from sqlalchemy import create_engine
from redis import Redis
from elasticsearch import Elasticsearch
from kafka import KafkaProducer, KafkaConsumer

# Configuración de PostgreSQL
POSTGRES_USER = os.getenv('POSTGRES_USER', 'tu_usuario')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'tu_contraseña')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'tu_base_de_datos')

SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Configuración de Elasticsearch
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_PORT', '9200')
es = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}])

# Configuración de Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Configuración de Redpanda (usando Kafka API)
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'localhost:9092').split(',')
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)
consumer = KafkaConsumer('user_events', bootstrap_servers=KAFKA_BROKERS, auto_offset_reset='earliest')
