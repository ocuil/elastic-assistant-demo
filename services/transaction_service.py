from typing import List, Dict
from datetime import datetime, timedelta
from services.elasticsearch_service import ElasticsearchService
from config.settings import BALANCES_INDEX
import logging

logger = logging.getLogger(__name__)

class TransactionService:
    def __init__(self):
        self.es_service = ElasticsearchService()
    
    def get_owners(self) -> List[str]:
        try:
            query = {
                "size": 0,
                "aggs": {
                    "owners": {
                        "terms": {
                            "field": "owner.keyword",
                            "size": 100
                        }
                    }
                }
            }
            result = self.es_service.search(BALANCES_INDEX, query)
            return [bucket["key"] for bucket in result["aggregations"]["owners"]["buckets"]]
        except Exception as e:
            logger.error(f"Error listing owners: {e}")
            return []

    def validate_owner(self, owner: str) -> bool:
        try:
            query = {
                "query": {
                    "term": {
                        "owner.keyword": owner
                    }
                },
                "size": 0
            }
            result = self.es_service.search(BALANCES_INDEX, query)
            return result["hits"]["total"]["value"] > 0
        except Exception as e:
            logger.error(f"Error validating owner: {e}")
            return False

    def get_account_balance(self, owner: str) -> str:
        try:
            query = {
                "size": 1,
                "sort": [{"@timestamp": "desc"}],
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"owner.keyword": owner}}
                        ]
                    }
                }
            }
            
            result = self.es_service.search(BALANCES_INDEX, query)
            
            if result["hits"]["hits"]:
                hit = result["hits"]["hits"][0]["_source"]
                balance = hit["balance_after_transaction"]
                return f"Saldo actual para {owner}: ${balance:,.2f}"
            return f"No se encontró información de saldo para {owner}."
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return "Error al obtener el saldo."

    def get_top_purchases(self, owner: str, days: int = 30) -> str:
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"owner.keyword": owner}},
                            {"range": {"@timestamp": {"gte": start_date.isoformat()}}},
                            {"range": {"amount": {"lt": 0}}}
                        ]
                    }
                },
                "aggs": {
                    "by_category": {
                        "terms": {
                            "field": "category",
                            "size": 5
                        },
                        "aggs": {
                            "total_spent": {
                                "sum": {"field": "amount"}
                            }
                        }
                    }
                },
                "size": 0
            }
            
            result = self.es_service.search(BALANCES_INDEX, query)
            
            categories = []
            total_spent = 0
            for bucket in result["aggregations"]["by_category"]["buckets"]:
                amount = abs(bucket["total_spent"]["value"])
                total_spent += amount
                categories.append(f"  {bucket['key']}: ${amount:,.2f}")
            
            if categories:
                response = [f"Top gastos para {owner} en los últimos {days} días:"]
                response.extend(categories)
                response.append(f"\nGasto total: ${total_spent:,.2f}")
                return "\n".join(response)
            return f"No se encontraron transacciones para {owner} en los últimos {days} días."
        except Exception as e:
            logger.error(f"Error getting top purchases: {e}")
            return "Error al obtener los gastos."

    def get_recurring_transactions(self, owner: str) -> str:
        try:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"owner.keyword": owner}},
                            {"term": {"is_recurring": True}}
                        ]
                    }
                },
                "aggs": {
                    "by_description": {
                        "terms": {
                            "field": "description.keyword",
                            "size": 10
                        },
                        "aggs": {
                            "avg_amount": {
                                "avg": {"field": "amount"}
                            }
                        }
                    }
                },
                "size": 0
            }
            
            result = self.es_service.search(BALANCES_INDEX, query)
            
            transactions = []
            for bucket in result["aggregations"]["by_description"]["buckets"]:
                amount = abs(bucket["avg_amount"]["value"])
                transactions.append(f"  {bucket['key']}: ${amount:,.2f}")
            
            if transactions:
                response = [f"Transacciones recurrentes para {owner}:"]
                response.extend(transactions)
                return "\n".join(response)
            return f"No se encontraron transacciones recurrentes para {owner}."
        except Exception as e:
            logger.error(f"Error getting recurring transactions: {e}")
            return "Error al obtener las transacciones recurrentes."