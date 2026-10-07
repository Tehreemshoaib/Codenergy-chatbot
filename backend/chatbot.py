from openai import OpenAI
from dotenv import load_dotenv
import os

from backend.database import get_services, get_faqs, get_projects


# Load environment variables
load_dotenv()


# Connect to DeepSeek
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def get_response(message):

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


    # Send message to DeepSeek
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
            {
                "role": "user",
                "content": message
            }
        ]
    )


    # Get DeepSeek response
    bot_response = response.choices[0].message.content


    return bot_response
