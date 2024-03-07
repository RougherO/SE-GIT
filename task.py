class Task:
    id: int
    title: str
    description: str
    status: bool = False

    def __init__(self, title: str) -> None:
        self.title = title

    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description

    def update_status(self, status: bool) -> None:
        self.status = status

    def update_description(self, description: str) -> None:
        self.description = description

    def update_title(self, title: str) -> None:
        self.title = title
