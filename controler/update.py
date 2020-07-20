from controler.item_class import create_item_dict, update_item_dict
from crud.connection import db_updater
from crud.market_data import insert_market_data, return_better_item, date, daily_reset, insert_api_datetime
from crud.daily_prices import insert_daily_prices, insert_daily_date


def dayily_update(cursor: object = None) -> None:
    """Conect to the database, get the better itens of the day and reset the database"""
    date_id = insert_daily_date(date())
    for item in return_better_item():
        insert_daily_prices(item[0], item[1], item[2], item[3], item[4], date_id, cursor)
    daily_reset()
    return None


@db_updater
def intra_day_update(cursor: object) -> None:
    """Get a Dict{item_id: Item_object}, api_datatime_id and update the database with those values
    cursor obtained throug decorator db_updater"""
    item_dict = create_item_dict()
    api_datetime = update_item_dict()

    api_datetime_id = insert_api_datetime(api_datetime)
    for item_id, item_object in item_dict.items():
        if item_object.storage:
            insert_market_data(api_datetime_id, item_id, item_object.buying_price, item_object.buying_amount,
                               item_object.vending_price, item_object.vending_amount, cursor)





