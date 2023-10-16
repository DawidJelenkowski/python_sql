from fastapi import FastAPI, Depends, Query, HTTPException, status
from pydantic import BaseModel, EmailStr, SecretStr, ValidationError
from db import Database
from utils import get_password_hash, verify_password
from psycopg2.errors import UniqueViolation
from uuid import uuid4

app = FastAPI(
    title="Guestbook API",
    version="0.1.0",
    description="A place to leave your suggestions..."
)


def get_db():
    db = Database()

    try:
        db.open()
        yield db
    finally:
        db.close()


class User(BaseModel):
    email: EmailStr
    password: SecretStr


@app.post("/activate", tags=["accounts"])
def activate(token: str, db: Database = Depends(get_db)):
    # > look for the token in the db
    # does the token belong to the user?
    # if yes, and account is inactive, then activate it

    # enable syntax like this:
    token = db.get_one("tokens", ["token", "user_id"], where={"token": token})

    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    else:
        return {"result": token.get("token"), "user_id": token.get("user_id")}

    # pass


@app.post("/register", status_code=status.HTTP_201_CREATED, tags=["accounts"])
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
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="A user by that email id is already registered")
