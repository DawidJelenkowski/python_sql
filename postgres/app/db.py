from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from os import environ as env

load_dotenv()

POSTGRES_HOST = 'postgres'
POSTGRES_PORT = 5432
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DATABASE = 'postgres'
#
POSTGRES_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}'


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None


    # OPEN CONNECTION TO THE DATABASE SPECIFIED IN "env.get()"
    def open(self, url=None):
        if not url:
            url = env.get("CONNECTION_URL")

        self.conn = connect(url)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)


    # CLOSE CONNECTION
    def close(self):
        self.cursor.close()
        self.conn.close()
        
    
    @staticmethod
    def _compose_kv_and(separator=" AND ", kv_pairs=None):
        return sql.SQL(separator).join(
            sql.SQL("{} = {}").format(
                sql.Identifier(k), sql.Literal(v)) for k, v in kv_pairs
        )
        
        
    # WRITE A DATA TO A TABLE
    def write(self, table: str, columns: list[str], data: list):
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id").format(
            sql.Identifier(table),
            sql.SQL(",").join(map(sql.Identifier, columns)),
            sql.SQL(",").join(map(sql.Literal, data))
        )

        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchone().get("id")
    
    
    # GETS A DATA FROM A TABLE
    def get(self, table: str, columns: list[str], limit: int = None, where: dict = None, or_where: dict = None):
        query = sql.SQL("SELECT {} FROM {}").format(
            sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.Identifier(table)
        )
        
        # if where is specified, it adds it to the query
        # anonymous function that maps keys and values
        # sql.Identifier takes column and sql.Literal takes value
        # it works similarly to update function
        if where:
            query += sql.SQL(" WHERE {}").format(
                self._compose_kv_and(kv_pairs=where.items())
            )
                                
                # sql.SQL(" AND ").join(
                #     map(
                #         lambda x: sql.SQL("{} = {}").format(
                #             sql.Identifier(x), sql.Literal(where.get(x))
                #         ), where)
                #     )
                # )

        
        # generator
        if where and or_where:
            query += sql.SQL(" OR ({})").format(
                self._compose_kv_and(kv_pairs=or_where.items())
            )
            #     sql.SQL(" AND ").join(
            #         sql.SQL("{} = {}").format(
            #             sql.Identifier(k),
            #             sql.Literal(v)
            #         ) for k, v in or_where.items()
            #     )
            # )                        
        # if limit is specified, it adds it to the query
        if limit:
            query += sql.SQL(" LIMIT {}").format(sql.Literal(limit))
        
        
       
        self.cursor.execute(query)
        return self.cursor.fetchall()


    # GET A RECORD FROM A TABLE
    def get_one(self, table: str, columns: list[str], where: dict = None):
        # the sole "self.get" with arguments would output: [{}] (dictionary in a list)
        result =  self.get(table, columns, 1, where)
        # by adding this, we get: {} (dictionary)
        if len(result):
            return result[0]


    # UPDATE DATA IN A TABLE
    def update(self, table: str, columns: list[str], data: list, where: dict = None):
        # if a user does not specify where it is going to be an empty query
        where_clause = sql.SQL("")
        
        # generator
        # it iterates through key(s) and value(s) where key is column and value is condition
        # It also allows to set multiple conditions, and it will be separated by " AND " automatically
        # it works similarly to the get function
        if where:
            where_clause = sql.SQL("WHERE {}").format(
                self._compose_kv_and(kv_pairs=where.items())
                )
                # sql.SQL(" AND ").join(
                #     sql.SQL("{} = {}").format(
                #         sql.Identifier(k), sql.Literal(v)) for k, v in where.items()
                #     )
                # )
        
        # the first argument takes table
        # the second takes column and value
        # iterate over first (a) and second (b) element of a tuple
        # the third argument takes where_clause only if specified
        # where a is a column and b is the value
        query = sql.SQL("UPDATE {} SET {} {}").format(
            sql.Identifier(table),
            self._compose_kv_and(separator=",", kv_pairs=zip(columns, data)),
            where_clause
        )
        #     sql.Identifier(table),
        #     sql.SQL(",").join(
        #         sql.SQL("{} = {}").format(
        #             sql.Identifier(a), sql.Literal(b)) for a, b in zip(columns, data)
        #     ), where_clause
        # )
        
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.rowcount
    

    def delete(self, table: str, where: dict = None):
        where_clause = sql.SQL("")

        if where:
            where_clause = sql.SQL("WHERE {}").format(
                self._compose_kv_and(kv_pairs=where.items())
            )
                # sql.SQL(" AND ").join(
                #     sql.SQL("{} = {}").format(
                #         sql.Identifier(k), sql.Literal(v)) for k, v in where.items()
                #     )
                # )
        
        query = sql.SQL("DELETE FROM {} {}").format(
            sql.Identifier(table),
            where_clause
        )
        
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.rowcount
# def test():
#     db = Database()

#     db.cursor

#     db.open()

#     return db.conn

# print(test())