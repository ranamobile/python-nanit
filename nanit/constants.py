import os

PROJECT_DIRECTORY = os.path.dirname(__file__)
NANIT_AUTH_FILE = os.path.join(PROJECT_DIRECTORY, "nanit-app-token.json")
NANIT_API_URL = "https://api.nanit.com"
NANIT_API_HEADERS = {
    "nanit-api-version": "1",
}
