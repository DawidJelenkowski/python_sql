from dotenv import load_dotenv
from os import environ as env
from mysql.connector import connect, Error
import data

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


def query(connection, q, data=None, many=False, fetch=None):
    cursor = connection.cursor()

    if many:
        cursor.executemany(q, data)
    else:
        cursor.execute(q, data)

    if fetch:
        return cursor.fetchall()
    else:
        connection.commit()

    cursor.close()


def enroll_student(student, course, year):
    with get_connection() as conn:
        q = "INSERT INTO student_course (student, course, year) VALUES (%s, %s, %s);"
        data = (student, course, year)

        query(conn, q, data=data)


def show_prerequisites_for(course):
    with get_connection() as conn:
        q = "SELECT prereq, min_grade FROM prerequisites WHERE course = %s"
        data = (course,)

        return query(conn, q, data=data, fetch=True)


def initialize_data():
    with get_connection() as conn:
        query(conn, "INSERT INTO students (first_name, last_name, unix_id) VALUES (%s, %s, %s);", data.students,
              many=True)
        query(conn, "INSERT INTO courses (moniker, name, department) VALUES (%s, %s, %s);", data.courses,
              many=True)
        query(conn, "INSERT INTO prerequisites (course, prereq, min_grade) VALUES (%s, %s, %s);", data.prerequisites,
              many=True)


def add_a_student(first_name, last_name, unix_id):
    with get_connection() as conn:
        q = "INSERT INTO students (first_name, last_name, unix_id) VALUES (%s, %s, %s);"
        data = (first_name, last_name, unix_id)

        query(conn, q, data)


def add_a_new_course(moniker, name, department):
    with get_connection() as conn:
        q = "INSERT INTO courses (moniker, name, department) VALUES (%s, %s, %s);"
        data = (moniker, name, department)

        query(conn, q, data)


def add_a_prerequisite(course, prereq, min_grade):
    with get_connection() as conn:
        q = "INSERT INTO prerequisites (course, prereq, min_grade) VALUES (%s, %s, %s);"
        data = (course, prereq, min_grade)

        query(conn, q, data)


def show_students_by(last_name):
    with get_connection() as conn:
        q = "SELECT first_name, last_name, unix_id FROM students WHERE last_name like %s;"
        data = ('%' + last_name + '%',)

        return query(conn, q, data=data, fetch=True)


def show_courses_by(department):
    with get_connection() as conn:
        q = "SELECT moniker, name, department FROM courses WHERE department = %s;"
        data = (department,)

        return query(conn, q, data=data, fetch=True)
