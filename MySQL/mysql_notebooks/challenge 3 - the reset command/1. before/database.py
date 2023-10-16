from dotenv import load_dotenv
from os import environ as env
from mysql.connector import connect, Error

load_dotenv()


def get_connection():
    connection = None

    try:
        connection = connect(
            user=env.get("MYSQL_USER"),
            password=env.get("MYSQL_PASSWORD"),
            host=env.get("MYSQL_HOST"),
            port=env.get("MYSQL_PORT"),
            database=env.get("MYSQL_DATABASE"),
        )
    except Error as e:
        print(f"Error '{e}' occurred while attempting to connect to the database")

    return connection


def reset():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open('ddl.sql', 'r') as f:
                for result in cursor.execute(f.read(), multi=True):
                    pass
