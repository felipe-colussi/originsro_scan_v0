from crud.connection import db_updater, db_reader
from math import inf
from typing import List, Tuple
import datetime

@db_updater
def insert_api_datetime(date_time: str, cursor: object) -> int:
    """
    Insert date
    :param date_time:
    :param cursor:
    :return:
    """
    cursor.execute(f"""INSERT INTO api_datetime (date_time) VALUES (TIMESTAMP '{date_time}') RETURNING id;""")
    return cursor.fetchone()[0]


def insert_market_data(api_date_time_id: int, item_id: int, buying_price: int, buying_ammount: int, vending_price: int,
                       vending_amount: int, cursor: object = None) -> None:
    """
    The function that calls this function should be decorated with @db_updater so we avoid extra database conections.
    :param api_date_time_id: id retornado de insert_api_datetime
    :param item_id: item_id
    :param buying_price: better price
    :param buying_ammount:  better price ammount
    :param vending_price:  better price
    :param vending_amount: better price ammount
    :param cursor:
    :return:
    """
    cursor.execute(f"""INSERT INTO market_data (api_datetime_id, item_db_id, buying_price, buying_amount, vending_price,
                       vending_amount) VALUES ({api_date_time_id}, {item_id},
                       {buying_price if buying_price != inf else 0}, {buying_ammount}, {vending_price},
                       {vending_amount});""")
    return None


@db_reader
def return_better_item(cursor: object) -> List[Tuple[int, int, int, int, int]]:
    """Return: [(item_id, buying_price, buying_amoun, vending_price, vending_amount)]"""
    cursor.execute("""SELECT a.item_db_id, a.max, b.max, c.min, d.max from (SELECT item_db_id, max(buying_price) FROM 
    market_data GROUP BY item_db_id) as a, (SELECT item_db_id, buying_price, max(buying_amount) FROM market_data 
    GROUP BY item_db_id, buying_price) as b, (SELECT item_db_id, min(vending_price) FROM MARKET_data GROUP BY 
    item_db_id) as c, (SELECT item_db_id, vending_price, max(vending_amount) FROM market_data GROUP BY item_db_id, 
    vending_price) as d WHERE a.item_db_id = b.item_db_id and b.item_db_id = c.item_db_id and c.item_db_id = 
    d.item_db_id and a.max = b.buying_price and c.min = d.vending_price;""")
    x = cursor.fetchall()
    return x


@db_updater
def daily_reset(cursor: object) -> None:
    cursor.execute("""DELETE FROM market_data""")
    cursor.execute("""DELETE FROM api_datetime""")


@db_reader
def date(cursor: object = None) -> str:
    cursor.execute("""SELECT date_time::DATE FROM api_datetime group by date_time""")
    x = cursor.fetchone()[0]
    return x



