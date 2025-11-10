# langchain_agent.py
import os
import pandas as pd
from sqlalchemy import text
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from connection import engine
from grok_connector import get_grok_connection

# Inicializa banco
def init_database():
    try:
        db = SQLDatabase(engine=engine, view_support=True, include_tables=["candidatos"])
        print("✅ Banco conectado com sucesso.")
        return db
    except Exception as e:
        print(f"❌ Erro ao conectar banco: {e}")
        return None

# Cria agente Grok + LangChain
def create_grok_agent(db):
    llm = get_grok_connection()

    context = """
    Você é um analista eleitoral brasileiro com acesso ao banco do TSE.    
    Ignore valores nulos e registros inválidos.
    Explique suas respostas em português natural.
    """

    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True,
        agent_type="openai-tools",
        prompt_prefix=context
    )
    return agent



# --- Consulta SQL simples ---
def run_predefined_query(question):
    """Executa SQL direto para perguntas simples."""
    q = question.lower()
    if "mulher" in q and "partido" in q:
        sql = text("""
            SELECT nm_partido, COUNT(*) AS total
            FROM public.candidatos
            WHERE ds_genero ILIKE '%FEM%'
            GROUP BY nm_partido
            ORDER BY total DESC
            LIMIT 10;
        """)
        title = "Mulheres candidatas por partido (PR, 2024)"
        return sql, title
    return None, None

# --- Executa SQL e retorna DataFrame ---
def execute_sql(sql):
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)