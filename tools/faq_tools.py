from langchain.tools import Tool
from services.faq_service import FAQService

class FAQTools:
    def __init__(self):
        self.faq_service = FAQService()
    
    def search_faqs(self, query: str) -> str:
        try:
            results = self.faq_service.get_elasticsearch_results(query)
            if not results:
                return "No se encontró información relevante."
            
            context = []
            for i, hit in enumerate(results, 1):
                pregunta = hit.get("_source", {}).get("pregunta", "")
                respuesta = hit.get("_source", {}).get("respuesta", "")
                
                if pregunta and respuesta:
                    context.append(f"Referencia {i}:\nPregunta: {pregunta}\nRespuesta: {respuesta}")
            
            return "\n\n".join(context)
        except Exception as e:
            logger.error(f"Error in FAQ search: {e}")
            return "Error al buscar en las FAQs."

    def get_tools(self):
        return [
            Tool(
                name="search_faqs",
                func=self.search_faqs,
                description="Busca información en las FAQs usando búsqueda semántica"
            )
        ]