import requests
from requests import HTTPError

# Constants for the PokeAPI
API_URL = "https://pokeapi.co/api/v2/"
ALL_POKEMON_ENDPOINT = "pokemon"
ALL_POKEMON_LIMIT = 2000
POKEMON_SPECIES_ENDPOINT = "pokemon-species"
SUCCESS_STATUS_CODE = 200

# Global variable to store the Pokémon cache
pokemon_cache = None

def fetch(url, params=None):
    """
    Helper function to make a GET request to the PokeAPI.
    :param url: The URL endpoint to fetch data from.
    :param params: Optional query parameters.
    :return: The JSON response from the API in dictionary format.
    """
    # Try to make the request
    try:
        # Make the GET request
        response = requests.get(f"{url}", params=params)

        # Return None if the request was unsuccessful
        if response.status_code != SUCCESS_STATUS_CODE:
            return None

        # Return the JSON response
        return response.json()

    # Handle connection errors and HTTP errors
    except (requests.ConnectionError, HTTPError):
        return None

def fetch_or_get_pokemon_cache():
    """
    Caches all Pokémon names and URLs from the PokeAPI.
    :return: A dictionary mapping Pokémon names to their URLs.
    """
    # Use a global variable to store the cache
    global pokemon_cache

    # If the cache is empty, fetch all Pokémon and store them in the cache
    if not pokemon_cache:
        fetched_data = fetch_all_pokemon()
        pokemon_cache = {pokemon["name"]: pokemon["url"] for pokemon in fetched_data["results"]}

    # Return the cache
    return pokemon_cache

def fetch_or_get_pokemon_by_name(pokemon_name):
    """
    Fetches a Pokémon by its name from the PokeAPI.
    :param pokemon_name: The name of the Pokémon to fetch.
    :return: The JSON response from the API in dictionary format.
    """
    # Get the URL for the given Pokémon name from the cache
    pokemon_url = fetch_or_get_pokemon_cache().get(pokemon_name, None)
    if not pokemon_url:
        return None

    # Fetch the Pokémon data from the API
    return fetch(pokemon_url)

def fetch_all_pokemon():
    """
    Fetches a list of all Pokémon from the PokeAPI.
    :return: The JSON response from the API in dictionary format.
    """
    return fetch(f"{API_URL}{ALL_POKEMON_ENDPOINT}", {"limit": ALL_POKEMON_LIMIT})

def fetch_pokemon_species(pokemon_id):
    """
    Fetches the species information for a Pokémon by its ID from the PokeAPI.
    :param pokemon_id: The ID of the Pokémon to fetch.
    :return: The JSON response from the API in dictionary format.
    """
    return fetch(f"{API_URL}{POKEMON_SPECIES_ENDPOINT}/{pokemon_id}")

def fetch_evolution_chain(pokemon_id):
    """
    Fetches the evolution chain for a Pokémon by its ID from the PokeAPI.
    :param pokemon_id: The ID of the Pokémon to fetch.
    :return: The JSON response from the API in dictionary format.
    """
    species = fetch_pokemon_species(pokemon_id)
    if not species:
        return None

    # Get the evolution chain URL from the species data
    evolution_chain_url = species["evolution_chain"]["url"]
    return fetch(evolution_chain_url)
