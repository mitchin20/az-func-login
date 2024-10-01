import os
import json
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from jose import jwt
from datetime import datetime, timedelta, timezone

# Check if KEY_VAULT_URL is already set to detect if the environment is production
if not os.environ.get("KEY_VAULT_URL"):
    # Load local.settings.json only if KEY_VAULT_URL is not set
    try:
        with open('local.settings.json') as f:
            settings = json.load(f)
            for key, value in settings.get("Values", {}).items():
                os.environ[key] = value
        print("Loaded settings from local.settings.json.")
    except FileNotFoundError:
        print("local.settings.json not found. Ensure it exists for local development.")
    except json.JSONDecodeError:
        print("Failed to decode local.settings.json. Check if the JSON structure is correct.")
else:
    print("Running in production mode. Skipping local.settings.json loading.")

key_vault_url = os.environ.get("KEY_VAULT_URL")
credential = DefaultAzureCredential()

client = SecretClient(vault_url=key_vault_url, credential=credential)

try:
    jwt_secret = client.get_secret("jwt-secret").value
    agl = "HS256"
    access_token_expire_minutes = 30
    logging.info("Successfully retrieved jwt secret")
except Exception as e:
    logging.error(f"Failed to retrieve JWT secret: {e}")
    raise

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=agl)

    return encoded_jwt