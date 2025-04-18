from .imports_for_tools import *

google_search_api = "AIzaSyCIkSFFwm_evB1UzTl_YPb_CaL5udRaYWM"
search_engine_id = '72dab577d8eff4361'



google_web_search_tool = genai.types.Tool(
    function_declarations=[
        genai.types.FunctionDeclaration(
            name="web_search",
            description=(
                "This tool is useful for gathering external insights, answering recent queries, images, web pages information, etc."
                "It should be invoked whenever external data is required."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "query": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "The search query to input for retrieving relevant information. "
                            "Use keywords or specific phrases to refine the search results."
                        ),
                    ),
                },
                required=["query"],
            ),
        ),
    ]
)



def web_search(query:str):
    results = "[web pages] "
    results += str(google_custom_search(google_search_api, search_engine_id, query, num_results=4))
    results += " [images urls]"
    results += str(google_custom_search_images(google_search_api, search_engine_id, query, num_results=10))
    return json.dumps(results, ensure_ascii=False)
    

def google_custom_search(api_key, search_engine_id, query, num_results=10):
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

def google_custom_search_images(api_key, search_engine_id, query, num_results=8):

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
        # print(search_results)  # Print the full response for debugging
        
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
