import requests


def get_node(pubkey):
    req = f'https://ln.bigsun.xyz/api/nodes?pubkey=eq.{pubkey}'
    return requests.get(req).json()


def get_channel(channel_id):
    req = f'https://ln.bigsun.xyz/api/channels?short_channel_id=eq.{channel_id}'
    return requests.get(req).json()


def get_policy(channel_id):
    req = f'https://ln.bigsun.xyz/api/policies?short_channel_id=eq.{channel_id}'
    return requests.get(req).json()
