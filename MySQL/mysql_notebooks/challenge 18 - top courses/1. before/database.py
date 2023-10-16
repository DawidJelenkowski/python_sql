import mysql.connector
import typer
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

        if env.get('MYSQL_VERBOSE') == "YES":
            print("Connected to MySQL successfully")
    except Error as e:
        print(f"Error '{e}' occurred while attempting to connect to the database")

    return connection


def reset():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open('ddl.sql', 'r') as f:
                for result in cursor.execute(f.read(), multi=True):
                    if env.get('MYSQL_VERBOSE') == "YES":
                        print("Executed: ", result.statement)


def query(connection, q, data=None, many=False, fetch=None):
    cursor = connection.cursor()

    try:
        if many:
            cursor.executemany(q, data)
        else:
            cursor.execute(q, data)

        if fetch:
            return cursor.fetchall()
        else:
            connection.commit()

        if env.get("MYSQL_VERBOSE") == "YES":
            print("Executed successfully: ", q)

        typer.echo(typer.style("Successful", bg=typer.colors.GREEN, fg=typer.colors.BLACK))
    except (mysql.connector.IntegrityError, mysql.connector.DatabaseError) as e:
        typer.echo(f"Statement execution failed: {typer.style(e, bg=typer.colors.RED, fg=typer.colors.BLACK)}")
    finally:
        cursor.close()


def show_courses_a_student_is_currently_taking(student):
    with get_connection() as conn:
        q = "SELECT course, year FROM student_course WHERE student = %s AND grade IS NULL;"
        data = (student,)

        return query(conn, q, data=data, fetch=True)


def unenroll_student(student, course, year):
    with get_connection() as conn:
        q = "DELETE FROM student_course WHERE student = %s AND course = %s AND year = %s;"
        data = (student, course, year)

        query(conn, q, data)


def set_grade(student, course, grade, year):
    with get_connection() as conn:
        q = "UPDATE student_course SET grade = %s WHERE student = %s AND course = %s AND year = %s;"
        data = (grade, student, course, year)

        query(conn, q, data=data)


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


def get_transcript_for(student):
    with get_connection() as conn:
        q = """
            SELECT course, year, grade, (select letter
                from letter_grade as lg
                where lg.grade <= sc.grade
                order by lg.grade desc limit 1
            ) as letter FROM student_course as sc WHERE student = %s AND grade IS NOT NULL ORDER BY year;        
        """
        data = (student,)

        return query(conn, q, data=data, fetch=True)
