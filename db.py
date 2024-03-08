import sqlite3

from task import Task

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()


def createTable():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS TASKS (
        TITLE TEXT,
        DESCRIPTION TEXT,
        STATUS INTEGER DEFAULT 0)"""
    )


def insertTask(task: Task) -> None:
    task.id = cursor.lastrowid + 1 if cursor.lastrowid else 1
    cursor.execute(
        'INSERT INTO TASKS(TITLE, DESCRIPTION) VALUES ("{}", "{}")'.format(
            task.title,
            task.description,
        )
    )
    conn.commit()


def deleteTask(id: int | None = None) -> None:
    cursor.execute(
        "DELETE FROM TASKS WHERE ROWID={}".format(id)
        if id
        else "DELETE FROM TASKS WHERE ROWID = (SELECT MAX(ROWID) FROM TASKS)"
    )
    conn.commit()


def updateTask(id: int, title: str = None, description: str = None):
    if title:
        cursor.execute(
            'UPDATE TASKS SET TITLE="{}" WHERE ROWID={}'.format(
                title,
                id,
            )
        )
    if description:
        cursor.execute(
            'UPDATE TASKS SET DESCRIPTION="{}" WHERE ROWID={}'.format(
                description,
                id,
            )
        )
    conn.commit()


def getTasks(n: int | None = None):
    command = (
        (
            "SELECT ROWID, T.* FROM TASKS AS T WHERE ROWID > (SELECT COUNT(*) - {} FROM TASKS)".format(
                -n
            )
            if n < 0
            else "SELECT ROWID, T.* FROM TASKS AS T WHERE ROWID <= {}".format(n)
        )
        if n
        else "SELECT ROWID, T.* FROM TASKS AS T"
    )

    for row in cursor.execute(command):
        yield row


def getRowCount():
    return cursor.execute("SELECT COUNT(*) FROM TASKS").fetchone()[0]


def updateStatus(id: int, status: bool):
    cursor.execute(
        "UPDATE TASKS SET STATUS={} WHERE ID={}".format(
            status,
            id,
        )
    )
    conn.commit()
