def format_evolution_chain(chain_data, name_to_highlight):
    """
    Creates a formatted string representing the evolution chain.
    The name of the Pokémon to highlight is displayed in green.
    :param chain_data: The evolution chain data.
    :param name_to_highlight: The name of the Pokémon to highlight.
    :return: A formatted string representing the evolution chain, intended for display in the console.
    """
    # Extract the Pokémon names from the chain data
    names = []
    current_pokemon = chain_data.get("chain", {})
    while current_pokemon:
        names.append(current_pokemon.get("species", {}).get("name", ""))
        evolves_to = current_pokemon.get("evolves_to", [])
        current_pokemon = evolves_to[0] if evolves_to else None

    # If there are no names, return a message indicating no evolutions
    if not names:
        return "This Pokémon has no known evolutions."

    # Create a formatted string with the Pokémon names in the chain
    return " -> ".join([
        f"\033[92m{name.capitalize()}\033[0m" if name == name_to_highlight
        else name.capitalize()
        for name in names
    ])

def snake_case_to_title_case(input_string):
    """
    Formats a snake_case string to a Title Case string.
    :param input_string: The snake_case string to format.
    """
    return input_string.title().replace("-", " ")