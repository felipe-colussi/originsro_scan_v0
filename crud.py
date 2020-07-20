import psycopg2

def conectar():
    """Conecta ao servidor - DATABASE """
    try:
        conn = psycopg2.connect(
            database='origins_ro_v2',
            host='localhost',
            user='origins_project',
            password='13524500'
        )
        return conn
    except psycopg2.Error as erro:
        print(f'Erro na conexão ao PostgreSQL Server: {erro}')


#TIRAR  ->  Criar em um lugar diferente
def desconectar(conn):
    """desconecta uma conexão"""
    if conn:
        conn.close()


def insert_item_db(conn, item_id, unique_name, name, i_type, npc_price, npc_sell_price, slots):
    """
    Insere itens na tabela Itens
    :param conn: arquivo de conexão, obtido através da função conectar()
    :param item_id: INT
    :param unique_name: STR
    :param name:  STR
    :param i_type:  STR
    :param npc_price: STR in [IT_HEALING, IT_UNKNOWN, IT_USABLE, IT_ETC, IT_WEAPON, IT_ARMOR, IT_CARD, IT_PETEGG,
     IT_PETARMOR, IT_AMMO, IT_DELAYCONSUME IT_CASH]
    :param npc_sell_price: INT
    :param slots: INT
    :return: None
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO item_db (id, uniq_name, name, type, npc_price, npc_sell_price, slots)
                  VALUES ({item_id}, '{unique_name}', '{name}', '{i_type}', {npc_price},
                    {npc_sell_price}, {slots});""")
    conn.commit()
    if cursor.rowcount == 1:
        print(f'Item {item_id} adicionado com sucesso')
    else:
        print(f'Erro ao adicionar o item {item_id}')


def insert_api_request(conn, date_time):
    """
    Insere datetime na tabela API_request, retorna ID  da consulta.
    :param conn: objeto de conexão, obtido através da função conectar()
    :param date_time: STR - TIMESTAMP
    :return: ID da linha criada.
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO api_request (date_time) VALUES (TIMESTAMP '{date_time}') RETURNING id;""")
    conn.commit()
    return cursor.fetchone()[0]


def insert_store(conn, shop_name, owner_name, mapa, x, y, opening_date, shop_type, api_request_id):
    """
    Adiciona uma loja a tabela stores retorna a ID da loja
    :param conn: objeto de conexão, obtido através da função conectar()
    :param shop_name: "shops" -> STR
    :param owner_name:  "owner" -> STR
    :param mapa: "location"["map"] -> STR
    :param x: "location"["x"] -> INT
    :param y:"location"["y"] -> INT
    :param opening_date: "creation_date" -> STR - TIMESTAMP
    :param shop_type: "type" -> V = Vending(Sell_list) B -> Buying(Buy_list)
    :param api_request_id: id da pesquisa obtida no insert_api_request -> INT
    :return: ID da linha criada
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO store (shop_name, owner_name, opening_date, shop_type, api_request_id, map, x, y)
                   VALUES ('{shop_name}', '{owner_name}', TIMESTAMP '{opening_date}', '{shop_type}', {api_request_id},
                   '{mapa}', {x}, {y}) RETURNING id;""")
    conn.commit()
    return cursor.fetchone()[0]


def insert_sell_list(conn, item_db_id, amount, price, store_id):
    """
    Insere item na tabela sell_list (Vending) e retorna o id da linha criada
    :param conn:  objeto de conexão, obtido através da função conectar()
    :param item_db_id: "items"[x]["item_id"] -> INT
    :param amount: "items"[x]["amount"] -> INT
    :param price: "items"[x]["price"] -> INT
    :param store_id: id da loja, obtida pelo insert_stores()
    :return: id item inserido na sell_list
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO sell_list (item_db_id, amount, price, store_id)
                   VALUES ({item_db_id}, {amount}, {price}, {store_id}) RETURNING id;""")
    conn.commit()
    return cursor.fetchone()[0]


def insert_buy_list(conn, item_db_id, amount, price, store_id):
    """
    Insere item na tabela buy_list (Buying) e retorna o id da linha criada
    :param conn:  objeto de conexão, obtido através da função conectar()
    :param item_db_id: "items"[x]["item_id"] -> INT
    :param amount: "items"[x]["amount"] -> INT
    :param price: "items"[x]["price"] -> INT
    :param store_id: id da loja, obtida pelo insert_stores()
    :return: id linha criada
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO buy_list (item_db_id, amount, price, store_id)
                   VALUES ({item_db_id}, {amount}, {price}, {store_id}) RETURNING id;""")
    conn.commit()
    return cursor.fetchone()[0]


