from controler.item_class import create_item_dict, update_item_dict, Item
from crud.connection import db_updater
from crud.market_data import insert_market_data, return_better_item, date, daily_reset, insert_api_datetime
from crud.daily_prices import insert_daily_prices, insert_daily_date
from typing import Dict
from crud.discord import delete_discord_item, return_discord_list
from controler.market_data import str_to_date
from views.discord_bot import reply


def dayily_update(cursor: object = None) -> None:
    """Conect to the database, get the better itens of the day and reset the database"""
    date_id = insert_daily_date(date())
    for item in return_better_item():
        insert_daily_prices(item[0], item[1], item[2], item[3], item[4], date_id, cursor)
    daily_reset()
    return None


@db_updater
def intra_day_update(cursor: object = None) -> Dict[int, object]:
    """Get a Dict{item_id: Item_object}, api_datatime_id and update the database with those values
    cursor obtained throug decorator db_updater
    Ver para melhorar a conversão de datetime para str e de str para date
    """
    item_dict = create_item_dict()
    api_datetime = update_item_dict(item_dict) # Verificar se é melhor ficar aqui ou receber como parâmetro.
    if not date() == str_to_date(api_datetime):
        dayily_update(cursor)
    api_datetime_id = insert_api_datetime(api_datetime)
    for item_id, item_object in item_dict.items():
        if item_object.storage:
            insert_market_data(api_datetime_id, item_id, item_object.buying_price, item_object.buying_amount,
                               item_object.vending_price, item_object.vending_amount, cursor)
    return item_dict


def check_vending_store_wishlists(item_dict: Dict[int, object]) -> None:
    """
    Recieve an Updatedet item_dict to check with the discord_wishlists if market price matches wishlist price.
    return_discord_list() will ruturn a List of tuples. ([0]-item_id, [1] - Price, [2] -Discord User )
    :param item_dict:  Updated item_dict returned from intra_day_update.
    :return:
    """
    for wishlist in return_discord_list():
        if item_dict[wishlist[0]].vending_price <= wishlist[1]:
            item = item_dict[wishlist[0]]
            """ 
            print(
                f"User: {wishlist[2]}\n"
                f"Item {item_dict[wishlist[0]].name} is selling for {item_dict[wishlist[0]].vending_price}!\n"
                f" The following merchant(s) are selling the itens for this price:\n"
                f"{item_dict[wishlist[0]].vending_store_str()}")"""
            reply(item.id, item.name, item.vending_price, item.vending_store_str()) # IF calld from discord bot
            delete_discord_item(wishlist[2], wishlist[0])
    return None



