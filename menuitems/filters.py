import django_filters

from menuitems.models import MenuItem


class MenuItemFilter(django_filters.FilterSet):
    limited_time_promotions__isnull = django_filters.BooleanFilter(
        field_name="limited_time_promotions", lookup_expr="isnull"
    )

    class Meta:
        model = MenuItem
        fields = [
            "soda",
            "limited_time_promotions__limited_time_promo",
            "limited_time_promotions__isnull",
        ]
