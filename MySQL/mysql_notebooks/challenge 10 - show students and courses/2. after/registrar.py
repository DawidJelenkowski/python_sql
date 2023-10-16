import typer
from rich.console import Console
from rich.table import Table
from database import reset, add_a_student, add_a_new_course, add_a_prerequisite, initialize_data, \
    show_prerequisites_for, show_students_by, show_courses_by

app = typer.Typer()
console = Console()


def pretty_table(with_headers, data, in_color):
    table = Table(*with_headers, show_header=True, header_style=f"bold {in_color}")

    for row in data:
        table.add_row(*map(str, row))

    console.print(table)


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
def reset_database(with_data: bool = True):
    # --with-data
    # --no-with-data

    answer = input("This will delete all the data. Are you sure? (y/n): ")

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
