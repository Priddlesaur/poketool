import requests
from requests import HTTPError

# Base URL for the PokeAPI
API_URL = "https://pokeapi.co/api/v2/"
ALL_POKEMON_ENDPOINT = "pokemon"
POKEMON_SPECIES_ENDPOINT = "pokemon-species"

# Global variable to store the Pokemon cache
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

        print(f"GET {response.url} -> {response.status_code}")

        # Return None if the request was unsuccessful
        if response.status_code != 200:
            return None

        # Return the JSON response
        return response.json()

    # Handle connection errors and HTTP errors
    except requests.exceptions.ConnectionError | HTTPError:
        return None

def fetch_or_get_pokemon_cache():
    """
    Caches all Pokemon names and URLs from the PokeAPI.
    :return: A dictionary mapping Pokemon names to their URLs.
    """
    # Use a global variable to store the cache
    global pokemon_cache

    # If the cache is empty, fetch all Pokemon and store them in the cache
    if not pokemon_cache:
        fetched_data = fetch_all_pokemon()
        pokemon_cache = {pokemon["name"]: pokemon["url"] for pokemon in fetched_data["results"]}

    # Return the cache
    return pokemon_cache

def fetch_or_get_pokemon_by_name(pokemon_name):
    """
    Fetches a Pokemon by its name from the PokeAPI.
    :param pokemon_name: The name of the Pokemon to fetch.
    :return: The JSON response from the API in dictionary format.
    """
    # Get the URL for the given Pokemon name from the cache
    pokemon_url = fetch_or_get_pokemon_cache().get(pokemon_name, None)
    if not pokemon_url:
        return None

    # Fetch the Pokemon data from the API
    return fetch(pokemon_url)

def fetch_all_pokemon():
    """
    Fetches a list of all Pokemon from the PokeAPI.
    :return: The JSON response from the API in dictionary format.
    """
    return fetch(f"{API_URL}{ALL_POKEMON_ENDPOINT}", {"limit": 2000})

def fetch_pokemon_species(pokemon_id):
    """
    Fetches the species information for a Pokemon by its ID from the PokeAPI.
    :param pokemon_id: The ID of the Pokemon to fetch.
    :return: The JSON response from the API in dictionary format.
    """
    return fetch(f"{API_URL}{POKEMON_SPECIES_ENDPOINT}/{pokemon_id}")

def fetch_evolution_chain(pokemon_id):
    """
    Fetches the evolution chain for a Pokemon by its ID from the PokeAPI.
    :param pokemon_id: The ID of the Pokemon to fetch.
    :return: The JSON response from the API in dictionary format.
    """
    species = fetch_pokemon_species(pokemon_id)
    if not species:
        return None

    # Get the evolution chain URL from the species data
    evolution_chain_url = species["evolution_chain"]["url"]
    return fetch(evolution_chain_url)
