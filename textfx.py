class Colors:
    # Colours for fancy text for the user
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_blue(message: str):
    """Prints a message in blue if the terminal supports it.

    Args:
        message (str): The message to be printed.
    """
    print(Colors.OKBLUE + message + Colors.ENDC)


def print_green(message: str):
    """Prints a message in green if the terminal supports it.

    Args:
        message (str): The message to be printed.
    """
    print(Colors.OKGREEN + message + Colors.ENDC)


def print_info(message: str):
    """Prints a message in yellow if the terminal supports it.

    Args:
        message (str): The message to be printed.
    """
    print(Colors.WARNING + message + Colors.ENDC)


def print_error(message: str):
    """Prints a message in red if the terminal supports it.

    Args:
        message (str): The message to be printed.
    """
    print(Colors.FAIL + message + Colors.ENDC)


def print_header(message: str):
    """Prints an purple message if the terminal supports it.

    Args:
        message (str): The message to be printed.
    """
    print(Colors.HEADER + message + Colors.ENDC)


def print_emph(message: str):
    """Prints an underlined message if the terminal supports it.

    Args:
        message (str): The message to be printed.
    """
    print(Colors.UNDERLINE + message + Colors.ENDC)
