import db
import table

from task import Task
from typer import Typer, Argument, Option

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
    title: str = Argument(
        help="New Task Title",
        show_default=False,
    ),
    description: str = Argument(
        None,
        help="New Task Description",
        show_default=False,
    ),
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
    id: int = Argument(
        None,
        help="Task ID",
        show_default=False,
    ),
    complete: bool = Option(
        None,
        help="Removes all completed tasks. Pass --no-complete to remove all pending tasks.",
        show_default=False,
    ),
    all: bool = Option(
        False,
        help="Deletes/clears all tasks",
        show_default=False,
    ),
) -> None:
    db.deleteTask(id, complete, all)


short_help = "Update a present Task"
help = "Update a Task -- change title or description -- from your list with the task-ID using update command."


@cliapp.command(
    name="update",
    help=help,
    short_help=short_help,
)
def updateTask(
    id: int = Argument(
        help="Task ID",
        show_default=False,
    ),
    title: str = Option(
        None,
        help="Provide new title of the task",
        show_default=False,
    ),
    description: str = Option(
        None,
        help="Provide new description of the task",
        show_default=None,
    ),
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
    first: int = Option(
        None,
        help="Shows first N tasks",
        show_default=False,
    ),
    last: int = Option(
        None,
        help="Shows last N tasks",
        show_default=False,
    ),
    complete: bool = Option(
        None,
        help="Show tasks that are completed. Use --no-complete to show incomplete task",
        show_default=False,
    ),
) -> None:
    if first and last:
        if first + last > db.getRowCount():
            table.composeTable(db.getTasks(n=None, status=complete))
        else:
            table.composeTable(db.getTasks(n=-last, status=complete))
            table.composeTable(db.getTasks(n=first, status=complete))
    elif first:
        table.composeTable(db.getTasks(n=first, status=complete))
    elif last:
        table.composeTable(db.getTasks(n=-last, status=complete))
    else:
        table.composeTable(db.getTasks(n=None, status=complete))
    table.renderTable()


short_help = "Complete a task"
help = "Mark a task as completed. When a task is complete the status field is marked FINISHED."


@cliapp.command(name="complete", help=help, short_help=short_help)
def completeTask(
    id: int = Argument(
        help="ID of task which is to be marked complete. Specifying 0 marks all current pending task as complete.",
        show_default=False,
    ),
):
    db.updateStatus(id, True)


if __name__ == "__main__":
    db.createTable()
    cliapp()
    db.conn.close()
