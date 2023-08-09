import argparse
import requests
import statistics
import os

URL = 'http://127.0.0.1:8000'

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
    with open(args.file, 'rt') as arkfile:
        for line in arkfile:
            response = requests.get(f'{URL}/ark://{line}')
            secs = response.elapsed.total_seconds()
            times.append(secs)
    avg = sum(times)/len(times)
    print(f"avg time (s) was {avg}")

    standard_deviation = statistics.stdev(times)
    print(f"sd {standard_deviation}")


