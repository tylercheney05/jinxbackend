from cups.models import Cup
from flavors.models import Flavor
from menuitems.models import MenuItem


def get_price(cup_id, menu_item_id, custom_order__soda_id, custom_order_flavor_ids):
    if custom_order__soda_id:
        cup = Cup.objects.get(id=cup_id)
        price = cup.price
        for flavor_id in custom_order_flavor_ids:
            flavor = Flavor.objects.get(id=flavor_id)
            price += flavor.flavor_group.price * cup.conversion_factor
        return price
    if menu_item_id:
        menu_item = MenuItem.objects.get(id=menu_item_id)
        cup_prices = menu_item.cup_prices
        for cup_price in cup_prices:
            if cup_price["id"] == cup_id:
                return cup_price["price"]
    return 0
