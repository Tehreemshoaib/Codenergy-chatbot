from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.chatbot import get_response

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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