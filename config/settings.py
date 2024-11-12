from dotenv import load_dotenv
import os

load_dotenv()

# Azure OpenAI settings
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_VERSION = os.getenv("API_VERSION")
DEPLOYMENT_ID = os.getenv("DEPLOYMENT_ID")

# Elasticsearch settings
ES_ENDPOINT = "https://8470e7b75ed04b90bb68ae3c194a20ff.us-west2.gcp.elastic-cloud.com:443"
ES_API_KEY = os.getenv("ES_API_KEY")
ES_INDEX = "faqs"
BALANCES_INDEX = "balances"

# Asegurarse de que todas las variables requeridas estén presentes
required_vars = [
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
    "API_VERSION",
    "DEPLOYMENT_ID",
    "ES_API_KEY"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(
        f"Faltan las siguientes variables de entorno requeridas: {', '.join(missing_vars)}"
    )