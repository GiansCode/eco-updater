import os
import utils
import yaml


class ShopGuiPlus:

    def __init__(self, items_per_page, price_multiplier, sell_margin):
        self.name = 'sg+'
        self.items_per_page = items_per_page
        self.price_multiplier = price_multiplier
        self.sell_margin = sell_margin

    def __save(self, shop_name, items):
        with open(f'{os.path.dirname(__file__)}/../shops/{shop_name}.yml', 'w') as file:
            shop = {
                shop_name: {
                    'items': items
                }
            }

            yaml.dump(shop, file, sort_keys=False)
            file.close()

        utils.log(self.name, shop_name, "Updated!\n")

    def update(self, shop_name, content):
        """
        Update a shop with the new data from github

        :param shop_name: the shop name
        :type shop_name: str
        :param content: the data
        :type content: dict
        """
        slot = 0
        page = 1
        items = {}

        for item in content:
            if slot > self.items_per_page - 1:
                slot = 0
                page += 1

            material = item['material_id']
            price = utils.get_price(shop_name, item)

            # price is invalid / 0
            if price == 0:
                continue

            # See https://github.com/Biggsen/vz-price-guide/blob/df71cb75d684a575dab282ea8bf5382a23c3b539/src/_includes/tbody.njk#L2-L3
            buy_price = price * self.price_multiplier
            sell_price = price * self.sell_margin * self.price_multiplier

            items[material] = {
                'type': 'item',
                'slot': slot,
                'page': page,
                'item': {
                    'material': material.upper(),
                    'amount': 1
                },
                'buyPrice': round(buy_price),
                # See https://github.com/Biggsen/vz-price-guide/blob/df71cb75d684a575dab282ea8bf5382a23c3b539/src/_includes/tbody.njk#L10-L14
                'sellPrice': utils.round_sell_price(sell_price)
            }

            slot += 1

        self.__save(shop_name, items)
