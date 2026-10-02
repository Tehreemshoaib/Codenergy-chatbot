from fastapi import FastAPI
from backend.chatbot import get_response

app = FastAPI()


@app.get("/")
def home():
    return {"message": "CodeNergy Chatbot Backend is running"}


@app.post("/chat")
def chat(message: str):
    response = get_response(message)

    return {
        "user_message": message,
        "bot_response": response
    }