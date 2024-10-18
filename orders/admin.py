from django.contrib import admin

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
    OrderDiscount,
    OrderItem,
    OrderItemCustomOrder,
    OrderItemMenuItem,
    OrderItemMenuItemCustomOrder,
    OrderName,
    OrderPaidAmount,
)

admin.site.register(CustomOrder)
admin.site.register(CustomOrderFlavor)
admin.site.register(CustomOrderFlavorCustomOrder)
admin.site.register(CustomOrderFlavorMenuItemCustomOrder)
admin.site.register(Discount)
admin.site.register(DiscountCupSize)
admin.site.register(DiscountPercentOff)
admin.site.register(DiscountPrice)
admin.site.register(MenuItemCustomOrder)
admin.site.register(Order)
admin.site.register(OrderDiscount)
admin.site.register(OrderItem)
admin.site.register(OrderItemCustomOrder)
admin.site.register(OrderItemMenuItem)
admin.site.register(OrderItemMenuItemCustomOrder)
admin.site.register(OrderName)
admin.site.register(OrderPaidAmount)
