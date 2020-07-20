import crud
import requests
from dateutil.parser import isoparse as iso
import item_class


def txt(string):
    return string.replace("'", "''")


def update_market():
    """Atualiza o database"""
    idb = requests.get("https://api.originsro.org/api/v1/market/list?api_key=pg398rhdi47l7a8ihzvkvuhndfkqi50o")
    arquivo = idb.json()
    conn = crud.conectar()
    api_request_id = crud.insert_api_request(conn, arquivo["generation_timestamp"])
    date_time = iso(arquivo["generation_timestamp"])
    for dic in arquivo['shops']:
        store = crud.insert_store(conn, txt(dic["title"]), txt(dic["owner"]),
                                  txt(dic["location"]["map"]), dic["location"]["x"], dic["location"]["y"],
                                  dic["creation_date"], dic["type"], api_request_id)
        if dic["type"] == "B":
            for item in dic["items"]:
                crud.insert_buy_list(conn, item["item_id"], item["amount"], item["price"], store)
                if item_class.items[item["item_id"]].b_d_high < item["price"]:
                    item_class.items[item["item_id"]].better_b_price(item["price"], item["amount"], store,
                                                                     dic["creation_date"])
                elif item_class.items[item["item_id"]].b_d_high == item["price"] and dic["creation_date"] \
                        not in item_class.items[item["item_id"]].b_store_date:
                    item_class.items[item["item_id"]].price_b_quantity(item["amount"], store, dic["creation_date"])
        else:
            for item in dic["items"]:
                sell_list_id = crud.insert_sell_list(conn, item["item_id"], item["amount"], item["price"], store)
                if item_class.items[item["item_id"]].v_d_low > item["price"]:
                    item_class.items[item["item_id"]].better_v_price(item["price"], item["amount"], store,
                                                                     dic["creation_date"])
                elif item_class.items[item["item_id"]].v_d_low == item["price"] and dic["creation_date"] not in \
                        item_class.items[item["item_id"]].v_store_date:
                    item_class.items[item["item_id"]].price_v_quantity(item["amount"], store, dic["creation_date"])

                if "refine" in item:
                    crud.insert_refine_sell_itens(conn, sell_list_id, item["refine"])
                if "creator" in item:
                    crud.insert_creator_sell_itens(conn, sell_list_id, item["creator"])
                if "cards" in item:
                    for card in item["cards"]:
                        crud.insert_card_sell_itens(conn, sell_list_id, card)
                if "star_crumbs" in item or "element" in item:
                    try:
                        star_crumbs = item["star_crumbs"]
                    except KeyError:
                        star_crumbs = 0
                    try:
                        stone = item["element"]
                    except KeyError:
                        stone = "Neutral"
                    crud.insert_forge_sell_itens(conn, sell_list_id, star_crumbs, stone)
    crud.desconectar(conn)
    return date_time


"""
def update_market():
    Atualiza o database
    pedir_api() <- VARIAVEL
    edir_timestamp()
    separar_shop()  <- Pedir_item_venda()  <- verificar_melhor_valor()
                                            <- Adicionar_database()
"""