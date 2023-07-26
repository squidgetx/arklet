import argparse
import requests
import os

URL = 'http://127.0.0.1:8000/mint'
DEFAULT_KEY = os.environ['ARK_API_KEY']

def send_mint_request(mint_url, **kwargs):
    auth = kwargs.pop('auth')
    if auth is None:
        auth = DEFAULT_KEY
    data = {}
    for key, value in kwargs.items():
        if value is not None:
            data[key] = value

    print(data)
    response = requests.post(mint_url, json=data, headers={'Authorization': auth})

    if response.status_code == 200:
        print("POST request successful.")
    else:
        print(f"POST request failed. Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mint a new ARK") 
    parser.add_argument("naan", help="Value for the 'naan' parameter")
    parser.add_argument("shoulder", help="Value for the 'shoulder' parameter")
    parser.add_argument("name", help="Value for the 'name' parameter")
    parser.add_argument("--url", help="Value for the 'url' parameter (optional)")
    parser.add_argument("--metadata", help="Value for the 'metadata' parameter (optional)")
    parser.add_argument("--title", help="Value for the 'title' parameter (optional)")
    parser.add_argument("--type", help="Value for the 'type' parameter (optional)")
    parser.add_argument("--commitment", help="Value for the 'commitment' parameter (optional)")
    parser.add_argument("--identifier", help="Value for the 'identifier' parameter (optional)")
    parser.add_argument("--format", help="Value for the 'format' parameter (optional)")
    parser.add_argument("--relation", help="Value for the 'relation' parameter (optional)")
    parser.add_argument("--source", help="Value for the 'source' parameter (optional)")
    parser.add_argument("--auth", help="API key")
    args = parser.parse_args()

    send_mint_request(URL, **vars(args))
