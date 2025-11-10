import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse

load_dotenv()

def limpar_url_conexao(url_original):
    """Remove parâmetros problemáticos da URL de conexão"""
    try:
        # Parse a URL
        parsed = urlparse(url_original)
        
        # Reconstruir a URL sem query parameters
        url_limpa = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            '',  # remove params
            '',  # remove query
            ''   # remove fragment
        ))
        
        return url_limpa
        
    except Exception as e:
        print(f"❌ Erro ao limpar URL: {e}")
        return url_original

def criar_engine_supabase():
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        raise ValueError("❌ DATABASE_URL não encontrado no arquivo .env")
    
    # Limpar a URL
    DATABASE_URL_LIMPA = limpar_url_conexao(DATABASE_URL)
    
    # Criar engine com configurações otimizadas
    engine = create_engine(
        DATABASE_URL_LIMPA,
        connect_args={
            'connect_timeout': 10,
            'application_name': 'AnalisadorEleitoral'
        },
        pool_pre_ping=True,
        echo=False  # Desativa logs detalhados (mude para True para debug)
    )
    
    return engine

# Criar engine global
try:
    engine = criar_engine_supabase()
    print("✅ Engine do Supabase criado com sucesso")
except Exception as e:
    print(f"❌ Falha ao criar engine: {e}")
    engine = None

def testar_conexao():
    """Testa a conexão com o banco"""
    if not engine:
        print("❌ Engine não disponível")
        return False
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"✅ Conexão bem-sucedida! PostgreSQL: {version}")
            
            # Testar se podemos criar tabelas
            result = conn.execute(text("SELECT current_database();"))
            db_name = result.scalar()
            print(f"📊 Conectado ao banco: {db_name}")
            
            return True
    except Exception as e:
        print(f"❌ Erro na conexão com o banco: {e}")
        return False

if __name__ == "__main__":
    testar_conexao()