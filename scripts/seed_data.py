from cups.models import Cup
from flavors.models import FlavorGroup
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

    ## Flavor Group
    FlavorGroup.objects.get_or_create(name="Syrup", uom="pump", price=0.5)
    print("Syrup created")
    FlavorGroup.objects.get_or_create(name="Puree", uom="tbs", price=0.75)
    print("Puree created")
    FlavorGroup.objects.get_or_create(name="Coconut Cream", uom="tbs", price=0.75)
    print("Coconut Cream created")
    FlavorGroup.objects.get_or_create(name="Half & Half", uom="single", price=0.75)
    print("Half & Half created")
    FlavorGroup.objects.get_or_create(name="Fruit", uom="wedge", price=0.5)
    print("Fruit created")
    FlavorGroup.objects.get_or_create(name="Spice", uom="pinch", price=0)
    print("Spice created")
