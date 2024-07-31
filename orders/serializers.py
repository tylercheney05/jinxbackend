from rest_framework import serializers

from locations.models import Location
from menuitems.models import MenuItem
from orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "completed_by"]
        read_only_fields = ["id"]


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.IntegerField(write_only=True)
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
        ]

    def get_price(self, obj):
        if obj.content_type.model == "menuitem":
            found_object = next(
                item
                for item in obj.content_object.cup_prices
                if item["size"] == obj.cup.size
            )
            return found_object["price"]

    def get_cup__size__display(self, obj):
        return obj.cup.get_size_display()

    def create(self, validated_data):
        menu_item_id = validated_data.pop("menu_item")
        order = validated_data.pop("order")
        location = order.get("location")

        order, _ = Order.objects.get_or_create(
            completed_by=self.context["request"].user,
            is_paid=False,
            location=location,
        )
        content_object = MenuItem.objects.get(id=menu_item_id)
        order_item = OrderItem(
            order=order,
            content_object=content_object,
            **validated_data,
        )
        order_item.save()
        return order_item
