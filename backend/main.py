
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from conversation_utils import get_next_question


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserMessage(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(user_msg: UserMessage):
    """
    Handles user input and returns the next chatbot response.
    """
    try:
        response = get_next_question(user_msg.user_id, user_msg.message)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}


@app.get("/")
async def root():
    """
    Root endpoint for health checks.
    """
    return {"status": "Backend is running 🚀"}
