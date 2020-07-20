import item_class
from crud import return_avg, conectar, desconectar, return_b_max, return_v_min, insert_historical_buy_price, \
    insert_historical_sell_price
from datetime import timedelta
from math import inf

# Ver para mudar o CRUD -> Pegar mais de um item numa tacada.

def daily_update(today):
    """
    :param today: date_time after dateutil.parse.isoparse.date()
    :return:
    """
#    day_price()
#    week_price()
#    month_price()
#    ...
#    ...
#    ...

    conn = conectar()
    for key, value in return_avg(conn, 'sell_list', str(today - timedelta(days=1))).items():
        item_class.items[key].set_v_d_avg(value)

    for key, value in return_avg(conn, 'sell_list', str(today - timedelta(days=7))).items():
        item_class.items[key].set_v_w_avg(value)

    for key, value in return_avg(conn, 'sell_list', str(today - timedelta(days=30))).items():
        item_class.items[key].set_v_m_avg(value)

    for key, value in return_avg(conn, 'sell_list', "2020-06-01").items():
        item_class.items[key].set_v_h_avg(value)

    for key, value in return_avg(conn, 'buy_list', str(today - timedelta(days=1))).items():
        item_class.items[key].set_b_d_avg(value)

    for key, value in return_avg(conn, 'buy_list', str(today - timedelta(days=7))).items():
        item_class.items[key].set_b_w_avg(value)

    for key, value in return_avg(conn, 'buy_list', str(today - timedelta(days=30))).items():
        item_class.items[key].set_b_m_avg(value)

    for key, value in return_avg(conn, 'buy_list', "2020-06-01").items():
        item_class.items[key].set_b_h_avg(value)

    for key, value in return_b_max(conn, str(today - timedelta(days=7))).items():
        item_class.items[key].set_b_w_high(value)

    for key, value in return_b_max(conn, str(today - timedelta(days=30))).items():
        item_class.items[key].set_b_m_high(value)

    for key, value in return_v_min(conn, str(today - timedelta(days=7))).items():
        item_class.items[key].set_v_w_low(value)

    for key, value in return_v_min(conn, str(today - timedelta(days=30))).items():
        item_class.items[key].set_v_m_low(value)

    # Adicionando os itens ao database:
    for item in item_class.items.values():
        if item.v_d_low == inf:
            item.v_d_low = 0

        insert_historical_sell_price(conn, item.id, str(today),
                                     item.v_d_low, item.v_d_low_quantity, item.v_d_avg, item.v_d_avg_x,
                                     item.v_w_low, item.v_w_avg, item.v_w_avg_x,
                                     item.v_m_low, item.v_m_avg, item.v_m_avg_x,
                                     item.v_h_avg, item.v_h_avg_x)
        insert_historical_buy_price(conn, item.id, str(today),
                                    item.b_d_high, item.b_d_high_quantity, item.b_d_avg, item.b_d_avg_x,
                                    item.b_w_high, item.b_w_avg, item.b_w_avg_x,
                                    item.b_m_high, item.b_m_avg, item.b_m_avg_x,
                                    item.b_h_avg, item.b_h_avg_x)

        item.reset_day()
    desconectar(conn)
    print(str(today))
    print('update_calss - Dayli Update OK')


conn = conectar()
print(return_avg(conn, 'sell_list', "2020-06-01"))
desconectar(conn)