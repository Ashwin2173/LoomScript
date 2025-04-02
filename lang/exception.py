class LoomSyntaxError(Exception):
    def __init__(self, message: str, line: int = None) -> None:
        super().__init__(message)
        self.line = line
