import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

key_value_url = "https://akv-reference.vault.azure.net/"
credential = DefaultAzureCredential()

client = SecretClient(vault_url=key_value_url, credential=credential)

# Get database url from azure key value
try:
    database_url = client.get_secret("database-url").value
    logging.info("Successfully retrieved the database URL from AKV")
except Exception as e:
    logging.error("Failed to retrieve database URL: {e}")
    raise

# sqlalchemy base class
Base = declarative_base()

# Create engine for migrations or operations
engine = create_engine(database_url, echo=True)

# Sessionmaker for interacting with database synchronously
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Dependency Injection for Database Session:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()