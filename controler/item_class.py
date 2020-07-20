from math import inf
from crud.item_db import item_db_list
from typing import Dict
from controler.market_data import stores, str_timestamp
from controler.api_request import market_api_request

class Item:
    def __init__(self, item_id: int, name: str, item_type: str) -> None:
        self.id = item_id
        self.name = name
        self.i_type = item_type
        self.vending_price = inf
        self.vending_amount = 0
        self.vending_store = []
        self.buying_price = 0
        self.buying_amount = 0
        self.buying_store = []
        self.storage = False

    def vending(self, price: int, amount: int, store_owner: str, location: str) -> None:
        """Update Vending Atributes"""
        if price < self.vending_price:
            self.vending_price = price
            self.vending_amount = amount
            self.vending_store = [(store_owner, location), ]
            self.storage = True
        elif price == self.vending_price and (store_owner, location) not in self.vending_store:
            self.vending_amount += amount
            self.vending_store.append((store_owner, location))

    def buying(self, price: int, amount: int, store_owner: str, location: str) -> None:
        """Update Buying atributes"""
        if price > self.buying_price:
            self.buying_price = price
            self.buying_amount = amount
            self.buying_store = [(store_owner, location), ]
            self.storage = True
        elif price == self.buying_price and (store_owner, location) not in self.buying_store:
            self.buying_amount += amount
            self.buying_store.append((store_owner, location))

    def reset(self) -> None:
        """Reset, should be called every new cycle."""
        self.vending_price = 0
        self.vending_amount = 0
        self.vending_store = []
        self.buying_price = 0
        self.buying_amount = 0
        self.buying_store = []
        self.storage = False


# VER SE É VALIDO FAZER UM PICKLE PARA ARMAZENAR OS VALORES ZERADOS.
def create_item_dict() -> Dict[int, object]:
    """Creat a dict {id: Object}"""
    return {item_id: Item(item_id, name, item_type) for item_id, name, item_type in item_db_list()}


def update_item_dict(item_dict: dict) -> str:
    """Update the item_dict for each item in the market."""
    file = market_api_request()
    stores(file, item_dict)
    return str_timestamp(file)