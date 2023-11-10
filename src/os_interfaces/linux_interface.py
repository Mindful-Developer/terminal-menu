"""Linux-specific implementations for os, sys, tty, and termios functions."""

import sys
import os
import tty
import termios  # pylint: disable=import-error


def clear():
    """
    Clear the terminal.
    """
    os.system("clear")


def get_key() -> str:
    """
    Get a single character input from the console.
    :return: The character input.
    """
    # Save the current terminal state
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())  # Set the terminal to raw mode

        # Read a single character
        ch = sys.stdin.read(1)

        # If it's the escape character, expect a bracket and read two more bytes
        if ch == "\x1b":
            ch = sys.stdin.read(2)
        return ch
    finally:
        # Restore the terminal to its previous state
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
