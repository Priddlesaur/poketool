COLOR_SUCCESS = "\033[92m"  # Green
COLOR_ERROR = "\033[91m"  # Red
COLOR_RESET = "\033[0m"  # Reset

def print_success(message):
    """
    Prints a success message in green.
    :param message: The success message to print.
    """
    print(f"{COLOR_SUCCESS}{message}{COLOR_RESET}")

def print_error(message):
    """
    Prints an error message in red.
    :param message: The error message to print.
    """
    print(f"{COLOR_ERROR}Error: {message}{COLOR_RESET}")

def select_option(header, options, default_value = ""):
    """
    Allows the user to select an option from a list of options.
    :param header: The header to display.
    :param options: A list of options to choose from.
    :param default_value: The index of the default option.
    :return: The selected option.
    """
    while True:
        if header is not None:
            print_success(f"\n=== {header} ===")

        # Print the options
        for key, value in options:
            print(f"[{key}] {value}")

        # Get the user's choice
        choice = input("Select an option: ").lower()

        # If the user didn't enter a choice, use the default
        if not choice:
            choice = str(default_value)

        # Check if the choice is valid
        if choice in [str(key) for key, _ in options]:
            return choice

        # Print an error message if the choice is invalid
        print_error("Invalid choice. Please try again.")
