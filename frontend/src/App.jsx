import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
  if (!message.trim()) return;

  const userMessage = message;

  // Show user's message immediately
  setMessages((prev) => [
    ...prev,
    {
      sender: "user",
      text: userMessage,
    },
  ]);

  setMessage("");

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/chat?message=${encodeURIComponent(userMessage)}`,
      {
        method: "POST",
      }
    );

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();

    // Show bot response
    setMessages((prev) => [
      ...prev,
      {
        sender: "bot",
        text: data.bot_response,
      },
    ]);
  } catch (error) {
    console.error("Chat error:", error);

    setMessages((prev) => [
      ...prev,
      {
        sender: "bot",
        text: "Sorry, I couldn't connect to the chatbot server.",
      },
    ]);
  }
};

  return (
    <div className="app">
      <div className="chat-container">

        <div className="chat-header">
          <h2>CodeNergy Assistant</h2>
          <span>Online</span>
        </div>

        <div className="chat-messages">

          {messages.length === 0 ? (
            <div className="welcome">
              <h3>👋 Hello!</h3>
              <p>How can I help you today?</p>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.sender}`}
              >
                {msg.text}
              </div>
            ))
          )}

        </div>

        <div className="chat-input">

          <input
            type="text"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />

          <button onClick={sendMessage}>
            Send
          </button>

        </div>

      </div>
    </div>
  );
}

export default App;