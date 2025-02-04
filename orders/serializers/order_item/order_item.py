from django.db import transaction
from rest_framework import serializers

from cups.serializers import CupDetailSerializer
from locations.models import Location
from menuitems.models import MenuItem, MenuItemFlavor
from orders.models import (
    CustomOrder,
    CustomOrderFlavor,
    CustomOrderFlavorCustomOrder,
    CustomOrderFlavorMenuItemCustomOrder,
    Discount,
    MenuItemCustomOrder,
    Order,
    OrderItem,
    OrderItemCustomOrder,
    OrderItemMenuItem,
    OrderItemMenuItemCustomOrder,
)
from sodas.models import Soda

from .order_item_custom_order import OrderItemCustomOrderSerializer
from .order_item_menu_item import OrderItemMenuItemSerializer
from .order_item_menu_item_custom_order import OrderItemMenuItemCustomOrderSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.IntegerField(write_only=True, required=False)
    order__collected_by = serializers.PrimaryKeyRelatedField(
        source="order.collected_by", read_only=True
    )
    price = serializers.SerializerMethodField(read_only=True)
    order__location = serializers.PrimaryKeyRelatedField(
        source="order.location", write_only=True, queryset=Location.objects.all()
    )
    custom_order__soda = serializers.PrimaryKeyRelatedField(
        write_only=True, required=False, queryset=Soda.objects.all(), allow_null=True
    )
    custom_order_flavors = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    order__id = serializers.PrimaryKeyRelatedField(source="order", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "cup",
            "low_sugar",
            "menu_item",
            "price",
            "note",
            "custom_order__soda",
            "custom_order_flavors",
            "order__id",
            "order__collected_by",
            "order__location",
        ]
        read_only_fields = ["id"]

    def get_price(self, obj):
        if self.context:
            discount_id = int(self.context["request"].query_params.get("discount", "0"))
            discount = Discount.objects.get(id=discount_id) if discount_id else None
            if hasattr(obj, "menu_item"):
                cup_prices = obj.menu_item.menu_item.cup_prices
            elif hasattr(obj, "menu_item_custom_order"):
                cup_prices = (
                    obj.menu_item_custom_order.menu_item_custom_order.cup_prices
                )
            elif hasattr(obj, "custom_order"):
                cup_prices = obj.custom_order.custom_order.cup_prices

            discount_percent_off = 0
            discount_price = 0
            discount_cup_size = None
            if discount:
                if hasattr(discount, "discountcupsize"):
                    discount_cup_size = discount.discountcupsize.cup
                if hasattr(discount, "discountpercentoff"):
                    discount_percent_off = discount.discountpercentoff.percent_off
                elif hasattr(discount, "discountprice"):
                    discount_price = discount.discountprice.price

            found_object = None
            for item in cup_prices:
                if item["size"] == obj.cup.size:
                    found_object = item
                    break

            if discount_percent_off:
                if discount_cup_size and discount_cup_size != obj.cup:
                    return found_object["price"]
                return found_object["price"] * (1 - discount_percent_off)
            elif discount_price:
                if discount_cup_size and discount_cup_size != obj.cup:
                    return found_object["price"]
                return discount_price
            return found_object["price"]
        return None

    @transaction.atomic
    def create(self, validated_data):
        menu_item_id = validated_data.pop("menu_item", None)
        order = validated_data.pop("order")
        location = order.get("location")
        custom_order__soda = validated_data.pop("custom_order__soda", None)
        custom_order_flavors = validated_data.pop("custom_order_flavors", [])
        cup = validated_data.get("cup", None)

        order, _ = Order.objects.get_or_create(
            collected_by=self.context["request"].user,
            is_paid=False,
            location=location,
        )
        order_item = OrderItem(
            order=order,
            **validated_data,
        )
        order_item.save()
        if custom_order__soda:
            menu_item_custom_order = None
            custom_order = None
            if menu_item_id:
                menu_item_custom_order = MenuItemCustomOrder.objects.create(
                    menu_item_id=menu_item_id, soda=custom_order__soda
                )
                OrderItemMenuItemCustomOrder.objects.create(
                    order_item=order_item, menu_item_custom_order=menu_item_custom_order
                )
                for flavor in custom_order_flavors:
                    try:
                        # If the flavor is already in the menu item, use that quantity
                        quantity = menu_item_custom_order.menu_item.flavors.get(
                            flavor=flavor
                        ).quantity * int(cup.conversion_factor)
                    except MenuItemFlavor.DoesNotExist:
                        quantity = int(cup.conversion_factor)
                    custom_order_flavor = CustomOrderFlavor.objects.create(
                        flavor_id=flavor,
                        quantity=quantity,
                    )
                    CustomOrderFlavorMenuItemCustomOrder.objects.create(
                        custom_order_flavor=custom_order_flavor,
                        menu_item_custom_order=menu_item_custom_order,
                    )
            else:
                custom_order = CustomOrder.objects.create(soda=custom_order__soda)
                OrderItemCustomOrder.objects.create(
                    order_item=order_item, custom_order=custom_order
                )
                for flavor in custom_order_flavors:
                    custom_order_flavor = CustomOrderFlavor.objects.create(
                        flavor_id=flavor,
                        quantity=int(cup.conversion_factor),
                    )
                    CustomOrderFlavorCustomOrder.objects.create(
                        custom_order_flavor=custom_order_flavor,
                        custom_order=custom_order,
                    )
        else:
            menu_item = MenuItem.objects.get(id=menu_item_id)
            OrderItemMenuItem.objects.create(
                order_item=order_item,
                menu_item=menu_item,
            )
        return order_item


class OrderItemDetailSerializer(serializers.ModelSerializer):
    menu_item = OrderItemMenuItemSerializer(read_only=True)
    menu_item_custom_order = OrderItemMenuItemCustomOrderSerializer(read_only=True)
    custom_order = OrderItemCustomOrderSerializer(read_only=True)
    cup = CupDetailSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "menu_item",
            "menu_item_custom_order",
            "custom_order",
            "cup",
            "low_sugar",
            "note",
        ]
        read_only_fields = ["id"]
