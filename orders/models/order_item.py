from django.db import models


class OrderItem(models.Model):
    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="items"
    )
    cup = models.ForeignKey("cups.Cup", on_delete=models.CASCADE)
    low_sugar = models.BooleanField(default=False)
    note = models.TextField(blank=True, default="")

    def __str__(self):
        return f"OrderItem {self.id} - {self.order}"


class OrderItemMenuItem(models.Model):
    order_item = models.OneToOneField(
        OrderItem, on_delete=models.CASCADE, related_name="menu_item"
    )
    menu_item = models.ForeignKey(
        "menuitems.MenuItem",
        on_delete=models.CASCADE,
        related_name="menu_item_order_items",
    )

    def __str__(self):
        return f"OrderItemMenuItem {self.id}"

    @property
    def price(self):
        cup_prices = self.menu_item.cup_prices
        for item in cup_prices:
            if item.get("size") == self.order_item.cup.size:
                return item.get("price")
        return None


class OrderItemMenuItemCustomOrder(models.Model):
    """Order items related to a MenuItemCustomOrder"""

    order_item = models.OneToOneField(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="menu_item_custom_order",
    )
    menu_item_custom_order = models.ForeignKey(
        "orders.MenuItemCustomOrder",
        on_delete=models.CASCADE,
        related_name="menu_item_custom_order_order_items",
    )

    def __str__(self):
        return f"OrderItemMenuItemCustomOrder {self.id}"

    @property
    def price(self):
        cup_prices = self.menu_item_custom_order.cup_prices
        for item in cup_prices:
            if item.get("size") == self.order_item.cup.size:
                return item.get("price")
        return None


class OrderItemCustomOrder(models.Model):
    """Order items related to a CustomOrder"""

    order_item = models.OneToOneField(
        OrderItem, on_delete=models.CASCADE, related_name="custom_order"
    )
    custom_order = models.ForeignKey(
        "orders.CustomOrder",
        on_delete=models.CASCADE,
        related_name="custom_order_order_items",
    )

    def __str__(self):
        return f"OrderItemCustomOrder {self.id}"

    @property
    def price(self):
        cup_prices = self.custom_order.cup_prices
        for item in cup_prices:
            if item.get("size") == self.order_item.cup.size:
                return item.get("price")
        return None
