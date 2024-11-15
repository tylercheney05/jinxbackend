from django.db import transaction
from rest_framework import serializers

from locations.models import Location
from menuitems.models import MenuItem, MenuItemFlavor
from orders.models import (
    CustomOrder,
    CustomOrderFlavor,
    CustomOrderFlavorCustomOrder,
    CustomOrderFlavorMenuItemCustomOrder,
    Discount,
    DiscountCupSize,
    DiscountPercentOff,
    DiscountPrice,
    MenuItemCustomOrder,
    Order,
    OrderItem,
    OrderItemCustomOrder,
    OrderItemMenuItem,
    OrderItemMenuItemCustomOrder,
    OrderName,
)
from sodas.models import Soda


class OrderSerializer(serializers.ModelSerializer):
    order_name__name = serializers.CharField(source="order_name.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "collected_by",
            "location",
            "order_name__name",
            "is_in_progress",
            "is_complete",
        ]
        read_only_fields = ["id"]


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.IntegerField(write_only=True, required=False)
    cup__size__display = serializers.SerializerMethodField(read_only=True)
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
    order_item_name = serializers.SerializerMethodField(read_only=True)
    soda_name = serializers.SerializerMethodField(read_only=True)
    order_item_flavors = serializers.SerializerMethodField(read_only=True)
    order__id = serializers.PrimaryKeyRelatedField(source="order", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "cup",
            "cup__size__display",
            "low_sugar",
            "menu_item",
            "price",
            "note",
            "custom_order__soda",
            "custom_order_flavors",
            "order_item_name",
            "soda_name",
            "order__id",
            "order__collected_by",
            "order__location",
            "order_item_flavors",
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

    def get_cup__size__display(self, obj):
        return obj.cup.get_size_display()

    def get_soda_name(self, obj):
        if hasattr(obj, "menu_item"):
            return obj.menu_item.menu_item.soda.name
        if hasattr(obj, "custom_order"):
            return obj.custom_order.custom_order.soda.name
        if hasattr(obj, "menu_item_custom_order"):
            return obj.menu_item_custom_order.menu_item_custom_order.soda.name
        return ""

    def get_order_item_name(self, obj):
        if hasattr(obj, "custom_order"):
            custom_order_custom_order_flavors = (
                obj.custom_order.custom_order.custom_order_custom_order_flavors.all()
            )
            flavors = [
                custom_order_custom_order_flavor.custom_order_flavor.flavor.name
                for custom_order_custom_order_flavor in custom_order_custom_order_flavors
            ]
            if len(flavors) > 1:
                flavor_names = ", ".join(flavors[:-1]) + " and " + flavors[-1]
            else:
                flavor_names = flavors[0] if flavors else ""
            return f"Custom Drink: {obj.custom_order.custom_order.soda.name} with {flavor_names}"
        elif hasattr(obj, "menu_item"):
            return obj.menu_item.menu_item.name
        elif hasattr(obj, "menu_item_custom_order"):
            menu_item_custom_order_custom_order_flavors = (
                obj.menu_item_custom_order.menu_item_custom_order.menu_item_custom_order_custom_order_flavors.all()
            )
            flavors = [
                menu_item_custom_order_custom_order_flavor.custom_order_flavor.flavor.name
                for menu_item_custom_order_custom_order_flavor in menu_item_custom_order_custom_order_flavors
            ]
            if len(flavors) > 1:
                flavor_names = ", ".join(flavors[:-1]) + " and " + flavors[-1]
            else:
                flavor_names = flavors[0] if flavors else ""
            return f"{obj.menu_item_custom_order.menu_item_custom_order.menu_item.name} (Customized): {obj.menu_item_custom_order.menu_item_custom_order.soda.name} with {flavor_names}"
        return ""

    def get_order_item_flavors(self, obj):
        flavors = {}
        if hasattr(obj, "menu_item"):
            for flavor in obj.menu_item.menu_item.flavors.all():
                flavors[
                    f"{'SUGAR-FREE ' if obj.low_sugar and flavor.flavor.sugar_free_available else ''}{flavor.flavor.name}"
                ] = f"{round(flavor.quantity * obj.cup.conversion_factor)} {flavor.flavor.flavor_group.get_uom_display()}{'' if flavor.quantity * obj.cup.conversion_factor == 1 else 's'}"
        elif hasattr(obj, "menu_item_custom_order"):
            menu_item_custom_order_custom_order_flavors = (
                obj.menu_item_custom_order.menu_item_custom_order.menu_item_custom_order_custom_order_flavors.all()
            )
            for (
                custom_order_flavor_menu_item_custom_order
            ) in menu_item_custom_order_custom_order_flavors:
                flavors[
                    f"{'SUGAR-FREE ' if obj.low_sugar and custom_order_flavor_menu_item_custom_order.custom_order_flavor.flavor.sugar_free_available else ''}{custom_order_flavor_menu_item_custom_order.custom_order_flavor.flavor.name}"
                ] = f"{round(custom_order_flavor_menu_item_custom_order.custom_order_flavor.quantity)} {custom_order_flavor_menu_item_custom_order.custom_order_flavor.flavor.flavor_group.get_uom_display()}{'' if custom_order_flavor_menu_item_custom_order.custom_order_flavor.quantity == 1 else 's'}"
        elif hasattr(obj, "custom_order"):
            custom_order_custom_order_flavors = (
                obj.custom_order.custom_order.custom_order_custom_order_flavors.all()
            )
            for custom_order_custom_order_flavor in custom_order_custom_order_flavors:
                flavors[
                    f"{'SUGAR-FREE ' if obj.low_sugar and custom_order_custom_order_flavor.custom_order_flavor.flavor else ''}{custom_order_custom_order_flavor.custom_order_flavor.flavor.name}"
                ] = f"{round(custom_order_custom_order_flavor.custom_order_flavor.quantity)} {custom_order_custom_order_flavor.custom_order_flavor.flavor.flavor_group.get_uom_display()}{'' if custom_order_custom_order_flavor.custom_order_flavor.quantity == 1 else 's'}"
        else:
            flavors = {}
        return flavors

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


class OrderNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderName
        fields = ["id", "name"]
        read_only_fields = ["id"]


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True, source="items")
    order_name__name = serializers.CharField(source="order_name.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_items",
            "order_name__name",
        ]


class DiscountSerializer(serializers.ModelSerializer):
    percent_or_price = serializers.CharField(write_only=True)
    percent = serializers.DecimalField(
        max_digits=3, decimal_places=2, write_only=True, required=False
    )
    price = serializers.DecimalField(
        max_digits=5, decimal_places=2, write_only=True, required=False
    )
    is_cup_specific = serializers.BooleanField(write_only=True)
    cup = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Discount
        fields = [
            "id",
            "name",
            "code",
            "percent_or_price",
            "percent",
            "price",
            "is_cup_specific",
            "cup",
        ]
        read_only_fields = ["id"]

    @transaction.atomic
    def create(self, validated_data):
        percent_or_price = validated_data.pop("percent_or_price")
        percent = validated_data.pop("percent", None)
        price = validated_data.pop("price", None)
        is_cup_specific = validated_data.pop("is_cup_specific", False)
        cup_id = validated_data.pop("cup", None)

        discount = Discount.objects.create(**validated_data)

        if is_cup_specific:
            DiscountCupSize.objects.create(discount=discount, cup_id=cup_id)

        if percent_or_price == "percent" and percent is not None:
            DiscountPercentOff.objects.create(discount=discount, percent_off=percent)
        elif percent_or_price == "price" and price is not None:
            DiscountPrice.objects.create(
                discount=discount,
                price=price,
            )
        return validated_data
