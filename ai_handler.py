import prefs
from datetime import datetime
from stuff import *
from google.genai import client, types

from openai import OpenAI


# Initialize original GOOGLE client
client_google = client.Client(api_key=prefs.api_google_key)

# Initialize openrouter client
client = OpenAI(base_url=prefs.base_url, api_key=prefs.api_key)
