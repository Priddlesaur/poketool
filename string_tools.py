def get_evolutions(chain_data):
    """
    Creates a list of Pokémon names in the evolution chain.
    :param chain_data: The evolution chain data.
    :return: A list of Pokémon names in the evolution chain.
    """
    # Extract the evolution chain from the response
    output_chain = []
    current_pokemon = chain_data["chain"]
    while current_pokemon:
        output_chain.append(current_pokemon["species"]["name"])
        current_pokemon = current_pokemon.get("evolves_to", [])[0] if current_pokemon.get("evolves_to") else None

    # Return the list of Pokémon names in the evolution chain
    return output_chain

def format_evolution_chain(chain, highlight):
    """
    Creates a formatted string representing the evolution chain.
    :param chain: The list of Pokémon names in the evolution chain.
    :param highlight: The name of the Pokémon to highlight.
    :return: A formatted string representing the evolution chain.
    """
    return " -> ".join([f"\033[92m{pokemon.capitalize()}\033[0m" if pokemon == highlight else pokemon.capitalize() for pokemon in chain])

def snake_case_to_title(type_name):
    """
    Formats the Pokémon type name to be more readable.
    :param type_name: The type name to format.
    """
    return type_name.title().replace("-", " ")