import typer
from datetime import datetime
from os import environ as env
from rich.console import Console
from rich.table import Table
from database import reset, add_a_student, add_a_new_course, add_a_prerequisite, initialize_data, \
    show_prerequisites_for, show_students_by, show_courses_by, enroll_student, set_grade, unenroll_student, \
    show_courses_a_student_is_currently_taking, get_transcript_for

app = typer.Typer()
console = Console()


def pretty_table(with_headers, data, in_color):
    table = Table(*with_headers, show_header=True, header_style=f"bold {in_color}")

    for row in data:
        table.add_row(*map(str, row))

    console.print(table)


@app.command()
def transcript(student: str):
    data = get_transcript_for(student)
    pretty_table(["Course", "Year", "Grade", "Letter Grade"], data=data, in_color="magenta")
    console.print(f"Average GPA: {sum([row[2] for row in data]) / len(data):.2f}", style="bold")


@app.command()
def enroll(student: str, course: str, year: int = datetime.now().year):
    enroll_student(student, course, year)


@app.command()
def add_student(first_name: str, last_name: str, unix_id: str):
    add_a_student(first_name, last_name, unix_id)


@app.command()
def add_course(moniker: str, name: str, department: str):
    add_a_new_course(moniker, name, department)


@app.command()
def add_prereq(course: str, prereq: str, min_grade: int = 50):
    add_a_prerequisite(course, prereq, min_grade)


@app.command()
def unenroll(student: str, course: str, year: int = datetime.now().year):
    unenroll_student(student, course, year)


@app.command()
def current_courses(student: str):
    data = show_courses_a_student_is_currently_taking(student)
    pretty_table(["Course", "Year"], data=data, in_color="green")


@app.command()
def grade(student: str, course: str, grade: int, year: int = datetime.now().year):
    set_grade(student, course, grade, year)


@app.command()
def show_prereqs(course: str):
    pretty_table(["Prerequisites", "Minimum Grade"], data=show_prerequisites_for(course), in_color="yellow")


@app.command()
def show_students(last_name: str):
    data = show_students_by(last_name)

    pretty_table(["First Name", "Last Name", "UnixID"], data=data, in_color="blue")


@app.command()
def show_courses(department: str):
    data = show_courses_by(department)

    pretty_table(["Moniker", "Name", "Department"], data=data, in_color="green")


@app.command()
def reset_database(verbose: bool = False, with_data: bool = True):
    # --with-data
    # --no-with-data

    # --verbose

    answer = input("This will delete all the data. Are you sure? (y/n): ")

    if verbose:
        env["MYSQL_VERBOSE"] = "YES"

    if answer.strip().lower() == "y":
        reset()
        typer.echo("Database reset successfully.")

        if with_data:
            initialize_data()
            typer.echo("Data initialized successfully.")
    else:
        typer.echo("Database reset aborted.")


if __name__ == "__main__":
    app()