def insert_refine_sell_itens(conn, sell_list_id, value):
    """
    Insere o refino de determinado item
    :param conn: objeto de conexão, obtido através da função conectar()
    :param sell_list_id: id da loja em que se encontra o item, retrno do insert_sell_list() -> INT
    :param value: "items"[x]["refine"] -> int in range(1,11)
    :return: None
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO refine_sell_itens (sell_list_id, value) VALUES ({sell_list_id}, {value})""")
    conn.commit()
    return None


def insert_forge_sell_itens(conn, sell_list_id, star_crumble, stone):
    """
    Insere detalhes de armas forjadas (Star_Crumble 1 = Strong, 2=Very Strong, 3 = Very Very Strong)
    :param conn: objeto de conexão, obtido através da função conectar()
    :param sell_list_id: id da loja em que se encontra o item, retrno do insert_sell_list() -> INT
    :param star_crumble: "itenm"[x]["star_crumbs" -> INT in range(0,4)
    :param stone: "items"[x]["element"] -> STR ("Fire", "Wind", "Ice", "Earth", "Neutral")
    :return: None
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO forge_sell_itens (sell_list_id, star_crumble, stone) VALUES 
                ({sell_list_id}, {star_crumble}, '{stone}')""")
    conn.commit()
    return None


def insert_creator_sell_itens(conn, sell_list_id, creator):
    """
    Insere ID do criador do item.
    :param conn: objeto de conexão, obtido através da função conectar()
    :param sell_list_id: id da loja em que se encontra o item, retrno do insert_sell_list() -> INT
    :param creator: "items"[x]["creator"] -> INT
    :return: None
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO creator_sell_itens (sell_list_id, creator) VALUES ({sell_list_id}, {creator})""")
    conn.commit()
    return None


def insert_card_sell_itens(conn, sell_list_id, card_id):
    """
    Insere uma carta e liga ela a um item, é inserida uma carta por comando.
    :param conn: objeto de conexão, obtido através da função conectar()
    :param sell_list_id: id da loja em que se encontra o item, retrno do insert_sell_list() -> INT
    :param card_id: "items"[x]["cards"][x] -> INT
    :return: None
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO card_sell_itens (sell_list_id, card_id) VALUES ({sell_list_id}, {card_id})""")
    conn.commit()
    return None


def insert_historical_sell_price(conn, item_db_id, date,
                                 day_lowest_price, day_lowest_price_quantity, day_avg_price, day_avg_x_price,
                                 week_lowest_price, week_avg_price, week_avg_x_price,
                                 month_lowest_price, month_avg_price, month_avg_x_price,
                                 historical_avg_price, historical_avg_x_price):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO historical_sell_price (item_db_id, at_day, 
                                  day_lowest_price, day_lowest_price_quantity, day_avg_price, day_avg_x_price,
                                  week_lowest_price, week_avg_price, week_avg_x_price,
                                  month_lowest_price, month_avg_price, month_avg_x_price,
                                  historical_avg_price, historical_avg_x_price) VALUES 
                                  ({item_db_id}, '{date}'::DATE, 
                                  {day_lowest_price}, {day_lowest_price_quantity}, {day_avg_price}, {day_avg_x_price},
                                  {week_lowest_price}, {week_avg_price}, {week_avg_x_price},
                                  {month_lowest_price}, {month_avg_price}, {month_avg_x_price},
                                  {historical_avg_price}, {historical_avg_x_price})""")
    conn.commit()
    return None


def insert_historical_buy_price(conn, item_db_id, date,
                                day_highest_price, day_highest_price_quantity, day_avg_price, day_avg_x_price,
                                week_highest_price, week_avg_price, week_avg_x_price,
                                month_highest_price, month_avg_price, month_avg_x_price,
                                historical_avg_price, historical_avg_x_price):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO historical_buy_price (item_db_id, at_day,
                                  day_highest_price, day_highest_price_quantity, day_avg_price, day_avg_x_price,
                                  week_highest_price, week_avg_price, week_avg_x_price,
                                  month_highest_price, month_avg_price, month_avg_x_price,
                                  historical_avg_price, historical_avg_x_price) VALUES 
                                  ({item_db_id}, '{date}'::DATE, 
                                  {day_highest_price}, {day_highest_price_quantity}, {day_avg_price}, {day_avg_x_price},
                                  {week_highest_price}, {week_avg_price}, {week_avg_x_price},
                                  {month_highest_price}, {month_avg_price}, {month_avg_x_price},
                                  {historical_avg_price}, {historical_avg_x_price})""")
    conn.commit()
    return None


