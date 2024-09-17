import json

HISTORY_FILE = "history.json"
HISTORY_MAX_ENTRIES = 10

pokemon_history = []

def add_to_history_file(pokemon_name):
    """
    Adds a Pokémon name to the history file.
    :param pokemon_name: The name of the Pokémon to add to the history.
    """
    global pokemon_history

    # Check if the Pokemon name is already in the history
    if pokemon_name in pokemon_history:
        return

    # Add the Pokemon name to beginning of the history list
    pokemon_history.insert(0, pokemon_name)

    # Write the updated history back to the file, but
    # only keep the last HISTORY_MAX_ENTRIES entries
    with open(HISTORY_FILE, "w") as file:
        json.dump(pokemon_history[:HISTORY_MAX_ENTRIES], file)

def load_history_file():
    """
    Loads the history file into the pokemon_history list.
    """
    global pokemon_history

    # Load the history file
    try:
        with open(HISTORY_FILE, "r") as file:
            pokemon_history = list(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file is not found or if the file is empty or malformed,
        # initialize the history list to an empty list
        pokemon_history = []
