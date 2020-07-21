from dateutil.parser import isoparse as iso
from datetime import datetime

def timestamp(api_request: dict) -> object:
    """Return a Datetime Object"""
    return iso(api_request['generation_timestamp'])


def str_timestamp(api_request: dict) -> str:
    """Return a Data-teime string"""
    return timestamp(api_request).strftime("%Y-%m-%d-%H-%M")


def str_to_date(data_time_str: str) -> object:
    """
    get a string from str_timestamp and convert it to a data
    :param data_time_str:
    :return: datatime
    """
    return datetime.strptime('2020-06-06-08-30', '%Y-%m-%d-%H-%M').date()


def str_data(api_request: dict) -> str:
    """Return a Data string"""
    return timestamp(api_request).strftime("%Y-%m-%d")


def buying_item(item: dict, owner: str, location: str, item_dict: dict) -> None:
    """update buying items
        Item list is a dictionary {id: item_object} obtainable throug controler.item_class.creat_item_dict()"""
    item_dict[item["item_id"]].buying(item["price"], item["amount"], owner, location)


def vending_item(item: dict, owner: str, location: str, item_dict: dict) -> None:
    """Update vending items
       Item list is a dictionary {id: item_object} obtainable throug controler.item_class.creat_item_dict()
    """
    item_dict[item["item_id"]].vending(item["price"], item["amount"], owner, location)


def stores(api_request: dict, item_dict: dict) -> None:
    """Iterate over all stores from API_Request
    Item list is a dictionary {id: item_object} obtainable throug controler.item_class.creat_item_dict()"""
    for store in api_request["shops"]:
        owner = store["owner"].replace("'", "''")
        location = store["location"]['map']
        if store["type"] == "V":
            for item_data in store["items"]:
                vending_item(item_data, owner, location, item_dict)
        else:
            for item_data in store["items"]:
                buying_item(item_data, owner, location, item_dict)

