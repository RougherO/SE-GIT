from rich.table import Table
from rich.console import Console
from task import Task

console = Console()

table = Table(
    "ID",
    "Title",
    "Description",
    "Status",
    title="TaskList",
    expand=True,
)


def renderTable(rows) -> None:
    for row in rows:
        table.add_row(
            *map(lambda elem: str(elem), row[:-1]),
            "FINISHED" if row[-1] else "PENDING",
        )
    console.print(table)
