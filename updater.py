import json
import os

from requests import get

import utils
from updaters.essentials import Essentials
from updaters.shopguiplus import ShopGuiPlus

items_per_page = 45
raw_url = 'https://raw.githubusercontent.com/Biggsen/vz-price-guide/main/src/_data/{}.json'
shops = ['drops', 'earth', 'food', 'ores', 'sand', 'stone', 'utility', 'wood']

# See https://github.com/Biggsen/vz-price-guide/blob/df71cb75d684a575dab282ea8bf5382a23c3b539/src/index.njk#L3-L4
price_multiplier = 1
sell_margin = 0.30

shop_gui_plus = ShopGuiPlus(items_per_page, price_multiplier, sell_margin)
essentials = Essentials(items_per_page, price_multiplier, sell_margin)


def get_content(shop_name):
    """
    Do a GET request for the given shop and return the content

    :param shop_name: the file name
    :type shop_name: str
    :return content as json or None
    """

    response = get(raw_url.format(shop_name))

    if not response.ok:
        utils.log(
            '',
            shop_name,
            f"Request for {response.url} failed with status code {response.status_code}:\n {response.reason}"
        )
        return None

    return json.loads(response.content)


def run():
    """The entry point of this script"""

    if not os.path.exists("./shops"):
        os.mkdir("./shops")

    for shop in shops:
        utils.log('', shop, "Updating...")
        content = get_content(shop)

        if content is None:
            utils.log('', shop, 'Could not get the content, skippint this shop!\n')
            continue

        shop_gui_plus.update(shop, content)
        essentials.update(shop, content)

    essentials.save()
