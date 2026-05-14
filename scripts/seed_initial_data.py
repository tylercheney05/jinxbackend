from django.apps import apps
from django.conf import settings
from django.core.management import call_command


def run(*args):
    flush = args[0] == "flush" if len(args) > 0 else False
    if settings.NODE_ENV == "production":
        print("Skipping initial data seeding in production environment.")
        return

    if flush:
        for model in apps.get_models():
            if model.__name__ == "User":
                continue
            model.objects.all().delete()
        print("Flushed the database (preserved User objects).")
    call_command("loaddata", "cups/fixtures/settings.json")
    call_command("loaddata", "sodas/fixtures/settings.json")
    call_command("loaddata", "flavors/fixtures/flavor_group/settings.json")
    call_command("loaddata", "flavors/fixtures/flavor/settings.json")
    call_command("loaddata", "locations/fixtures/settings.json")
    call_command("loaddata", "orders/fixtures/order_name/settings.json")
    call_command("loaddata", "orders/fixtures/discount/settings.json")
    call_command("loaddata", "menuitems/fixtures/menu_item/settings.json")
    call_command("loaddata", "menuitems/fixtures/limited_time_promo/settings.json")
    call_command("loaddata", "menuitems/fixtures/limited_time_menu_item/settings.json")
