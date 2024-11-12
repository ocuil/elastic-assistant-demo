import streamlit as st
from ui.constants import PRESET_QUESTIONS

def render_sidebar():
    if st.sidebar.button("🔄 Reiniciar Conversación"):
        return True
    
    with st.sidebar.expander("ℹ️ Información de uso"):
        st.markdown("""
        ### Tipos de consultas disponibles:
        
        1. **Consultas de FAQ:**
           - Preguntas generales sobre servicios bancarios
           - Políticas y procedimientos
           - Información sobre productos
        
        2. **Consultas de transacciones:**
           - Saldo de cuenta
           - Historial de gastos
           - Transacciones recurrentes
           - Lista de clientes
        
        ### Consejos:
        - Puedes usar los botones de preguntas predefinidas para consultas comunes
        - Para consultas de transacciones, asegúrate de especificar el cliente entre comillas
        - Usa el botón "Reiniciar" para comenzar una nueva conversación
        - Sé específico en tus preguntas para obtener mejores respuestas
        """)

def render_chat_history(chat_history):
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def render_preset_questions(process_query_callback):
    st.markdown("#### Preguntas Frecuentes:")
    cols = st.columns(len(PRESET_QUESTIONS))
    
    for col, (label, question_data) in zip(cols, PRESET_QUESTIONS.items()):
        if col.button(label, key=f"preset_{label}", use_container_width=True):
            process_query_callback(question_data["question"], question_data["type"])