def insert_discord_request(item_id, price, discord_user):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO discord_request (item_id, price, discord_user) VALUES ({item_id}, {price},
                   {discord_user});""")
    conn.commit()
    desconectar(conn)
    return None


def return_item_id(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id from item_db")
    lista = [item[0] for item in cursor.fetchall()]
    return lista


def return_item_id_type():
    """Retorna um Dicionário ID - Tipo de Item"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id,name, type, slots FROM item_db")
    lista = cursor.fetchall()
    desconectar(conn)
    return lista


def return_discord_request(discord_id):
    """

    :param discord_id: discord ID (ctx.message.author.id)
    :return: item_id, nome, preço
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT d.item_id, i.name, d.price FROM discord_request as d, item_db as i 
    WHERE d.item_id = i.id and d.discord_user = {discord_id}
    ORDER BY d.item_id""")
    lista = cursor.fetchall()
    desconectar(conn)
    return lista


def delete_discord_list(discord_id):
    """
    Clear the discord_id buy List
    :param discord_id: discord ID (ctx.message.author.id)
    :return: None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM discord_request WHERE discord_user = {discord_id}""")
    conn.commit()
    desconectar(conn)
    return


def delete_discord_item(conn, discord_id, item_id):
    """
    Delet a item from discord_request
    :param item_id: item_id to be deleted
    :param conn: conection
    :param discord_id: discord ID (ctx.message.author.id)
    :return: None
    """
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM discord_request WHERE discord_user = {discord_id} and item_id = {item_id}""")
    conn.commit()
    return


def limpar_database():
    x = input('Deseja mesmo limpar o database?? digite y para sim')
    if x == 'y':
        print('conectando...')
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""DELETE from buy_list;""")
        conn.commit()
        cursor.execute("""DELETE from card_sell_itens;""")
        conn.commit()
        cursor.execute("""DELETE from creator_sell_itens;""")
        conn.commit()
        cursor.execute("""DELETE from forge_sell_itens;""")
        conn.commit()
        cursor.execute("""DELETE from refine_sell_itens;""")
        conn.commit()
        cursor.execute("""DELETE from sell_list;""")
        conn.commit()
        cursor.execute("""DELETE from store;""")
        conn.commit()
        cursor.execute("""DELETE from historical_buy_price;""")
        conn.commit()
        cursor.execute("""DELETE from historical_sell_price;""")
        conn.commit()
        cursor.execute("""DELETE from api_request;""")
        conn.commit()
        desconectar(conn)


def return_avg(conn, table, date):
    """
    "Retorna o valor médio de um item em "X" Tempo (Item_ID, VALOR)
    :param conn: conexão
    :param table: tabela a qual será retirado os itens (buy_list ou sell_list) -> STR
    :param date: data a partir de que será realizado o filtro -> STR
    :return: dicionario {item_id: avg_price}
    """
    cursor = conn.cursor()
    cursor.execute(f"""SELECT b.item_db_id, ROUND(AVG(b.price),0) FROM {table} as b, store, api_request WHERE 
    b.store_id = store.id and store.api_request_id = api_request.id and api_request.date_time::date >= '{date}'::date 
    GROUP BY b.item_db_id
;""")
    return {item_id: int(avg_price) for item_id, avg_price in cursor.fetchall()}


def return_b_max(conn, date):
    '''
    Retorna os valores máximos de uma data até o ultimo update
    :param conn: CONN
    :param date: DATA - STR {}
    :return: DIC( ITEM_ID: VALOR))
    '''
    """ r"""
    cursor = conn.cursor()
    cursor.execute(f"""SELECT b.item_db_id, MAX(b.price) FROM buy_list as b, store, api_request WHERE b.store_id = 
    store.id and store.api_request_id = api_request.id and (api_request.date_time::date) >= '{date}'::date 
    GROUP BY item_db_id; """)
    return {item_id: int(price) for item_id, price in cursor.fetchall()}


def return_v_min(conn, date):
    """
    Obtem o valor mínimo a venda de um item a venda da data informada até a data atual.
    :param conn: conexão obtida através de conectar()
    :param date: Data -> STR
    :return: DIC (ITEM_ID, VALOR)
    """
    cursor = conn.cursor()
    cursor.execute(f"""SELECT s.item_db_id, MIN(s.price) FROM sell_list as s, store, api_request WHERE s.store_id = 
    store.id and store.api_request_id = api_request.id and (api_request.date_time::date) >= '{date}'::date GROUP BY 
    item_db_id""")
    return {item_id: int(price) for item_id, price in cursor.fetchall()}


if __name__ == '__main__':
    limpar_database()


