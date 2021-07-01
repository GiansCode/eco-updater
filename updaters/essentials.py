import os
import utils
import yaml


class Essentials:

    def __init__(self, items_per_page, price_multiplier, sell_margin):
        self.name = 'ess'
        self.items_per_page = items_per_page
        self.price_multiplier = price_multiplier
        self.sell_margin = sell_margin
        self.items = {}

    def save(self):
        with open(f'{os.path.dirname(__file__)}/../worth.yml', 'w') as file:
            yaml.dump({'worth': self.items}, file, sort_keys=False)
            file.close()

    def update(self, shop_name, content):
        """
        Update a shop with the new data from github

        :param shop_name: the shop name
        :type shop_name: str
        :param content: the data
        :type content: dict
        """

        for item in content:
            material = item['material_id']
            price = utils.get_price(shop_name, item)

            # price is invalid / 0
            if price == 0:
                continue

            # See https://github.com/Biggsen/vz-price-guide/blob/df71cb75d684a575dab282ea8bf5382a23c3b539/src/_includes/tbody.njk#L3
            sell_price = price * self.sell_margin * self.price_multiplier
            self.items[material] = utils.round_sell_price(sell_price)

        utils.log(self.name, shop_name, "Updated!\n")
