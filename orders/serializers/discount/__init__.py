from rest_framework import serializers

from orders.models import Discount, DiscountCupSize, DiscountPercentOff, DiscountPrice


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
