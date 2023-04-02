import requests
from requests.auth import HTTPBasicAuth

def get_request(url, node):
    if node.auth_type == "TOKEN":
        auth_header = {'Authorization':node.token}
        data = requests.get(url, headers=auth_header)
        return data.json()

    elif node.auth_type == "BASIC":
        data = requests.get(url, auth=HTTPBasicAuth(node.username, node.password))
        return data.json()

def post_request(url, node, json):
    if node.auth_type == "TOKEN":
        auth_header = {'Authorization':node.token}
        data = requests.post(url, json=json, headers=auth_header)
        return None

    elif node.auth_type == "BASIC":
        data = requests.post(url, json=json, auth=HTTPBasicAuth(node.username, node.password))
        return None