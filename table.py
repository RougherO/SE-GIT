from rich.table import Table
from rich.console import Console

console = Console()

_table = Table(
    "ID",
    "Title",
    "Description",
    "Status",
    title="TaskList",
    expand=True,
)


def composeTable(rows) -> None:
    for row in rows:
        _table.add_row(
            *map(lambda elem: str(elem), row[:-1]),
            "FINISHED" if row[-1] else "PENDING",
        )


def renderTable() -> None:
    console.print(_table)
