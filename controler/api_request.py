import requests


def market_api_request() -> dict:
    """Request the market API from origins-ro server"""
    idb = requests.get("https://api.originsro.org/api/v1/market/list?api_key=*")
    return idb.json()


def item_api_request() -> dict:
    """Request the item_API, Use this just whenever the server have a major update"""
    idb = requests.get("https://api.originsro.org/api/v1/items/list?api_key=*")
    return idb.json()

