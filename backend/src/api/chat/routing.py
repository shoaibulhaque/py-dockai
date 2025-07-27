from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from api.db import get_session
from .models import ChatMessagePayLoad, ChatMessage, ChatMessageListItem

router = APIRouter()


# /api/chat/
@router.get("/")
def chat_health():
    return {"status": "ok"}


# /api/chats/recent/
# curl http://localhost:8080/api/chats/recent
@router.get("/recent/", response_model=List(ChatMessageListItem))
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)  # sql --> query
    results = session.exec(query).fetchall()[:10]

    return results


# HTTP POST ==> {"message": "Hello, World!"} ==> {"message": "Hello World", "id": 1}
# curl -X POST -d '{"message": "Hello, world"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
@router.post("/", response_model=ChatMessageListItem)
def chat_create_message(
    payload: ChatMessagePayLoad, session: Session = Depends(get_session)
):

    data = payload.model_dump()  # pydantic --> dict
    print(data)
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)  # ensure id/primary key added to the object instance
    # ready to store in the db

    return obj
