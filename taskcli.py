import db
import table

from task import Task
from typer import Typer, Argument, Option
import typer

cliapp = Typer(
    name="taskcli",
    add_completion=False,
    options_metavar=False,
    help="taskcli is a cli tool to manage tasks with command line",
)

short_help = "Add a new Task"
help = "Add a new Task to your list with a title and description using the add command. Adding a description \
to task is optional but a title is compulsory."


@cliapp.command(
    name="add",
    help=help,
    short_help=short_help,
)
def addTask(
    title: str = Argument(help="New Task Title"),
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
help = "View all tasks completed or not in a tabular format. --first and --last flags \
can be used to retrieve first N tasks or last N tasks, by default shows all tasks. If number of first \
and last tasks together is greater than the total tasks present then shows entire task list."


@cliapp.command(
    name="view",
    help=help,
    short_help=short_help,
)
def view(
    first: int = Option(None, help="Shows first N tasks"),
    last: int = Option(None, help="Shows last N tasks"),
) -> None:
    if first and last:
        if first + last > db.getRowCount():
            table.composeTable(db.getTasks())
        else:
            table.composeTable(db.getTasks(-last))
            table.composeTable(db.getTasks(first))
    elif first:
        table.composeTable(db.getTasks(first))
    elif last:
        table.composeTable(db.getTasks(-last))
    else:
        table.composeTable(db.getTasks())
    table.renderTable()


if __name__ == "__main__":
    db.createTable()
    cliapp()
    db.conn.close()
