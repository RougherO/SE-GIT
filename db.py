import sqlite3

from task import Task

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()


def createTable():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS TASKS (
        ID INTEGER AUTOINCREMENT,
        TITLE TEXT,
        DESCRIPTION TEXT,
        STATUS INTEGER)"""
    )


def insertTask(task: Task) -> None:
    task.id = cursor.lastrowid + 1 if cursor.lastrowid else 1
    cursor.execute(
        f"""INSERT INTO TASKS VALUES (
            {task.id},
            {task.title},
            {task.description},
            {task.status})"""
    )
    conn.commit()


def deleteTask(id: int) -> None:
    cursor.execute(f"""DELETE FROM TASKS WHERE ID={id}""")
    conn.commit()


def updateTask(id: int, title: str = None, description: str = None):
    if title:
        cursor.execute(
            f"""UPDATE TASKS SET 
            TITLE={title},
            WHERE ID={id}
            """
        )
    if description:
        cursor.execute(
            f"""UPDATE TASKS SET 
            DESCRIPTION={description},
            WHERE ID={id}
            """
        )
    conn.commit()


def updateStatus(id: int, status: bool):
    cursor.execute(f"UPDATE TASKS SET STATUS={status} WHERE ID={id}")
    conn.commit()
