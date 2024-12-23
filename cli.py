import json
import os
import typer

app = typer.Typer()
tasks_file = "tasks.json"


def load_task_list():
    # Load task list from a JSON file
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as f:
            return json.load(f)
    return []


def save_task_list(task_list):
    # Save task list to a JSON file
    with open(tasks_file, "w") as f:
        json.dump(task_list, f)


@app.command()
def add(task: str):
    """Add a new task"""
    tasks = load_task_list()
    tasks.append(task)
    save_task_list(tasks)
    typer.echo(f"Added task: {tasks}")


@app.command()
def complete(removed_task: str):
    """Remove a task"""
    tasks = load_task_list()
    if removed_task in tasks:
        tasks.remove(removed_task)
        save_task_list(tasks)
        typer.echo(f"Remove task '{removed_task}' completed")
    else:
        typer.echo(f"Task '{removed_task}' not found")


@app.command()
def read(arg: str):
    """Show all tasks"""
    typer.echo(f"arg: '{arg}'")
    tasks = load_task_list()
    if tasks:
        typer.echo("Task list:")
        for idx, task in enumerate(tasks):
            typer.echo(f"{idx + 1}. {task}")
    else:
        typer.echo("No tasks found.")


if __name__ == "__main__":
    app()
