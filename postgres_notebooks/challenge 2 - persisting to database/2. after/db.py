from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from os import environ as env

load_dotenv()


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self, url=None):
        if not url:
            url = env.get("CONNECTION_URL")

        self.conn = connect(url)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def close(self):
        self.cursor.close()
        self.conn.close()
