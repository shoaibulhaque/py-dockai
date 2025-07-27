from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from langgraph.checkpoint.memory import MemoryCheckpointSaver
from api.db import get_session
from api.ai.agents import get_supervisor
from api.ai.schemas import SupervisorMessageSchema
from .models import ChatMessagePayLoad, ChatMessage, ChatMessageListItem

router = APIRouter()
checkpointer = MemoryCheckpointSaver()


# /api/chat/
@router.get("/")
def chat_health():
    return {"status": "ok"}


# /api/chats/recent/
# curl http://localhost:8080/api/chats/recent
@router.get("/recent/", response_model=List[ChatMessageListItem])
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)  # sql --> query
    results = session.exec(query).fetchall()[:10]

    return results


# HTTP POST ==> {"message": "Hello, World!"} ==> {"message": "Hello World", "id": 1}
# curl -X POST -d '{"message": "Hello, world"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
@router.post("/", response_model=SupervisorMessageSchema)
def chat_create_message(
    payload: ChatMessagePayLoad, session: Session = Depends(get_session)
):
    data = payload.model_dump()  # pydantic -> dict
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    thread_id = uuid.uuid4()
    supe = get_supervisor(checkpointer=checkpointer)
    msg_data = {
        "messages": [
            {"role": "user", "content": f"{payload.message}"},
        ]
    }
    result = supe.invoke(msg_data, {"configurable": {"thread_id": thread_id}})
    if not result:
        raise HTTPException(status_code=400, detail="Error with supervisor")
    messages = result.get("messages")
    if not messages:
        raise HTTPException(status_code=400, detail="Error with supervisor")
    return messages[-1]
