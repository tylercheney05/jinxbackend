from django.contrib import admin

from menuitems.models import (
    LimitedTimeMenuItem,
    LimitedTimePromotion,
    MenuItem,
    MenuItemFlavor,
)

admin.site.register(MenuItem)
admin.site.register(MenuItemFlavor)
admin.site.register(LimitedTimePromotion)
admin.site.register(LimitedTimeMenuItem)
