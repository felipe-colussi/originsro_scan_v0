from controler.update import intra_day_update, check_vending_store_wishlists


def checker():
    x = intra_day_update()
    check_vending_store_wishlists(x)
