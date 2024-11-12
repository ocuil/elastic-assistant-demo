from elasticsearch import Elasticsearch
from config.settings import ES_ENDPOINT, ES_API_KEY
import logging

logger = logging.getLogger(__name__)

class ElasticsearchService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = Elasticsearch(
                ES_ENDPOINT,
                api_key=ES_API_KEY
            )
        return cls._instance

    def search(self, index: str, body: dict) -> dict:
        try:
            return self.client.search(index=index, body=body)
        except Exception as e:
            logger.error(f"Error en búsqueda de Elasticsearch: {e}")
            raise