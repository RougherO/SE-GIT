import db
import table

from task import Task
from typer import Typer, Argument, Option

cliapp = Typer(
    add_completion=False,
    options_metavar=False,
)

short_help = "Add a new Task"
help = "Add a new Task to your list with a title and description using the add command."


@cliapp.command(
    name="add",
    help=help,
    short_help=short_help,
)
def addTask(
    title: str,
    description: str = Argument(None, help="New Task Description"),
) -> None:
    db.insertTask(Task(title, description))


short_help = "Remove an already present Task"
help = "Remove a Task from your list with the task-ID using remove command. \
If no argument is provided then removes the last added task"


@cliapp.command(
    name="remove",
    help=help,
    short_help=short_help,
)
def removeTask(
    id: int = Argument(None, help="Task ID"),
) -> None:
    db.deleteTask(id)


short_help = "Update a present Task"
help = "Update a Task -- change title or description -- from your list with the task-ID using update command."


@cliapp.command(
    name="update",
    help=help,
    short_help=short_help,
)
def updateTask(
    id: int = Argument(help="Task ID"),
    title: str = Option(None, help="Provide new title of the task"),
    description: str = Option(None, help="Provide new description of the task"),
) -> None:
    db.updateTask(id, title, description)


short_help = "View all tasks"
help = "View all tasks completed or not in a tabular format"


@cliapp.command(
    name="view",
    help=help,
    short_help=short_help,
)
def view() -> None:
    table.renderTable(db.getTasks())


if __name__ == "__main__":
    db.createTable()
    cliapp()
    db.conn.close()
