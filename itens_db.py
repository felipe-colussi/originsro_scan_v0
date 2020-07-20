import crud
import requests


'''

lista_itens = dict()

with open('itemjson.txt', 'r') as idb:
    arquivo = json.load(idb)
    for dic in arquivo['items']:
        lista_itens[str(dic['item_id']).lower()] = Item(dic['item_id'], dic['unique_name'], dic['name'], dic['type'],
                                                            dic['npc_price'])


'''


if __name__ == '__main__':
    idb = requests.get("https://api.originsro.org/api/v1/items/list?api_key=*")
    arquivo = idb.json()
    conn = crud.conectar()
    lista_id = crud.return_item_id(conn)
    for dic in arquivo['items']:
        if not dic["item_id"]:
            npc_sell_price = ((dic['npc_price'] // 2) * 124 // 100)
            crud.insert_item_db(conn, dic["item_id"], dic["unique_name"], dic["name"].replace("'", "''"), dic["type"],
                                dic["npc_price"], npc_sell_price, dic.get('slots', 0))
    crud.desconectar(conn)


