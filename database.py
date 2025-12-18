
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import streamlit as st


def get_engine(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME) -> Engine:
    """
    Create a SQLAlchemy engine with SSL enabled (required for TiDB Cloud)
    """
    connection_url = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(
        connection_url,
        connect_args={
            "ssl": {
                "ssl_mode": "REQUIRED"
            }
        },
        pool_pre_ping=True
    )

    return engine


def insert_artifact_data(engine, st):
    """
    Dummy insert function (safe placeholder).
    Modify this only if you really want to insert data.
    """
    try:
        with engine.begin() as conn:
            # Example test query (safe)
            conn.execute(text("SELECT 1"))

        st.success("✅ Database connection successful (SSL enabled)")
        return True

    except Exception as e:
        st.error(f"❌ Insert/Connection failed: {e}")
        return False


def create_database_if_missing(*args, **kwargs):
    """
    TiDB Cloud does NOT allow creating databases from clients.
    This function is intentionally disabled.
    """
    return


def run_schema(engine):
    """
    Do nothing.
    You already have tables in TiDB.
    """
    return
