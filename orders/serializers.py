from django.db import transaction
from rest_framework import serializers

from locations.models import Location
from menuitems.models import MenuItem
from orders.models import CustomOrder, CustomOrderFlavor, Order, OrderItem
from sodas.models import Soda


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "completed_by"]
        read_only_fields = ["id"]


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.IntegerField(write_only=True, required=False)
    menu_item__name = serializers.CharField(
        source="content_object.name", read_only=True
    )
    cup__size__display = serializers.SerializerMethodField(read_only=True)
    order__completed_by = serializers.PrimaryKeyRelatedField(
        source="order.completed_by", read_only=True
    )
    price = serializers.SerializerMethodField(read_only=True)
    order__location = serializers.PrimaryKeyRelatedField(
        source="order.location", write_only=True, queryset=Location.objects.all()
    )
    custom_order__soda = serializers.PrimaryKeyRelatedField(
        write_only=True, required=False, queryset=Soda.objects.all(), allow_null=True
    )
    custom_order_flavors = serializers.ListField(
        child=serializers.DictField(), write_only=True
    )
    custom_order_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "cup",
            "cup__size__display",
            "zero_sugar",
            "menu_item",
            "menu_item__name",
            "order__completed_by",
            "price",
            "order__location",
            "note",
            "custom_order__soda",
            "custom_order_flavors",
            "custom_order_name",
        ]

    def get_price(self, obj):
        found_object = next(
            item
            for item in obj.content_object.cup_prices
            if item["size"] == obj.cup.size
        )
        return found_object["price"]

    def get_cup__size__display(self, obj):
        return obj.cup.get_size_display()

    def get_custom_order_name(self, obj):
        if obj.content_type.model == "customorder":
            flavors = [
                flavor.flavor.name for flavor in obj.content_object.custom_flavors.all()
            ]
            if len(flavors) > 1:
                flavor_names = ", ".join(flavors[:-1]) + " and " + flavors[-1]
            else:
                flavor_names = flavors[0] if flavors else ""
            return f"Custom: {obj.content_object.soda.name} with {flavor_names}"
        return ""

    @transaction.atomic
    def create(self, validated_data):
        menu_item_id = validated_data.pop("menu_item", None)
        order = validated_data.pop("order")
        location = order.get("location")
        custom_order__soda = validated_data.pop("custom_order__soda", None)
        custom_order_flavors = validated_data.pop("custom_order_flavors", [])

        order, _ = Order.objects.get_or_create(
            completed_by=self.context["request"].user,
            is_paid=False,
            location=location,
        )
        if custom_order__soda:
            custom_order = CustomOrder.objects.create(soda=custom_order__soda)
            for flavor in custom_order_flavors:
                CustomOrderFlavor.objects.create(
                    custom_order=custom_order,
                    flavor_id=flavor["flavor"],
                    quantity=flavor["quantity"],
                )
            content_object = custom_order
        else:
            content_object = MenuItem.objects.get(id=menu_item_id)

        order_item = OrderItem(
            order=order,
            content_object=content_object,
            **validated_data,
        )
        order_item.save()
        return order_item
