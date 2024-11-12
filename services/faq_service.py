from typing import List, Dict
from services.elasticsearch_service import ElasticsearchService
from config.settings import ES_INDEX
import logging

logger = logging.getLogger(__name__)

class FAQService:
    def __init__(self):
        self.es_service = ElasticsearchService()
    
    def get_elasticsearch_results(self, query: str) -> List[Dict]:
        try:
            es_query = {
                "retriever": {
                    "rrf": {
                        "retrievers": [
                            {
                                "standard": {
                                    "query": {
                                        "nested": {
                                            "path": "pregunta.inference.chunks",
                                            "query": {
                                                "knn": {
                                                    "field": "pregunta.inference.chunks.embeddings",
                                                    "query_vector_builder": {
                                                        "text_embedding": {
                                                            "model_id": "e5",
                                                            "model_text": query
                                                        }
                                                    }
                                                }
                                            },
                                            "inner_hits": {
                                                "size": 2,
                                                "name": "faqs.pregunta",
                                                "_source": ["pregunta.inference.chunks.text"]
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "standard": {
                                    "query": {
                                        "nested": {
                                            "path": "respuesta.inference.chunks",
                                            "query": {
                                                "knn": {
                                                    "field": "respuesta.inference.chunks.embeddings",
                                                    "query_vector_builder": {
                                                        "text_embedding": {
                                                            "model_id": "e5",
                                                            "model_text": query
                                                        }
                                                    }
                                                }
                                            },
                                            "inner_hits": {
                                                "size": 2,
                                                "name": "faqs.respuesta",
                                                "_source": ["respuesta.inference.chunks.text"]
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    }
                },
                "size": 5,
                "_source": ["pregunta", "respuesta"]
            }
            return self.es_service.search(ES_INDEX, es_query)["hits"]["hits"]
        except Exception as e:
            logger.error(f"Error in FAQ search: {e}")
            return []