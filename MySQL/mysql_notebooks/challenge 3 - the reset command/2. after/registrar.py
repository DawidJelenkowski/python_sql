import typer
from rich.console import Console
from database import reset

app = typer.Typer()
console = Console()


@app.command()
def add_student():
    console.print("Adding a new student...")


@app.command()
def add_course():
    console.print("Adding a new course...")


@app.command()
def reset_database():
    answer = input("This will delete all the data. Are you sure? (y/n): ")

    if answer.strip().lower() == "y":
        reset()
        typer.echo("Database reset successfully.")
    else:
        typer.echo("Database reset aborted.")


if __name__ == "__main__":
    app()
