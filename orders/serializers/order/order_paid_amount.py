from rest_framework import serializers

from orders.models import Discount, OrderName, OrderPaidAmount
from orders.serializers import OrderDiscountSerializer, OrderSerializer
from orders.utils.discount import calculate_order_price_with_discount


class OrderPaidAmountSerializer(serializers.ModelSerializer):
    order_name = serializers.PrimaryKeyRelatedField(
        queryset=OrderName.objects.all(), write_only=True
    )
    discount = serializers.PrimaryKeyRelatedField(
        queryset=Discount.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = OrderPaidAmount
        fields = ["id", "order", "order_name", "discount"]
        write_only_fields = ["order"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        order = validated_data.pop("order")
        order_name = validated_data.pop("order_name")
        discount = validated_data.pop("discount", None)

        # Mark order as complete
        order_data = {
            "is_paid": True,
            "order_name": order_name.id,
        }
        order_serializer = OrderSerializer(order, data=order_data, partial=True)
        if order_serializer.is_valid():
            order_serializer.save()
        else:
            raise serializers.ValidationError(order.errors)

        # Create OrderDiscount
        if discount:
            order_discount_data = {
                "order": order.id,
                "discount": discount.id,
            }
            order_discount_serializer = OrderDiscountSerializer(
                data=order_discount_data
            )
            if order_discount_serializer.is_valid():
                order_discount_serializer.save()
            else:
                raise serializers.ValidationError(order_discount_serializer.errors)

        # Create OrderPaidAmount
        if discount:
            paid_amount = calculate_order_price_with_discount(order, discount)
        else:
            paid_amount = order.pending_price
        return OrderPaidAmount.objects.create(order=order, paid_amount=paid_amount)
