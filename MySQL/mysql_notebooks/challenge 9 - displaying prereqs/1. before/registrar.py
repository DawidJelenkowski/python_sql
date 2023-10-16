import typer
from rich.console import Console
from database import reset, add_a_student, add_a_new_course, add_a_prerequisite, initialize_data

app = typer.Typer()
console = Console()


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
