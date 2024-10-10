from cups.models import Cup


def run():
    # Add cups
    Cup.objects.get_or_create(size="16", price=3, conversion_factor=1)
    print("16 oz cup created")
    Cup.objects.get_or_create(size="32", price=3.5, conversion_factor=2)
    print("32 oz cup created")
