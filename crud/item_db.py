from crud.connection import db_updater, db_reader
from controler.api_request import item_api_request
from typing import List, Tuple


def insert_item_db(item_id: int, name: str, i_type: str, npc_price: int, cursor: object= None) -> None:
    """
    Insere itens na tabela Itens
    :param cursor:
    :param item_id: INT
    :param name:  STR
    :param i_type:  STR
    :param npc_price: STR in [IT_HEALING, IT_UNKNOWN, IT_USABLE, IT_ETC, IT_WEAPON, IT_ARMOR, IT_CARD, IT_PETEGG,
     IT_PETARMOR, IT_AMMO, IT_DELAYCONSUME IT_CASH]
    :return: None
    """
    cursor.execute(f"""INSERT INTO item_db (id, name, type, npc_price)
                  VALUES ({item_id}, '{name}', '{i_type}', {npc_price});""")


@db_updater
def item_db_create(cursor: object=None) -> None:
    """create the item_db"""
    id_list = item_db_id_list()
    for dic in item_api_request()['items']:
        if dic['item_id'] in id_list:
            pass
        else:
            npc_sell_price = ((dic['npc_price'] // 2) * 124 // 100)
            insert_item_db(dic["item_id"], dic["name"].replace("'", "''"), dic["type"], npc_sell_price, cursor=cursor)




@db_reader
def item_db_list(cursor: object=None) -> List[Tuple[int, str, str]]:
    cursor.execute("SELECT id, name, type FROM item_db;")
    lista = cursor.fetchall()
    return lista


@db_reader
def item_db_id_list(cursor: object=None) -> List[int]:
    cursor.execute("SELECT id FROM item_db;")
    lista = [x[0] for x in cursor.fetchall()]
    return lista

