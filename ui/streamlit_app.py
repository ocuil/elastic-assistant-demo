# ui/streamlit_app.py

import streamlit as st
from uuid import uuid4
from core.chatbot import Chatbot
from ui.components import render_sidebar, render_chat_history, render_preset_questions

class StreamlitApp:
    def __init__(self):
        self.initialize_session_state()
        
    def initialize_session_state(self):
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid4())
        if 'chatbot' not in st.session_state:
            st.session_state.chatbot = Chatbot(st.session_state.session_id)

    def clear_conversation(self):
        st.session_state.chat_history = []
        st.session_state.session_id = str(uuid4())
        st.session_state.chatbot = Chatbot(st.session_state.session_id)

    def process_query(self, query: str, force_type: str = None):
        with st.chat_message("user"):
            st.write(query)
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = st.session_state.chatbot.process_query(query, force_type)
                st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    def run(self):
        st.set_page_config(
            page_title="Asistente Bancario",
            page_icon="🏦",
            layout="centered"
        )

        st.title("🏦 Asistente ElasticBank")
        
        if render_sidebar():
            self.clear_conversation()
        
        chat_container = st.container()
        input_container = st.container()
        
        with chat_container:
            render_chat_history(st.session_state.chat_history)
        
        with input_container:
            if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
                self.process_query(prompt)
            
            st.write("")
            render_preset_questions(self.process_query)