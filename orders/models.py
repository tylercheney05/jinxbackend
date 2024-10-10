from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Sum

from cups.models import Cup


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    collected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        help_text="The user who collected the order payment",
        related_name="orders_collected",
    )
    is_paid = models.BooleanField(default=False)
    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    is_complete = models.BooleanField(default=False)
    order_name = models.ForeignKey("OrderName", on_delete=models.PROTECT, null=True)
    is_in_progress = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.date}"


class OrderPaidAmount(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="paid_amount"
    )
    paid_amount = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"OrderPaidAmount {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    cup = models.ForeignKey("cups.Cup", on_delete=models.CASCADE)
    low_sugar = models.BooleanField(default=False)
    note = models.TextField(blank=True, default="")
    is_prepared = models.BooleanField(default=False)

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


class MenuItemCustomOrder(models.Model):
    """The same thing as CustomOrder except this associates it to a menu item"""

    menu_item = models.ForeignKey(
        "menuitems.MenuItem", on_delete=models.CASCADE, related_name="custom_orders"
    )
    soda = models.ForeignKey(
        "sodas.Soda", on_delete=models.CASCADE, related_name="menu_item_custom_orders"
    )

    def __str__(self):
        return f"MenuItemCustomOrder {self.id}"

    @property
    def cup_prices(self):
        cup_prices = list()
        for cup in Cup.objects.all():
            cup_price = cup.price
            price = self.menu_item_custom_order_custom_order_flavors.annotate(
                quantity_price=(
                    F("custom_order_flavor__quantity")
                    * F("custom_order_flavor__flavor__flavor_group__price")
                )
            ).aggregate(total_sum_product=Sum("quantity_price"))
            cup_prices.append(
                {
                    "id": cup.id,
                    "size": cup.size,
                    "size__display": cup.get_size_display(),
                    "price": cup_price + price.get("total_sum_product", 0),
                }
            )
        return cup_prices


class OrderItemMenuItemCustomOrder(models.Model):
    order_item = models.OneToOneField(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="menu_item_custom_order",
    )
    menu_item_custom_order = models.ForeignKey(
        MenuItemCustomOrder,
        on_delete=models.CASCADE,
        related_name="menu_item_custom_order_order_items",
    )

    def __str__(self):
        return f"OrderItemMenuItemCustomOrder {self.id}"


class OrderItemCustomOrder(models.Model):
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


class CustomOrder(models.Model):
    soda = models.ForeignKey(
        "sodas.Soda", on_delete=models.CASCADE, related_name="custom_orders"
    )

    def __str__(self):
        return f"Custom Order {self.id}"

    @property
    def cup_prices(self):
        cup_prices = list()
        for cup in Cup.objects.all():
            cup_price = cup.price
            price = self.custom_order_custom_order_flavors.annotate(
                quantity_price=(
                    F("custom_order_flavor__quantity")
                    * F("custom_order_flavor__flavor__flavor_group__price")
                )
            ).aggregate(total_sum_product=Sum("quantity_price"))
            cup_prices.append(
                {
                    "id": cup.id,
                    "size": cup.size,
                    "size__display": cup.get_size_display(),
                    "price": cup_price + price.get("total_sum_product", 0),
                }
            )
        return cup_prices


class CustomOrderFlavor(models.Model):
    flavor = models.ForeignKey(
        "flavors.Flavor", on_delete=models.CASCADE, related_name="custom_order_flavors"
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Custom Order {self.object_id} {self.flavor.name} {self.quantity}"


class CustomOrderFlavorCustomOrder(models.Model):
    custom_order_flavor = models.OneToOneField(
        CustomOrderFlavor,
        on_delete=models.CASCADE,
        related_name="custom_order_flavor_custom_order",
    )
    custom_order = models.ForeignKey(
        CustomOrder,
        on_delete=models.CASCADE,
        related_name="custom_order_custom_order_flavors",
    )

    def __str__(self):
        return f"CustomOrderFlavorCustomOrder {self.id}"


class CustomOrderFlavorMenuItemCustomOrder(models.Model):
    custom_order_flavor = models.OneToOneField(
        CustomOrderFlavor,
        on_delete=models.CASCADE,
        related_name="custom_order_flavor_menu_item_custom_order",
    )
    menu_item_custom_order = models.ForeignKey(
        MenuItemCustomOrder,
        on_delete=models.CASCADE,
        related_name="menu_item_custom_order_custom_order_flavors",
    )

    def __str__(self):
        return f"CustomOrderFlavorMenuItemCustomOrder {self.id}"


class OrderName(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class DiscountPercentOff(models.Model):
    discount = models.OneToOneField(Discount, on_delete=models.CASCADE)
    percent_off = models.DecimalField(
        decimal_places=2,
        max_digits=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    def __str__(self):
        return f"{self.discount.name} - {self.percent_off * 100}% off"


class DiscountPrice(models.Model):
    discount = models.OneToOneField(Discount, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.discount.name} - ${self.price}"


class DiscountCupSize(models.Model):
    discount = models.OneToOneField(Discount, on_delete=models.CASCADE)
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.discount.name} - {self.cup.size}"


class OrderDiscount(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} - {self.discount.name}"
