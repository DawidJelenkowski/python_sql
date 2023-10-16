from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr, SecretStr, ValidationError
from db import Database
from utils import get_password_hash, verify_password

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


@app.get("/register")
def register(email: str, password: SecretStr):
    try:
        user = User(email=email, password=password)
        hashed_password = get_password_hash(password.get_secret_value())

        # stored in the db

        return {"email": email, "password": hashed_password}
    except ValidationError:
        return {"error": "That does not look like a valid email"}
