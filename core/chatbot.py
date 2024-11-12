# core/chatbot.py

from typing import Optional
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from core.agents import create_llm, create_faq_agent, create_transaction_agent
from tools.faq_tools import FAQTools
from tools.transaction_tools import TransactionTools
from core.chat_history import SessionManager
import re
import logging

logger = logging.getLogger(__name__)

class Chatbot:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.session_manager = SessionManager()
        
        # Initialize LLM
        self.llm = create_llm()
        
        # Initialize tools
        self.faq_tools = FAQTools()
        self.transaction_tools = TransactionTools()
        
        # Initialize agents
        self.faq_agent = create_faq_agent(self.llm, self.faq_tools.get_tools())
        self.transaction_agent = create_transaction_agent(self.llm, self.transaction_tools.get_tools())
        
        # Create agent executors with message history
        self.faq_agent_executor = RunnableWithMessageHistory(
            AgentExecutor(
                agent=self.faq_agent,
                tools=self.faq_tools.get_tools(),
                handle_parsing_errors=True,
                max_iterations=3,
                return_intermediate_steps=True
            ).with_config({"run_name": "FAQ_Agent"}),
            lambda session_id: self.session_manager.get_session(session_id),
            input_messages_key="input",
            history_messages_key="chat_history"
        )

        self.transaction_agent_executor = RunnableWithMessageHistory(
            AgentExecutor(
                agent=self.transaction_agent,
                tools=self.transaction_tools.get_tools(),
                handle_parsing_errors=True,
                max_iterations=3,
                return_intermediate_steps=True
            ).with_config({"run_name": "Transaction_Agent"}),
            lambda session_id: self.session_manager.get_session(session_id),
            input_messages_key="input",
            history_messages_key="chat_history"
        )
        
        self.current_owner = None

    def process_query(self, query: str, force_type: Optional[str] = None) -> str:
        """
        Procesa una consulta y determina si debe ser manejada por el agente FAQ o el de transacciones
        """
        try:
            if force_type == "transaction":
                return self._handle_transaction_query(query)
            elif force_type == "faq":
                return self._handle_faq_query(query)
            
            # Auto-detect query type
            if self._is_transaction_query(query):
                return self._handle_transaction_query(query)
            return self._handle_faq_query(query)
        
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return "Lo siento, ocurrió un error al procesar tu consulta."

    def _is_transaction_query(self, query: str) -> bool:
        """
        Determina si una consulta está relacionada con transacciones
        """
        transaction_keywords = {
            "saldo", "cuenta", "gastos", "compras", "transferencia",
            "movimientos", "cliente", "recurrente", "pago"
        }
        has_quotes = bool(re.search(r"['\"](.*?)['\"]", query))
        words = set(query.lower().split())
        return has_quotes or bool(words & transaction_keywords)

    def _handle_faq_query(self, query: str) -> str:
        """
        Maneja las consultas relacionadas con FAQs
        """
        try:
            # Obtener el contexto de las FAQs
            faq_context = self.faq_tools.search_faqs(query)
            
            if not faq_context or faq_context == "No se encontró información relevante.":
                return "Lo siento, no encontré información específica sobre tu pregunta en las FAQs. ¿Podrías reformularla o ser más específico?"
            
            # Enriquecer la consulta con el contexto
            enriched_query = f"""Consulta del usuario: {query}

Contexto de las FAQs:
{faq_context}

Por favor, proporciona una respuesta clara y concisa basada en esta información, citando las referencias relevantes."""

            # Procesar la consulta con el agente FAQ
            response = self.faq_agent_executor.invoke(
                {
                    "input": enriched_query,
                },
                {"session_id": self.session_id}
            )
            
            # Actualizar el historial de chat
            chat_history = self.session_manager.get_session(self.session_id)
            chat_history.add_message(HumanMessage(content=query))
            chat_history.add_message(AIMessage(content=response["output"]))
            
            return response["output"]
            
        except Exception as e:
            logger.error(f"Error processing FAQ query: {e}")
            return "Lo siento, ocurrió un error al procesar tu consulta sobre las FAQs."

    def _handle_transaction_query(self, query: str) -> str:
        """
        Maneja las consultas relacionadas con transacciones
        """
        try:
            # Extraer el nombre del cliente entre comillas si existe
            client_match = re.search(r"['\"](.*?)['\"]", query)
            
            # Si hay un cliente especificado en la consulta
            if client_match:
                potential_owner = client_match.group(1)
                # Validar si el cliente existe
                if self.transaction_tools.validate_owner(potential_owner):
                    self.current_owner = potential_owner
                else:
                    clients_list = self.transaction_tools.list_owners()
                    return f"El cliente '{potential_owner}' no fue encontrado.\n{clients_list}"
            
            # Si no hay cliente en la consulta y no es una solicitud de lista
            if not self.current_owner and not any(keyword in query.lower() for keyword in ["lista", "clientes", "disponibles"]):
                clients_list = self.transaction_tools.list_owners()
                return f"Por favor, especifica un cliente de la siguiente lista:\n{clients_list}"
            
            # Procesar la consulta con el agente de transacciones
            response = self.transaction_agent_executor.invoke(
                {
                    "input": query,
                },
                {"session_id": self.session_id}
            )
            
            # Actualizar el historial de chat
            chat_history = self.session_manager.get_session(self.session_id)
            chat_history.add_message(HumanMessage(content=query))
            chat_history.add_message(AIMessage(content=response["output"]))
            
            # Mantener el tamaño del historial
            if len(chat_history.messages) > 10:
                chat_history.messages = chat_history.messages[-10:]
            
            return response["output"]
            
        except Exception as e:
            logger.error(f"Error processing transaction query: {e}")
            return "Lo siento, ocurrió un error al procesar tu consulta sobre transacciones."