from fastapi import FastAPI, Depends
from db import Database

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
