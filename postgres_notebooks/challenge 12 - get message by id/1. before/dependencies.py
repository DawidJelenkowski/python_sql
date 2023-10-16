from db import Database


def get_db():
    db = Database()

    try:
        db.open()
        yield db
    finally:
        db.close()
