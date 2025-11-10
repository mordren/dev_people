# grok_connector.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def _get_gemini_llm():
    """Retorna uma instância configurada do Gemini Flash (via API compatível com OpenAI)."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("❌ Variável de ambiente GEMINI_API_KEY não encontrada.")

    llm = ChatOpenAI(
        api_key=GEMINI_API_KEY,
        # Endpoint compatível com OpenAI da Gemini
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        # ajuste o nome se o modelo for diferente
        model="gemini-2.5-flash",
        temperature=0.2,
        max_tokens=2000,
    )
    return llm

# Mantém o mesmo nome usado no resto do código
def get_grok_connection():
    return _get_gemini_llm()

# Se em algum lugar você tiver get_grok_model(), também cobre:
def get_grok_model():
    return _get_gemini_llm()
