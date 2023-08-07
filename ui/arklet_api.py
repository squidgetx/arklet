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
    'csv'
]

UPDATE_FIELDS = MINT_FIELDS + ['ark']

GET = 'get'
POST = 'post'
PUT = 'put'

class ArkAPIError(Exception):
    pass

def query_generic(method, url, **kwargs):
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


def query(data):
    assert data['ark'], "Must include --ark argument"
    return query_generic(GET, data['ark'] + '?json')

def authorized(method, url, data):
    auth = DEFAULT_KEY
    return query_generic(method, url, json=data, headers={'Authorization': auth})

def update(data: dict):
    assert data['ark'], "Must include --ark argument"
    return authorized(PUT, '/update', data)

def mint(data: dict):
    assert data['naan'], "Must include --naan argument for mint operation"
    assert data['shoulder'], "Must include --shoulder argument for mint operation"
    return authorized(POST, '/mint', data)

def csv2json(csvfile):
    reader = csv.DictReader(open(csvfile, 'rt'))
    return [r for r in reader]

def query_csv(data: dict):
    assert data['csv'], "Must include --csv argument for bulk operations"
    assert len(data.keys()) == 1, "Only --csv argument is required for bulk query"
    jsondata = csv2json(data['csv'])
    assert 'ark' in jsondata[0], "CSV for bulk ark querying must include 'ark' column"
    return query_generic(POST, 'bulk_query', json=jsondata)

def update_csv(data: dict):
    assert data['csv'], "Must include --csv argument for bulk operations"
    assert len(data.keys()) == 1, "Only --csv argument is required for bulk update"
    update_data = csv2json(data['csv'])
    for record in update_data:
        assert 'ark' in record, "CSV for bulk ark querying must include 'ark' column"
    return authorized(POST, 'bulk_update', {
        'data': update_data,
    })

def mint_csv(data: dict):
    assert data['csv'], "Must include --csv argument for bulk operations"
    assert data['naan'], "Must include --naan argument for bulk operations"
    assert len(data.keys()) == 2, "Only --csv argument is required for bulk update"
    mint_data = csv2json(data['csv'])
    return authorized(POST, 'bulk_mint', {
        'data': mint_data,
        'naan': data['naan']
    })

ENDPOINTS = [
    query,
    update,
    mint,
    query_csv,
    update_csv,
    mint_csv, 
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
