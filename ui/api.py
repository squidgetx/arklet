import requests
import csv
import argparse
import json
import os

DEFAULT_URL = 'http://127.0.0.1:8000'
DEFAULT_KEY = os.environ['ARK_API_KEY']

MINT_FIELDS = [
    'naan',
    'shoulder',
    'url',
    'metadata',
    'title',
    'type',
    'commitment',
    'identifier',
    'format',
    'relation',
    'source',
    'auth',
    'csv'
]

UPDATE_FIELDS = MINT_FIELDS + ['ark']

GET = 'get'
POST = 'post'
PUT = 'put'

class ArkAPIError(Exception):
    pass

def query(method, url, **kwargs):
    url = DEFAULT_URL + '/' + url
    if method == GET:
        response = requests.get(url)
    elif method == POST:
        response = requests.post(url, **kwargs)
    elif method == PUT:
        response = requests.put(url, **kwargs)
    if response.status_code == 200:
        return response.json()
    else:
        raise ArkAPIError(f"Request failed: {response.status_code}, {response.text}")


def query_ark(data):
    assert data['ark'], "Must include --ark argument"
    return query(GET, data['ark'] + '?json')

def authorized(method, url, data):
    auth = data.get('auth', '')
    if auth == '':
        auth = DEFAULT_KEY
    del data['auth']
    return query(method, url, json=data, headers={'Authorization': auth})

def update_ark(data: dict):
    assert data['ark'], "Must include --ark argument"
    return authorized(PUT, '/update', data)

def mint_ark(data: dict):
    return authorized(POST, '/mint', data)

def csv2json(csvfile):
    reader = csv.DictReader(open(csvfile, 'rt'))
    return [r for r in reader]

def query_arks(data: dict):
    assert data['csv'], "Must include --csv argument for bulk operations"
    jsondata = csv2json(data['csv'])
    assert 'ark' in jsondata[0], "CSV for bulk ark querying must include 'ark' column"
    return query(POST, 'bulk_query', json=jsondata)

def update_arks(data: dict):
    assert data['csv'], "Must include --csv argument for bulk operations"
    jsondata = csv2json(data['csv'])
    assert 'ark' in jsondata[0], "CSV for bulk ark querying must include 'ark' column"
    return query(POST, 'bulk_update', json=jsondata)

def mint_arks(data: dict):
    assert data['csv'], "Must include --csv argument for bulk operations"
    raise NotImplementedError

ENDPOINTS = [
    query_ark,
    update_ark,
    mint_ark,
    query_arks,
    update_arks,
    mint_arks
] 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARK API command line suite")
    parser.add_argument('action', help='API Action you wish to execute', choices=[f.__name__ for f in ENDPOINTS])
    for f in UPDATE_FIELDS:
        parser.add_argument(f"--{f}", help=f)
    
    args = parser.parse_args()
    action_func = locals()[args.action]
    result = action_func(vars(args))
    print(json.dumps(result, indent=4))
