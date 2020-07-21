from crud.connection import *


def insert_daily_date(date: str, cursor: object) -> int:
    """
    Insert a date in daily_date and return the created ID
    :param date: Day witch the data references to
    :param cursor: decorator @db_updater
    :return: ID
    """
    cursor.execute(f"""INSERT INTO daily_date (date) VALUES ('{date}') RETURNING id;""")
    x = cursor.fetchone()[0]
    return x


@db_updater
def insert_daily_prices(item_id: int, buying_price: int, buying_ammount: int, vending_price: int,
                        vending_amount: int, date_id: int, cursor: object= None) -> None:
    """
    Insert the daily pirces into the daily_prices. After this insert tha tables market_data and api_datetime shold
    be reseted.
    The functin that call this function should call the decorator @db_updater so we avoid tons of db connections.
    The function that calls it should be decorated with @db_updater to avoid extra conections.
    """
    cursor.execute(f"""INSERT INTO daily_prices (item_id, buying_price, buying_amount, vending_price, vending_amount, 
    scan_date_id) VALUES ({item_id}, {buying_price}, {buying_ammount}, {vending_price}, {vending_amount}, {date_id})""")
    return None



