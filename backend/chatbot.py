from openai import OpenAI
from dotenv import load_dotenv
import os
from upstash_redis import Redis
import json

from backend.database import get_services, get_faqs, get_projects


# Load environment variables
load_dotenv()


redis_client = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)


# Connect to DeepSeek
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def get_response(message, session_id="user1"):

    # Create a Redis key for this conversation
    chat_key = f"chat:{session_id}"


    # Get previous messages from Redis
    previous_messages = redis_client.lrange(
        chat_key,
        0,
        -1
    )


    # Convert Redis JSON strings into Python dictionaries
    conversation_history = []

    for stored_message in previous_messages:
        conversation_history.append(
            json.loads(stored_message)
        )


    # Get CodeNergy information from MongoDB
    services = get_services()
    faqs = get_faqs()
    projects = get_projects()


    # Build services information
    services_info = "Services:\n"

    for service in services:
        services_info += f"""
- Title: {service.get("title", "")}
  Category: {service.get("category", "")}
  Subcategory: {service.get("subcategory", "")}
  Description: {service.get("description", "")}
"""


    # Build FAQ information
    faq_info = "Frequently Asked Questions:\n"

    for faq in faqs:
        faq_info += f"""
Q: {faq.get("question", "")}
A: {faq.get("answer", "")}
"""


    # Build projects information
    projects_info = "Projects:\n"

    for project in projects:
        projects_info += f"""
- Title: {project.get("title", "")}
  Description: {project.get("description", "")}
"""


    # Combine CodeNergy information
    knowledge = f"""
{services_info}

{faq_info}

{projects_info}
"""


    # Send previous conversation + new message to DeepSeek
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": f"""
You are the official CodeNergy website assistant.

Answer the user's questions using ONLY the CodeNergy information
provided below.

Do not invent company information, services, prices, contact details,
projects, or other facts that are not present in the provided information.

If the answer cannot be found in the provided information, politely
say that you don't have that information and suggest contacting
CodeNergy directly.

Keep responses helpful, natural, and concise.

CodeNergy information:
{knowledge}
"""
            },

            *conversation_history,

            {
                "role": "user",
                "content": message
            }
        ]
    )


    # Get DeepSeek response
    bot_response = response.choices[0].message.content


    # Save user message
    redis_client.rpush(
        chat_key,
        json.dumps({
            "role": "user",
            "content": message
        })
    )


    # Save bot response
    redis_client.rpush(
        chat_key,
        json.dumps({
            "role": "assistant",
            "content": bot_response
        })
    )


    return bot_response