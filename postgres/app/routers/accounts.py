from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Query, Depends
from pydantic import BaseModel, EmailStr, SecretStr, ValidationError
from psycopg2.errors import UniqueViolation
from app.db import Database
from app.dependencies import get_db
from app.utils import get_password_hash


router = APIRouter(tags=['accounts'])
# ADDS FUNCTIONALITY
# EmailStr checks if the provided value is in an email form ex: some@gmail.com
# SecretStr hides values while providing ********* instead of "somepassword"
class User(BaseModel):
    email: EmailStr
    password: SecretStr

# ACTIVATE USER ACCOUNT
@router.post('/activate')
def activate(token: str, db: Database = Depends(get_db)):
    # look for the token in the db
    # does the token belong to the user?
    # if yes, and account is inactive, then actiave it
    token = db.get_one('tokens', ['user_id'], where={'token': token})
    
    # CHECK IF AN ACCOUNT HAS BEEN ALREADY ACTIVATED
    if token:
        is_account_active = db.get_one('users', ['active'], where={'id': token.get('user_id')})
        
        # the bool("string") gives True, so if variable "is_account_active" contains string
        # it will not activate the account once again and will rise an error
        if is_account_active.get('active'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account already activated"
            )
        
        db.update('users', ['active', 'activated_at'], ['true', 'now()'], where={'id': token.get('user_id')})
        return {'status': "Your account has been activated!"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")


# REGISTER USER IN A DATABASE
# db is an inherited function from the class Database from db.py
# the Query(default=None) makes the password required
# hashes the provided password
# writes the data to the "users" and "tokens" table
@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(email: str, password: SecretStr = Query(default=None, min_length=8), db: Database = Depends(get_db)):
    try:
        user = User(email=email, password=password)
        hashed_password = get_password_hash(password.get_secret_value())
        token = str(uuid4())
        user_id = db.write('users', ['email', 'password'], [email, hashed_password])

        db.write('tokens', ['token', 'user_id'], [token, user_id])
        return {"message": "User created", "user_id": user_id}
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="That does not look like a valid email")
    except UniqueViolation:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="A user by that email id is already registered")