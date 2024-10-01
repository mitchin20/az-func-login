import json
import logging
import azure.functions as func
from sqlalchemy.orm import Session

# Parse and validate request body
def parse_request_body(req: func.HttpRequest, schema):
    try:
        req_body = req.get_json()
        return schema(**req_body)
    except ValueError as ve:
        logging.error(f"Unable to parse request: {ve}")
        return None
        

# Helper function to create and yield database session
def get_db_session(get_db_func):
    try:
        db: Session = next(get_db_func())
        return db
    except Exception as e:
        logging.error(f"Failed to create DB session: {e}")
        return None
    
# Generate consistent HTTP response 
def generate_response(success: bool, user=None, access_token=None, token_type=None, error=None, message=None, status_code=200):
    response = {
        "success": success,
        "user": user,
        "access_token": access_token,
        "token_type": token_type,
        "error": error,
        "message": message
    }
    
    return func.HttpResponse(
        json.dumps(response),
        status_code=status_code,
        mimetype="application/json"
    )