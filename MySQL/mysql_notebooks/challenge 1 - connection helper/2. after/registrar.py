import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def add_student():
    console.print("Adding a new student...")


@app.command()
def add_course():
    console.print("Adding a new course...")


if __name__ == "__main__":
    app()
