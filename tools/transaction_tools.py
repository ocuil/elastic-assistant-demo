from langchain.tools import Tool
from services.transaction_service import TransactionService
import logging

logger = logging.getLogger(__name__)

class TransactionTools:
    def __init__(self):
        self.transaction_service = TransactionService()
    
    def list_owners(self, *args) -> str:
        """Get list of available owners/clients"""
        try:
            owners = self.transaction_service.get_owners()
            if not owners:
                return "No hay clientes disponibles en este momento."
            return "Clientes disponibles:\n" + "\n".join(f"- {owner}" for owner in owners)
        except Exception as e:
            logger.error(f"Error listing owners: {e}")
            return "Error al obtener la lista de clientes."
    
    def validate_owner(self, owner: str) -> bool:
        """Validate if owner exists"""
        try:
            return self.transaction_service.validate_owner(owner)
        except Exception as e:
            logger.error(f"Error validating owner: {e}")
            return False
    
    def get_account_balance(self, owner: str) -> str:
        """Get current account balance for a specific owner"""
        try:
            if not self.validate_owner(owner):
                return f"Cliente no encontrado: {owner}"
            
            return self.transaction_service.get_account_balance(owner)
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            return "Error al obtener el saldo de la cuenta."
    
    def get_top_purchases(self, owner: str, days: int = 30) -> str:
        """Get top purchase categories for specified owner and timeframe"""
        try:
            if not self.validate_owner(owner):
                return f"Cliente no encontrado: {owner}"
            
            return self.transaction_service.get_top_purchases(owner, days)
        except Exception as e:
            logger.error(f"Error getting top purchases: {e}")
            return "Error al obtener los principales gastos."
    
    def get_recurring_transactions(self, owner: str) -> str:
        """Get recurring transactions for an owner"""
        try:
            if not self.validate_owner(owner):
                return f"Cliente no encontrado: {owner}"
            
            return self.transaction_service.get_recurring_transactions(owner)
        except Exception as e:
            logger.error(f"Error getting recurring transactions: {e}")
            return "Error al obtener las transacciones recurrentes."
    
    def get_tools(self) -> list:
        """Return list of available tools for the agent"""
        return [
            Tool(
                name="list_owners",
                func=self.list_owners,
                description="Obtiene la lista de clientes disponibles"
            ),
            Tool(
                name="get_account_balance",
                func=self.get_account_balance,
                description="Obtiene el saldo actual. Parámetro requerido: owner (nombre del cliente)"
            ),
            Tool(
                name="get_top_purchases",
                func=self.get_top_purchases,
                description="Obtiene las principales categorías de gastos. Parámetros: owner (nombre del cliente), days (opcional, por defecto 30)"
            ),
            Tool(
                name="get_recurring_transactions",
                func=self.get_recurring_transactions,
                description="Obtiene las transacciones recurrentes. Parámetro requerido: owner (nombre del cliente)"
            )
        ]