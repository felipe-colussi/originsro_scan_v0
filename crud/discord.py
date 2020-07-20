from .connection import db_updater, db_reader


@db_updater
def insert_discord_request(item_id: int, price: int, discord_user: int, cursor: object) -> None:
    """
    Insert a item in the discord database
    :param item_id:  item_id
    :param price: target price
    :param discord_user:  discord ID (ctx.message.author.id)
    :param cursor: object from decorator
    :return:
    """
    cursor.execute(f"""INSERT INTO discord_request (item_id, price, discord_user) VALUES ({item_id}, {price},
                   {discord_user});""")
    return None


@db_reader
def return_discord_request(discord_id: int, cursor: object) -> list:
    """ Return a list of the wishlist
    :param cursor got from decorator:
    :param discord_id: discord ID (ctx.message.author.id)
    :return: item_id, nome, preço
    """
    cursor.execute(f"""SELECT d.item_id, i.name, d.price FROM discord_request as d, item_db as i 
    WHERE d.item_id = i.id and d.discord_user = {discord_id}
    ORDER BY d.item_id""")
    lista = cursor.fetchall()
    return lista


@db_updater
def delete_discord_list(discord_id: int, cursor: object) -> None:
    """
    Clear the discord_id wishlist
    :param cursor: got from decorator
    :param discord_id: discord ID (ctx.message.author.id)
    :return: None
    """
    cursor.execute(f"""DELETE FROM discord_request WHERE discord_user = {discord_id}""")
    return


@db_updater
def delete_discord_item(discord_id, item_id, cursor):
    """
    Delet a item from discord_request
    :param cursor: got from the decorator
    :param item_id: item_id to be deleted
    :param discord_id: discord ID (ctx.message.author.id)
    :return: None
    """
    cursor.execute(f"""DELETE FROM discord_request WHERE discord_user = {discord_id} and item_id = {item_id}""")
    return
