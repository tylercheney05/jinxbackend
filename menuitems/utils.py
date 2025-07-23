def get_flavors_price(menu_item, cup):
    if hasattr(menu_item, "price"):
        return menu_item.price.price * cup.conversion_factor
    price = menu_item.flavors.sum_price(cup=cup)
    return price.get("total_sum_product", 0)
