"""Module for tui elements"""

import sys
import os

if os.name == "nt":
    from .os_interfaces.windows_interface import get_key, clear
else:
    from .os_interfaces.linux_interface import get_key, clear



def t_clear():
    """
    Clear the terminal.
    """
    clear()


def t_scroll_clear():
    """
    Clear the terminal.
    """
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()


def t_message(message: str):
    """
    Display a message in the terminal and wait for the user to press a key.
    :param message: The message to display.
    """
    sys.stdout.write(f"{message}")
    sys.stdout.write("\n\nPress any key to continue...")
    sys.stdout.flush()
    get_key()
    sys.stdout.write("\n\n")
    sys.stdout.flush()


def t_question(question: str) -> str:
    """
    Ask a question in the terminal and return the answer.
    :param question: The question to ask.
    :return: The answer to the question.
    """
    sys.stdout.write(f"{question}")
    sys.stdout.flush()
    inp = input()
    sys.stdout.write("\n")
    sys.stdout.flush()
    return inp


def t_select(
    title: str,
    options: list[str],
    arrow: str = "\033[1;34m>\033[0m",
    *,
    allow_q: bool = False,
) -> str | None:
    """
    Display a menu in the terminal and return the selected option.
    :param title: The title of the menu.
    :param options: The options to display.
    :param arrow: The arrow to display next to the selected option.
    :param allow_q: Whether to allow 'q' to quit.
    :return: The selected option or None if 'q' was pressed.
    """
    current_option = 0
    option_count = len(options)

    def print_menu():
        # Only clear the current line and reprint options
        for _ in range(option_count + 2):  # +2 for title and the line below it
            sys.stdout.write("\r\x1b[K")  # Clear the entire line
            sys.stdout.write("\x1b[1A")  # Move cursor one line up
        sys.stdout.write("\r\x1b[K")  # Clear the line with the title

        # Reprint the menu
        sys.stdout.write(title + "\n")
        sys.stdout.write("-" * len(title) + "\n")
        for index, option in enumerate(options):
            prefix = arrow if index == current_option else " "
            sys.stdout.write(f"{prefix} {option}\n")
        sys.stdout.flush()

    for _ in range(option_count + 2):
        sys.stdout.write("\n")
        sys.stdout.flush()

    print_menu()

    while True:
        key = get_key()

        if key in ["P", "j"]:
            if current_option < option_count - 1:
                current_option += 1
            print_menu()

        elif key in ["H", "k"]:
            if current_option > 0:
                current_option -= 1
            print_menu()

        elif allow_q and key == "q":  # Allow 'q' to quit as well
            sys.stdout.write("\n")  # Move the cursor down to the end of the menu
            sys.stdout.flush()
            return None

        if key in ["\r", "\n", " "]:  # Enter key (carriage return or newline)
            sys.stdout.write("\n")  # Move the cursor down to the end of the menu
            sys.stdout.flush()
            return options[current_option]


def t_multi_select(
    title: str,
    options: list[str],
    *,
    arrow: str = "\033[1;34m>\033[0m",
    tick: str = "\033[1;32mx\033[0m",
    finish_option: str = "Done",
) -> list[str]:
    """
    Display a menu in the terminal and allow the user to select multiple options.
    :param title: The title of the menu.
    :param options: The options to display.
    :param arrow: The arrow to display next to the current option.
    :param tick: The symbol to represent selected options.
    :param finish_option: The text to display for finishing selection.
    :return: A list of selected options.
    """
    selected_options = [False] * len(
        options
    )  # A list to keep track of which options are selected
    current_option = 0  # Currently highlighted option


    def print_menu():
        # Clear the screen and reprint the menu
        for _ in range(
            len(options) + 3
        ):  # +3 for title, the line below it, and the "Done" option
            sys.stdout.write("\r\x1b[K")  # Clear the entire line
            sys.stdout.write("\x1b[1A")  # Move cursor one line up
        sys.stdout.write("\r\x1b[K")  # Clear the line with the title

        # Reprint the menu
        sys.stdout.write(title + "\n")
        sys.stdout.write("-" * len(title) + "\n")
        for index, option in enumerate(options):
            prefix = arrow if index == current_option else " "
            tick_mark = tick if selected_options[index] else " "
            sys.stdout.write(f"{tick_mark} {prefix} {option}\n")
        sys.stdout.write(
            f"  {arrow if current_option == len(options) else ' '} {finish_option}\n"
        )

    for _ in range(len(options) + 3):
        sys.stdout.write("\n")

    print_menu()

    while True:
        key = get_key()

        if key in ["P", "j"]:  # Arrow down or 'j' for down
            if current_option < len(
                options
            ):  # Ensure current_option does not go beyond 'Done'
                current_option += 1
            else:
                current_option = 0  # Wrap around to the first option
            print_menu()

        elif key in ["H", "k"]:  # Arrow up or 'k' for up
            if current_option > 0:
                current_option -= 1
            else:
                current_option = len(options)  # Wrap around to 'Done'
            print_menu()

        elif key in ["\r", "\n", " "]:  # Space bar to select or deselect
            if current_option == len(options):
                sys.stdout.write("\n")
                break

            selected_options[current_option] = not selected_options[current_option]
            print_menu()

    # Return the list of selected options
    return [option for option, selected in zip(options, selected_options) if selected]


if __name__ == "__main__":
    t_scroll_clear()
    MY_QUESTION = "This is a t_question: "
    answer = t_question(MY_QUESTION)
    t_message(f"You answered: {answer}")

    MY_TITLE = "This is a t_select:"
    my_options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
    SELECTED_OPTION = t_select(title=MY_TITLE, options=my_options)
    t_message(f"You selected: {SELECTED_OPTION}")

    MY_TITLE = "This is a t_multi_select:"
    my_options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
    SELECTED_OPTIONS = t_multi_select(title=MY_TITLE, options=my_options)
    t_message(f"You selected: {', '.join(SELECTED_OPTIONS)}")
    t_clear()
