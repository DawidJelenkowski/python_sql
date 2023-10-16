from psycopg2 import connect, sql
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

    def write(self, table: str, columns: list[str], data: list):
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id").format(
            sql.Identifier(table),
            sql.SQL(",").join(map(sql.Identifier, columns)),
            sql.SQL(",").join(map(sql.Literal, data)),
        )

        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchone().get('id')

    def get(self, table: str, columns: list[str], limit: int = None, where: dict = None):
        query = sql.SQL("SELECT {} FROM {}").format(
            sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.Identifier(table)
        )

        if where:
            query += sql.SQL(" WHERE {}").format(
                sql.SQL(" AND ").join(
                    map(
                        lambda x: sql.SQL("{} = {}").format(
                            sql.Identifier(x), sql.Literal(where.get(x))
                        ), where)
                )
            )

        if limit:
            query += sql.SQL(" LIMIT {}").format(sql.Literal(limit))

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_one(self, table: str, columns: list[str], where: dict = None):
        result = self.get(table, columns, 1, where)  # [{}]
        if len(result):
            return result[0]  # {}

    def update(self, table: str, columns: list[str], data: list, where: dict = None):
        where_clause = sql.SQL("")

        if where:
            where_clause = sql.SQL("WHERE {}").format(
                sql.SQL(" AND ").join(
                    sql.SQL("{} = {}").format(
                        sql.Identifier(k), sql.Literal(v)) for k, v in where.items()
                )
            )

        query = sql.SQL("UPDATE {} SET {} {}").format(
            sql.Identifier(table),
            sql.SQL(",").join(
                sql.SQL("{} = {}").format(
                    sql.Identifier(a), sql.Literal(b)) for a, b in zip(columns, data)
            ),
            where_clause
        )

        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.rowcount



