from market_db import update_market
from update_class import daily_update
import datetime
import schedule
import time


def update(last_update):
    global last_scan #
    print(f'Global Last Scan carregada = {last_scan}')
    today = datetime.datetime.utcnow().date()
    print(today)
    if last_update != today:
        print('Chamando daily update')
        daily_update(today)
    last_scan = update_market().date()
    print(last_scan)
    return last_scan

print('runing')
last_scan = datetime.datetime.utcnow().date()


# Cada x Minutos roda :  Programa.
schedule.every(6).minutes.do(update, last_scan)


while 1:
    schedule.run_pending()
    time.sleep(1)
