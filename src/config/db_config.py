import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

def convert_url(original_url):
    parts = original_url.split("://")
    scheme = parts[0]
    rest = parts[1]

    userinfo, netloc_path = rest.split("@")
    username, password = userinfo.split(":")
    
    # Splitting netloc_path to extract host, port, and db
    if ":" in netloc_path:
        host_port, db = netloc_path.split("/")
        host, port = host_port.split(":")
    else:
        host = netloc_path
        port = "5432" 
        load_dotenv()

        env = os.getenv("ENV", "dev") 

        if env == "dev":
            db="book_db_fastapi"
        else:
            db="Fast-Api-Db"
        
    new_url = f"{scheme}+psycopg2://{username}:{password}@{host}:{port}/{db}"
    return new_url

class Settings(BaseSettings):
    def __init__(self):
        super().__init__()
        load_dotenv()
    
    @property
    def db_url(self):
        env = os.getenv("ENV", "prod")  # Default to 'prod' if ENV is not set
        
        if env == "dev":
            conn_url = os.getenv("LOCAL_DATABASE_URL")
        else:
            conn_url = os.getenv("PRODUCTION_URL")

        if conn_url:
            return convert_url(conn_url)
        else:
            raise ValueError("Database connection URL is not set in environment variables.")


loaded_config = Settings()
