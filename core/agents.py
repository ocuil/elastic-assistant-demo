from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from config.settings import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    API_VERSION,
    DEPLOYMENT_ID
)

def create_llm():
    return AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=API_VERSION,
        deployment_name=DEPLOYMENT_ID,
        temperature=0
    )

def create_faq_agent(llm, tools):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres un asistente bancario especializado..."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("assistant", "{agent_scratchpad}")
    ])
    
    return create_openai_tools_agent(llm, tools, prompt=prompt)

def create_transaction_agent(llm, tools):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres un asistente financiero experto..."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("assistant", "{agent_scratchpad}")
    ])
    
    return create_openai_tools_agent(llm, tools, prompt=prompt)