import history
from algorithms import levenshtein_distance
from command_line_tools import (
    print_error,
    print_success,
    select_option,
)
from history import add_to_history_file
from pokeapi import (
    fetch_or_get_pokemon_by_name,
    fetch_evolution_chain,
    fetch_or_get_pokemon_cache
)
from string_tools import (
    format_evolution_chain,
    snake_case_to_title_case
)

def show_main_menu():
    # Show the main menu options
    user_input = select_option("Main Menu", [
        ("1", "Search for a Pokémon"),
        ("2", "View Search History"),
        ("3", "↩ Exit Application")
    ])

    # Handle the user input
    match user_input:
        case "1":
            show_pokemon_search_menu()
        case "2":
            show_history_selection_menu()
        case "3":
            return False

    # Return True to continue running the main menu
    return True

def show_history_selection_menu():
    # Generate the history items with index numbers
    history_items = [(index, item.capitalize()) for index, item in enumerate(history.pokemon_history, start=1)]
    back_option = str(len(history_items) + 1)

    # Ask the user to select a Pokémon from the history
    user_input = select_option("Search History", history_items + [(back_option, "↩ Back to Main Menu")])

    # If the user chooses to go back, return
    if user_input == back_option:
        return

    # Show the options menu for the selected Pokémon
    pokemon_name = history.pokemon_history[int(user_input) - 1]
    pokemon_data = fetch_or_get_pokemon_by_name(pokemon_name)
    show_pokemon_options_menu(pokemon_data)

def show_pokemon_search_menu():
    """
    Finds a Pokémon by name and shows the options menu if the Pokémon is found.
    """
    pokemon_name = input("\nEnter the name of the Pokémon you want to find: ").strip().lower()
    if not pokemon_name:
        print_error("You didn't enter a Pokémon name.")
        return

    # Find the Pokémon by name
    pokemon_data = fetch_or_get_pokemon_by_name(pokemon_name)

    # If the Pokémon is not found, suggest a similar name
    if not pokemon_data:
        suggested_names = get_pokemon_suggestions(pokemon_name)
        back_option = str(len(suggested_names) + 1)

        # If the Pokémon is not found, print an error message
        print_error(f"Pokémon '{pokemon_name.capitalize()}' not found.")

        # Create a list of suggestion choices
        suggestion_options = [
            (str(index + 1), suggestion.capitalize()) for (index, suggestion) in enumerate(suggested_names)
        ]

        # Ask the user to select a suggestion, with
        # the default option being the back choice
        input_choice = select_option(
            "Suggestions",
            suggestion_options + [(back_option, "↩ Back to Main Menu")],
            back_option
        )

        # If the user chooses to go back, return
        if input_choice == back_option:
            print("Returning to main menu...")
            return

        # Fetch the Pokémon data for the selected suggestion
        pokemon_data = fetch_or_get_pokemon_by_name(suggested_names[int(input_choice) - 1])

    # Check one final time if the Pokémon is not found
    if not pokemon_data:
        print_error(f"Pokémon '{pokemon_name}' not found!")
        return

    # Show the options menu for the Pokémon
    while show_pokemon_options_menu(pokemon_data):
        pass

def show_pokemon_options_menu(pokemon_data):
    """
    Shows the options menu for a Pokémon.
    :param pokemon_data: The Pokémon data to show the options menu for.
    :return: True if the options menu should continue, False if the user wants to go back.
    """
    pokemon_name = pokemon_data["name"]

    # Add the Pokémon to the history
    add_to_history_file(pokemon_name)

    # Let the user choose an option until they go back
    option_index = select_option(f"Options Menu for {pokemon_name.capitalize()}", [
        ("1", "View Pokémon Stats"),
        ("2", "View Pokémon Evolution Chain"),
        ("3", "View Pokémon Moves"),
        ("4", "↩ Back to Main Menu"),
    ], "4")

    # Handle the selected option
    match option_index:
        case "1":
            view_pokemon_stats(pokemon_data)
        case "2":
            view_pokemon_evolution_chain(pokemon_data)
        case "3":
            view_pokemon_moves(pokemon_data)
        case "4" | _:
            print_success("Returning to Pokémon selection...")
            return False

    # Return true to continue showing the options menu for this Pokémon
    return True

def view_pokemon_stats(pokemon_data):
    """
    Prints the stats of a Pokémon.
    :param pokemon_data: The Pokémon data to display stats for.
    """
    print_success(f"\nStats for {pokemon_data['name'].capitalize()}:")
    print(f"Name: {pokemon_data['name'].capitalize()}")
    print(f"Height: {pokemon_data['height']}")
    print(f"Weight: {pokemon_data['weight']}")
    print(f"Base Experience: {pokemon_data['base_experience']}")
    print(f"Types: {', '.join(snake_case_to_title_case(pt['type']['name']) for pt in pokemon_data['types'])}")
    print(f"Abilities: {', '.join(snake_case_to_title_case(ability['ability']['name']) for ability in pokemon_data['abilities'])}")


def view_pokemon_evolution_chain(pokemon_data):
    """
    Fetches and prints the evolution chain of a Pokémon by name.
    :param pokemon_data: The Pokémon data to display the evolution chain for.
    """
    pokemon_id = pokemon_data["id"]
    pokemon_name = pokemon_data["name"]

    # Fetch the evolution chain for the Pokémon
    evolution_chain = fetch_evolution_chain(pokemon_id)
    if not evolution_chain:
        print_error(f"Evolution chain for {pokemon_name.capitalize()} not found.")
        return

    # Print the evolution chain
    print_success(f"\n=== Evolution Chain for {pokemon_name.capitalize()} ===")
    print(format_evolution_chain(evolution_chain, pokemon_name))

def view_pokemon_moves(pokemon_data):
    """
    Prints the moves of a Pokémon.
    :param pokemon_data: The Pokémon data to display moves for.
    """
    name = pokemon_data["name"]
    moves = sorted(pokemon_data["moves"], key=lambda move: move["move"]["name"])

    # Print the moves for the Pokémon
    print_success(f"\n=== Moves for {name.capitalize()} ===")
    for move in moves:
        print(f"- {snake_case_to_title_case(move["move"]["name"])}")

def get_pokemon_suggestions(input_name):
    """
    Suggests a Pokémon name based on the input name.
    :param input_name: The input name to suggest a Pokémon for.
    """
    # Get the Pokémon cache
    pokemon_cache = fetch_or_get_pokemon_cache()
    if not pokemon_cache:
        return None

    # Find the top 3 closest matches based on Levenshtein distance.
    return sorted(pokemon_cache.keys(), key=lambda name: levenshtein_distance(input_name, name))[:3]