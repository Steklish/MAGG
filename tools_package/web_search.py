from .imports_for_tools import *

google_search_api = "AIzaSyCIkSFFwm_evB1UzTl_YPb_CaL5udRaYWM"
search_engine_id = '72dab577d8eff4361'



web_search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": (
            "Use this tool to search the web to get facts or recent uodates."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A query to be searched."
                }
            },
            "required": ["query"]
        }
    }
}


def web_search(query:str):
    results = google_custom_search(google_search_api, search_engine_id, query, num_results=5)
    results += google_custom_search_images(google_search_api, search_engine_id, query, num_results=5)
    return json.dumps(results, ensure_ascii=False)
    

def google_custom_search(api_key, search_engine_id, query, num_results=10):
    """
    Perform a search using Google Custom Search JSON API.

    :param api_key: Your Google API key.
    :param search_engine_id: Your Custom Search Engine ID.
    :param query: The search query.
    :param num_results: Number of results to return (default is 10).
    :return: A list of search results.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'num': num_results
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        search_results = response.json()
        
        # Extract relevant information from the response
        results = []
        for item in search_results.get('items', []):
            result = {
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet')
            }
            results.append(result)
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return ["Error finding web pages"]

def google_custom_search_images(api_key, search_engine_id, query, num_results=5):
    """
    Perform an image search using Google Custom Search JSON API.

    :param api_key: Your Google API key.
    :param search_engine_id: Your Custom Search Engine ID.
    :param query: The search query.
    :return: A list of image search results.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'num': num_results,
        'searchType': 'image'  # Specify that we want image results
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        search_results = response.json()
        print(search_results)  # Print the full response for debugging
        
        # Extract relevant information from the response
        results = []
        for item in search_results.get('items', []):
            result = {
                'title': item.get('title'),
                'link': item.get('link'),  # URL of the image
            }
            results.append(result)
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        print(response.text)  # Print the error response for debugging
        return ["Error finding images"]
