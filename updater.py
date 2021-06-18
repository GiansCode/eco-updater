import json
import yaml
import os

from requests import get

items_per_page = 45
raw_url = 'https://raw.githubusercontent.com/Biggsen/vz-price-guide/main/src/_data/{}.json'
shops = ['drops', 'earth', 'food', 'ores', 'sand', 'stone', 'utility', 'wood']


def get_content(shop_name):
    """
    Do a GET request for the given shop and return the content

    :param shop_name: the file name
    :type shop_name: str
    :return content as json or None
    """

    response = get(raw_url.format(shop_name))

    if not response.ok:
        log(shop_name,
            f"Request for {response.url} failed with status code {response.status_code}:\n {response.reason}")
        return None

    return json.loads(response.content)


def update(shop_name):
    """
    Update a shop with the new data from github

    :param shop_name: the shop name
    :type shop_name: str
    """
    content = get_content(shop_name)

    # the get request failed
    if content is None:
        return

    slot = 0
    page = 1
    items = {}

    for item in content:
        # the maximum amount of items for one page has been reached
        # setting the slot back to 0 and incrementing the page number by 1
        if slot > items_per_page - 1:
            slot = 0
            page += 1

        material = item['material_id']
        price_string = item['price']
        price = int(price_string) if price_string.isdigit() else 0

        # price is invalid / 0
        if price == 0:
            log(shop_name, f"Skipping {material} because price {price_string} is not a number")
            continue

        stack = int(item['stack'])

        items[f"p{page}-{slot}"] = {
            'type': 'item',
            'slot': slot,
            'page': page,
            'item': {
                'material': material
            },
            'buyPrice': price
        }

        slot += 1

    save(shop_name, items)


def save(shop_name, items):
    """
    Save the items to file on **/shops/<shop_name>.yml**

    :param shop_name: the file name
    :type shop_name: str
    :param items: items to save
    :type items: dict
    """

    with open(f'./shops/{shop_name}.yml', 'w') as file:
        shop = {
            shop_name: {
                'items': items
            }
        }

        yaml.dump(shop, file, sort_keys=False)
        file.close()

    log(shop_name, "Updated!\n")


def log(shop_name, message):
    """
    Print a message to console

    :param shop_name: the shop name, used for the message prefix
    :type shop_name: str
    :param message: the message to be printed
    :type message: str
    """
    print(f"[{shop_name}] {message}")


def run():
    """The entry point of this script"""

    if not os.path.exists("./shops"):
        os.mkdir("./shops")

    for shop in shops:
        log(shop, "Updating...")
        update(shop)
