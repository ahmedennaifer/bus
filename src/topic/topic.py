class Topic:
    def __init__(self, name: str) -> None:
        self.name = name
        self._messages = []

    def __repr__(self):
        return f"Topic(Name:{self.name})"
