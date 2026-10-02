from backend.database import get_company, get_services, get_faqs


def get_response(message):
    message = message.lower()

    # Get company information
    company = get_company()

    # If user asks about the company
    if "company" in message or "codenenergy" in message:
        return company[2]

    # If user asks about services
    if "service" in message or "services" in message:
        services = get_services()

        response = "CodeNergy provides the following services:\n\n"

        for service in services:
            response += f"- {service[2]}\n"

        return response

    # If user asks an FAQ
    faqs = get_faqs()

    for faq in faqs:
        question = faq[2].lower()

        if any(word in question for word in message.split()):
            return faq[3]

    return "Sorry, I don't have information about that yet."

if __name__ == "__main__":
    print(get_response("What services do you provide?"))
