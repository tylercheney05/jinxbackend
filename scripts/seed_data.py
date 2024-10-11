from cups.models import Cup
from flavors.models import Flavor, FlavorGroup
from sodas.models import Soda


def run():
    # Add cups
    Cup.objects.get_or_create(size="16", price=3, conversion_factor=1)
    print("16 oz cup created")
    Cup.objects.get_or_create(size="32", price=3.5, conversion_factor=2)
    print("32 oz cup created")

    print("\n")
    print("--------------------")
    print("\n")

    # Add sodas
    Soda.objects.get_or_create(name="Coke")
    print("Coke created")
    Soda.objects.get_or_create(name="Sprite")
    print("Sprite created")
    Soda.objects.get_or_create(name="Dr. Pepper")
    print("Dr. Pepper created")
    Soda.objects.get_or_create(name="Mtn. Dew")
    print("Mtn. Dew created")

    print("\n")
    print("--------------------")
    print("\n")

    ## Add Flavor Groups
    syrup, _ = FlavorGroup.objects.get_or_create(name="Syrup", uom="pump", price=0.5)
    print("Syrup created")
    puree, _ = FlavorGroup.objects.get_or_create(name="Puree", uom="tbs", price=0.75)
    print("Puree created")
    coconut_cream, _ = FlavorGroup.objects.get_or_create(
        name="Coconut Cream", uom="tbs", price=0.75
    )
    print("Coconut Cream created")
    half_and_half, _ = FlavorGroup.objects.get_or_create(
        name="Half & Half", uom="single", price=0.75
    )
    print("Half & Half created")
    fruit, _ = FlavorGroup.objects.get_or_create(name="Fruit", uom="wedge", price=0.5)
    print("Fruit created")
    spice, _ = FlavorGroup.objects.get_or_create(name="Spice", uom="pinch", price=0)
    print("Spice created")

    print("\n")
    print("--------------------")
    print("\n")

    ## Add Flavors
    Flavor.objects.get_or_create(
        name="Coconut", flavor_group=syrup, sugar_free_available=True
    )
    print("Coconut syrup created")
    Flavor.objects.get_or_create(
        name="Cranberry", flavor_group=syrup, sugar_free_available=False
    )
    print("Cranberry syrup created")
    Flavor.objects.get_or_create(
        name="Elderflower", flavor_group=syrup, sugar_free_available=False
    )
    print("Elderflower syrup created")
    Flavor.objects.get_or_create(
        name="Guava", flavor_group=syrup, sugar_free_available=False
    )
    print("Guava syrup created")
    Flavor.objects.get_or_create(
        name="Hibiscus", flavor_group=syrup, sugar_free_available=False
    )
    print("Hibiscus syrup created")
    Flavor.objects.get_or_create(
        name="Lavender", flavor_group=syrup, sugar_free_available=True
    )
    print("Lavender syrup created")
    Flavor.objects.get_or_create(
        name="Mango", flavor_group=syrup, sugar_free_available=True
    )
    print("Mango syrup created")
    Flavor.objects.get_or_create(
        name="Peach", flavor_group=syrup, sugar_free_available=True
    )
    print("Peach syrup created")
    Flavor.objects.get_or_create(
        name="Pineapple", flavor_group=syrup, sugar_free_available=True
    )
    print("Pineapple syrup created")
    Flavor.objects.get_or_create(
        name="Prickly Pear", flavor_group=syrup, sugar_free_available=False
    )
    print("Prickly Pear syrup created")
    Flavor.objects.get_or_create(
        name="Raspberry", flavor_group=syrup, sugar_free_available=True
    )
    print("Raspberry syrup created")
    Flavor.objects.get_or_create(
        name="Strawberry", flavor_group=syrup, sugar_free_available=True
    )
    print("Strawberry syrup created")
    Flavor.objects.get_or_create(
        name="Vanilla", flavor_group=syrup, sugar_free_available=True
    )
    print("Vanilla syrup created")
    Flavor.objects.get_or_create(
        name="Mango Puree", flavor_group=puree, sugar_free_available=False
    )
    print("Mango Puree created")
    Flavor.objects.get_or_create(
        name="Raspberry Puree", flavor_group=puree, sugar_free_available=False
    )
    print("Raspberry Puree created")
    Flavor.objects.get_or_create(
        name="Coconut Cream", flavor_group=coconut_cream, sugar_free_available=False
    )
    print("Coconut Cream created")
    Flavor.objects.get_or_create(
        name="Half & Half", flavor_group=half_and_half, sugar_free_available=False
    )
    print("Half & Half created")
    Flavor.objects.get_or_create(
        name="Fresh Lime", flavor_group=fruit, sugar_free_available=False
    )
    print("Fresh Lime wedge created")
    Flavor.objects.get_or_create(
        name="Cinnamon", flavor_group=spice, sugar_free_available=False
    )
    print("Cinnamon created")
