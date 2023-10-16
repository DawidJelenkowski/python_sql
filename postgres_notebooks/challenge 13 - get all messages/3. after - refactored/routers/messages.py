from fastapi import APIRouter, Form, Depends, HTTPException, status
from dependencies import get_db, validate_user
from db import Database

router = APIRouter(tags=["messages"])


@router.post("/messages")
def write_a_message_on_the_guestbook(message: str = Form(...), private: bool = Form(False),
                                     db: Database = Depends(get_db),
                                     user_id: int = Depends(validate_user)):
    message_id = db.write("guestbook", ["user_id", "message", "private"], [user_id, message, private])

    return {
        "message_id": message_id
    }


# POST  -> create a new resource
# PUT   -> update an existing resource (full replace)
# PATCH -> update an existing resource (partially)

@router.patch("/messages/{message_id}")
def update_a_specific_message(message_id: int, message: str = Form(...), private: bool = Form(False),
                              db: Database = Depends(get_db),
                              user_id: str = Depends(validate_user)):
    message_db = db.get_one("guestbook", ["id", "user_id"], where={"id": message_id})

    if not message_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message was not found")

    if message_db.get("user_id") == user_id:
        db.update("guestbook", ["message", "private"], [message, private], where={"id": message_id})
        return {"status": "Message updated"}

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this message")


@router.get("/messages/{message_id}")
def get_a_specific_message(message_id: int, db: Database = Depends(get_db),
                           user_id: int = Depends(validate_user)):
    message = db.get_one(
        table="guestbook",
        columns=["id", "user_id", "message", "private", "created_at"],
        where={"id": message_id}
    )

    if (not message) or (message['private'] and message['user_id'] != user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="A public message by that id could not be found")

    # do not return user_id and private
    exclude = ["user_id", "private"]

    return {k: v for k, v in message.items() if k not in exclude}


@router.get("/messages")
def get_all_messages(num: int = 10, db: Database = Depends(get_db), user_id: str = Depends(validate_user)):
    messages = db.get(table="guestbook",
                      columns=["id", "message", "created_at"],
                      where={"private": False},
                      or_where={"private": True, "user_id": user_id},
                      limit=num)

    return messages
