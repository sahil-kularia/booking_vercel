from fastapi import FastAPI
from pydantic import BaseModel
from conversation_utils import get_next_question

app = FastAPI()

class UserMessage(BaseModel):
    user_id: str
    message: str

@app.get("/")
async def root():
    return {"message": "🎉 Backend API is running! Visit /chat to POST messages."}

@app.post("/chat")
async def chat_endpoint(user_msg: UserMessage):
    """
    Chat API to handle conversation.
    """
    response = get_next_question(user_msg.user_id, user_msg.message)
    return {"response": response}
