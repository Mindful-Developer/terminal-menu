"""Windows-specific implementations of msvcrt and os functions"""

import msvcrt  # pylint: disable=import-error
import os


def clear():
    """
    Clear the terminal.
    """
    os.system("cls")


def get_key() -> str:
    """
    Get a single character input from the console.
    :return: The character input.
    """
    # Read a single character
    key = msvcrt.getch()

    # If it's the escape character, expect a bracket and read the next byte
    if key == b"\xe0":
        key = msvcrt.getch()
    return key.decode()
