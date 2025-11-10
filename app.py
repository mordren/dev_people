# app.py
import streamlit as st
import pandas as pd
from langchain_agent import init_database, create_grok_agent, run_predefined_query, execute_sql

# --- Configuração inicial ---
st.set_page_config(page_title="Analisador Eleitoral", page_icon="🤖", layout="wide")
st.title("🤖 Analisador Eleitoral com Grok + LangChain")

# --- Inicialização do banco e agente ---
db = init_database()
if not db:
    st.error("❌ Erro ao conectar ao banco de dados.")
    st.stop()

agent = create_grok_agent(db)
st.sidebar.success("✅ Banco e agente inicializados com sucesso")

# --- Entrada de pergunta ---
question = st.text_area("Digite sua pergunta:", height=100)

# --- Botão principal ---
if st.button("🚀 Analisar"):
    with st.spinner("Consultando e analisando..."):
        try:
            # 1️⃣ Executar query direta (pré-definida)
            sql, title = run_predefined_query(question)
            if sql:
                df = execute_sql(sql)
                st.success("✅ Consulta direta executada com sucesso!")
                st.dataframe(df)
                st.bar_chart(df.set_index(df.columns[0]))
            
            else:
                # 2️⃣ Se não for pré-definida, usar Grok + LangChain
                response = agent.invoke({"input": question})
                st.markdown(f"### 🧠 Resposta:")
                st.write(response["output"] if isinstance(response, dict) else response)

        except Exception as e:
            st.error(f"❌ Erro na análise: {e}")

# --- Rodapé ---
st.markdown("---")
st.caption("Desenvolvido com ❤️ usando LangChain + Streamlit + Supabase")