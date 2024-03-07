import sqlite3

from task import Task

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()


def createTable():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS TASKS (
        TITLE TEXT,
        DESCRIPTION TEXT,
        STATUS INTEGER)"""
    )


def insertTask(task: Task) -> None:
    task.id = cursor.lastrowid + 1 if cursor.lastrowid else 1
    cursor.execute(
        """INSERT INTO TASKS VALUES (
            ?,
            ?,
            ?)""",
        (
            task.title,
            task.description,
            task.status,
        ),
    )
    conn.commit()


def deleteTask(id: int) -> None:
    cursor.execute("""DELETE FROM TASKS WHERE ROWID=?""", (id,))
    conn.commit()


def updateTask(id: int, title: str = None, description: str = None):
    if title:
        cursor.execute(
            """UPDATE TASKS SET 
            TITLE=?
            WHERE ROWID=?
            """,
            (
                title,
                id,
            ),
        )
    if description:
        cursor.execute(
            """UPDATE TASKS SET 
            DESCRIPTION=?
            WHERE ROWID=?
            """,
            (
                description,
                id,
            ),
        )
    conn.commit()


def getTasks(n: int | None = None):
    for row in cursor.execute("SELECT ROWID, T.* FROM TASKS AS T"):
        yield row


def updateStatus(id: int, status: bool):
    cursor.execute(
        "UPDATE TASKS SET STATUS=? WHERE ID=?",
        (
            status,
            id,
        ),
    )
    conn.commit()
