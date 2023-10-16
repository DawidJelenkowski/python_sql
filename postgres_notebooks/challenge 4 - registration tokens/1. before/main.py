from fastapi import FastAPI, Depends, Query, HTTPException, status
from pydantic import BaseModel, EmailStr, SecretStr, ValidationError
from db import Database
from utils import get_password_hash, verify_password
from psycopg2.errors import UniqueViolation

app = FastAPI()


def get_db():
    db = Database()

    try:
        db.open()
        yield db
    finally:
        db.close()


@app.get('/')
def root():
    return {"message": "nothing here, try /hello"}


@app.get('/hello')
def hello(db: Database = Depends(get_db)):
    # db...
    db.cursor.execute("SELECT 9 as magic_number;")
    data = db.cursor.fetchone()
    return {"message": "greetings!", "data": data}


class User(BaseModel):
    email: EmailStr
    password: SecretStr


# > facilitate syntax like:
# user_id = db.write('users', ['email', 'password'], [email, hashed_password])

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(email: str, password: SecretStr = Query(default=None, min_length=8), db: Database = Depends(get_db)):
    try:
        user = User(email=email, password=password)
        hashed_password = get_password_hash(password.get_secret_value())

        user_id = db.write('users', ['email', 'password'], [email, hashed_password])

        return {"message": "User created", "user_id": user_id}
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="That does not look like a valid email")
    except UniqueViolation:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="A user by that email id is already registered")
