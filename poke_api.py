'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_info() function
    # Use breakpoints to view returned dictionary
    poke_info = get_pokemon_info("Rockruff")
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon = str(pokemon).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def get_pokemon_names():
    """Gets a list of all Pokemon names from the PokeAPI.

    Returns:
        list: List of all Pokemon names
    """
    url = POKE_API_URL + "?limit=1000"  
    response = requests.get(url)
    data = response.json()
    return [entry['name'] for entry in data['results']]

def download_image(image_url, save_path):
    """Downloads and saves a Pokemon artwork image from the provided URL.

    Args:
        image_url (str): URL of the image to download
        save_path (str): Path to save the downloaded image
    """
    response = requests.get(image_url)
    with open(save_path, 'wb') as image_file:
        image_file.write(response.content)

if __name__ == '__main__':
    main()
