import azure.functions as func
import logging
from sqlalchemy.orm import Session
from db.database import get_db
from utils import get_db_session, generate_response, parse_request_body
from schema.user_schema import UserLogin
from services.auth_service import login_user
from services.create_access_token import create_access_token

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="loginservice", methods=["POST"])
def loginservice(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Create DB Session
    db: Session = get_db_session(get_db)
    if not db:
        return generate_response(
            success=False,
            error="Database connection failed",
            message="Unable to connect to the database",
            status_code=500
        )
        
    # Parse and validate request body for JSON data
    user_input = parse_request_body(req=req, schema=UserLogin)
    if not user_input:
        return generate_response(
            success=False,
            error="Invalid input",
            message="Invalid email or password input",
            status_code=400
        )
        
    # extract email and password
    email = user_input.email
    password = user_input.password

    # Validate email and password if not null
    if not email or not password:
        return generate_response(
            success=False,
            error="Invalid input",
            message="Email and Password are required",
            status_code=400
        )
        
    # Authenticate and generate token
    try:
        # Authenticate
        user_info = login_user(db, email, password)
        if not user_info:
            return generate_response(
                success=False,
                error="User not found",
                message=f"Account {email} does not exist",
                status_code=404
            )
        
        # Generate token
        access_token = create_access_token(data={"sub": user_info["email"]})
        
        print(f"user_info: {user_info}")
        
        return generate_response(
            success=True,
            user=user_info,
            access_token=access_token,
            token_type="Bearer",
            message="Successfully logged in"
        )
    except ValueError as ve:
        logging.error(f"Authentication error: {ve}")
        return generate_response(
            success=False,
            error="Failed to login",
            message="Authentication failed",
            status_code=500
        )