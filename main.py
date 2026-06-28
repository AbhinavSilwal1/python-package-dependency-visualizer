import typer
from pathlib import Path


app = typer.Typer()


@app.command()
def hello():
    # Temporary test command to verify CLI works.
    print("Python Package Dependency Visualizer is running 🚀")


@app.command()
def version():
    # Show version of the tool.
    print("v0.1.0")


@app.command()
def scan(path: str = typer.Argument(".")):
    # Scan a project directory and list Python files
    project_path = Path(path)

    print(f"Scanning project: {project_path.resolve()}\n")

    if not project_path.exists():
        print("Path does not exist.")
        raise typer.Exit()

    python_files = []

    for file in project_path.rglob("*.py"):
        if ".venv" in file.parts or "__pycache__" in file.parts:
            continue

        python_files.append(file)

    print(f"Found {len(python_files)} Python files:\n")

    for file in python_files:
        print(f"- {file.relative_to(project_path)}")


if __name__ == "__main__":
    app()