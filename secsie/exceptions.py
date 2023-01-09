"""
exceptions.py

Contains all the custom exceptions thrown by secsie.
"""


class InvalidSyntax(SyntaxError):
    """
    This happens when the config you're trying to parse is invalid.
    """

    def __init__(self, error_message: str, line_number: int):
        super().__init__(f"Invalid syntax on line {line_number}: {error_message}")
        self.lineno = line_number
