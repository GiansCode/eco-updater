def get_price(shop_name, item):
    price_string = item['price']
    price = int(price_string) if price_string.isdigit() else 0

    # price is invalid / 0
    if price == 0:
        log('', shop_name, f"Skipping {item['material_id']} because price {price_string} is not a number")

    return price


def round_sell_price(price):
    return round(price, 2) if price < 0.8 else round(price)


def log(updater='', shop=None, message=None):
    """
    Print a message to console

    :param updater: the updater implementation name, eg 'essentials'
    :type updater: str
    :param shop: the shop name, used for the message prefix
    :type shop: str
    :param message: the message to be printed
    :type message: str
    """
    if updater == '':
        print(f"[{shop}] {message}")
    else:
        print(f"[{shop}] ({updater}) {message}")