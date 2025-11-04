"""
Database utilities and connection management
"""
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config import DATABASE_URL
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseManager:
    """Database connection and query manager"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or DATABASE_URL
        self.engine = None
        self.Session = None
        
    def connect(self):
        """Create database connection"""
        try:
            self.engine = create_engine(self.database_url, pool_pre_ping=True)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("Database connection established")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    @contextmanager
    def get_session(self):
        """Get database session context manager"""
        if not self.Session:
            self.connect()
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: dict = None):
        """Execute a SQL query and return results"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def load_dataframe(self, query: str, params: dict = None) -> pd.DataFrame:
        """Execute query and return as DataFrame"""
        try:
            return pd.read_sql_query(query, self.engine, params=params)
        except Exception as e:
            logger.error(f"DataFrame loading failed: {e}")
            raise
    
    def insert_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = "append"):
        """Insert DataFrame into database table"""
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            logger.info(f"Inserted {len(df)} rows into {table_name}")
        except Exception as e:
            logger.error(f"DataFrame insertion failed: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")

def init_db():
    """Initialize database schema"""
    db = DatabaseManager()
    db.connect()
    
    # Read and execute SQL setup script
    from config import SQL_DIR
    setup_script = SQL_DIR / "database_setup.sql"
    
    if setup_script.exists():
        with open(setup_script, 'r') as f:
            sql_script = f.read()
        
        with db.engine.connect() as conn:
            conn.execute(text(sql_script))
            conn.commit()
        
        logger.info("Database schema initialized")
    else:
        logger.warning("Database setup script not found")

