import argparse
import requests
import statistics
import os

URL = 'http://ark.frick.org'

def send_get_request(get_url, ark, **kwargs):
    response = requests.get(get_url)

    if response.status_code == 200:
        print("GET request successful.")
    else:
        print(f"GET request failed. Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch random ARKs.")
    parser.add_argument('file')
    args = parser.parse_args()
    times = []
    responses = []
    with open(args.file, 'rt') as arkfile:
        for line in arkfile:
            url = f'{URL}/ark://{line}'
            print(url)
            response = requests.get(url, 
                                    allow_redirects=False,
                                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
            )
            if (response.status_code == 302):
                redirect_location = response.headers.get('location')
                print("302:", redirect_location)
            else:
                print(response.status_code)
            secs = response.elapsed.total_seconds()
            times.append(secs)
    avg = sum(times)/len(times)
    print(f"avg time (s) was {avg}")

    standard_deviation = statistics.stdev(times)
    print(f"sd {standard_deviation}")



