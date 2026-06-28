import typer


app = typer.Typer()


@app.command()
def hello():
    # Temporary test command to verify CLI works.
    print("Python Package Dependency Visualizer is running 🚀")


@app.command()
def version():
    # Show version of the tool.
    print("v0.1.0")


if __name__ == "__main__":
    app()