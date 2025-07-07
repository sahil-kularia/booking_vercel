
# from fastapi import FastAPI
# from pydantic import BaseModel
# from conversation_utils import get_next_question

# app = FastAPI()

# class UserMessage(BaseModel):
#     user_id: str
#     message: str

# @app.post("/chat")
# async def chat_endpoint(user_msg: UserMessage):
#     """
#     Chat API to handle conversation.
#     """
#     response = get_next_question(user_msg.user_id, user_msg.message)
#     return {"response": response}

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from conversation_utils import get_next_question

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (important for frontend-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class UserMessage(BaseModel):
    user_id: str
    message: str

# API route to handle chat
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

# Health check route
@app.get("/")
async def root():
    """
    Root endpoint for health checks.
    """
    return {"status": "Backend is running 🚀"}
