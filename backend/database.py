import psycopg2


def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="Codenergy chatbot",
        user="postgres",
        password="1234",
        port="5432"
    )

    return connection


def get_company():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM companies WHERE id = 1;")

    company = cursor.fetchone()

    cursor.close()
    connection.close()

    return company


def get_services():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM services WHERE company_id = 1;")

    services = cursor.fetchall()

    cursor.close()
    connection.close()

    return services


def get_faqs():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM faqs WHERE company_id = 1;")

    faqs = cursor.fetchall()

    cursor.close()
    connection.close()

    return faqs

if __name__ == "__main__":
    faqs = get_faqs()

    for faq in faqs:
        print(faq)