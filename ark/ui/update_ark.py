import argparse
import requests
import os

URL = 'http://127.0.0.1:8000/update'
DEFAULT_KEY = os.environ['ARK_API_KEY']

def send_put_request(update_url, auth, ark, **kwargs):
    data = {'ark': ark}
    for key, value in kwargs.items():
        if value is not None:
            data[key] = value

    if not auth:
        auth = DEFAULT_KEY
    print(data)
    response = requests.put(update_url, json=data, headers={'Authorization': auth})

    if response.status_code == 200:
        print("PUT request successful.")
    else:
        print(f"PUT request failed. Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a given ARK.")
    parser.add_argument("ark", help="Value for the 'ark' parameter")
    parser.add_argument("--url", help="Value for the 'url' parameter (optional)")
    parser.add_argument("--metadata", help="Value for the 'metadata' parameter (optional)")
    parser.add_argument("--title", help="Value for the 'title' parameter (optional)")
    parser.add_argument("--type", help="Value for the 'type' parameter (optional)")
    parser.add_argument("--rights", help="Value for the 'rights' parameter (optional)")
    parser.add_argument("--identifier", help="Value for the 'identifier' parameter (optional)")
    parser.add_argument("--format", help="Value for the 'format' parameter (optional)")
    parser.add_argument("--relation", help="Value for the 'relation' parameter (optional)")
    parser.add_argument("--source", help="Value for the 'source' parameter (optional)")
    parser.add_argument("--auth", help="API key")
    args = parser.parse_args()

    send_put_request(URL, **vars(args))
