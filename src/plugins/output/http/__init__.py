import requests
import json


def message():
    print(f"Output plugin loaded: http")


def output_from_main(value, **kwargs):

    url = f"{kwargs['changing_url']}{value}"
    payload = {}
    headers = {}

    response = requests.request("PUT", url, headers=headers, data=payload)
    print(f"Set the system to: {response.text}\n")


def current_value(**kwargs):
    url = kwargs['current_url']
    payload = {}
    headers = {}

    tmp = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
    print(f"System already at: {tmp}")
    # tmp = list(tmp.values())
    # return tmp[0]
    return tmp

