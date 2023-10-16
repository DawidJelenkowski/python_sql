from fastapi import APIRouter, Form, Depends
from dependencies import get_db
from db import Database

router = APIRouter(tags=["messages"])


@router.post("/messages")
def write_a_message_on_the_guestbook(message: str = Form(...), private: bool = Form(False),
                                     db: Database = Depends(get_db)):
    message_id = db.write("guestbook", ["user_id", "message", "private"], [16, message, private])

    return {
        "message_id": message_id
    }
