import os

import pandas as pd
import pytz

from cups.models import Cup
from flavors.models import Flavor, FlavorGroup
from jinxbackend.settings import BASE_DIR
from locations.models import Location
from menuitems.models import (
    LimitedTimeMenuItem,
    LimitedTimePromotion,
    MenuItem,
    MenuItemFlavor,
)
from orders.models import (
    CustomOrder,
    CustomOrderFlavor,
    CustomOrderFlavorCustomOrder,
    Discount,
    DiscountCupSize,
    DiscountPercentOff,
    DiscountPrice,
    Order,
    OrderDiscount,
    OrderItem,
    OrderItemCustomOrder,
    OrderItemMenuItem,
    OrderName,
    OrderPaidAmount,
)
from sodas.models import Soda
from users.models import User


def run():
    # Add cups
    _16_oz, _ = Cup.objects.get_or_create(size="16", price=3, conversion_factor=1)
    print("16 oz cup created")
    _32_oz, _ = Cup.objects.get_or_create(size="32", price=3.5, conversion_factor=2)
    print("32 oz cup created")

    print("\n")
    print("--------------------")
    print("\n")

    # Add sodas
    coke, _ = Soda.objects.get_or_create(name="Coke")
    print("Coke created")
    sprite, _ = Soda.objects.get_or_create(name="Sprite")
    print("Sprite created")
    dp, _ = Soda.objects.get_or_create(name="Dr. Pepper")
    print("Dr. Pepper created")
    mtn_dew, _ = Soda.objects.get_or_create(name="Mtn. Dew")
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
    coconut, _ = Flavor.objects.get_or_create(
        name="Coconut", flavor_group=syrup, sugar_free_available=True
    )
    print("Coconut syrup created")
    cranberry, _ = Flavor.objects.get_or_create(
        name="Cranberry", flavor_group=syrup, sugar_free_available=False
    )
    print("Cranberry syrup created")
    elderflower, _ = Flavor.objects.get_or_create(
        name="Elderflower", flavor_group=syrup, sugar_free_available=False
    )
    print("Elderflower syrup created")
    guava, _ = Flavor.objects.get_or_create(
        name="Guava", flavor_group=syrup, sugar_free_available=False
    )
    print("Guava syrup created")
    hibiscus, _ = Flavor.objects.get_or_create(
        name="Hibiscus", flavor_group=syrup, sugar_free_available=False
    )
    print("Hibiscus syrup created")
    lavender, _ = Flavor.objects.get_or_create(
        name="Lavender", flavor_group=syrup, sugar_free_available=True
    )
    print("Lavender syrup created")
    mango, _ = Flavor.objects.get_or_create(
        name="Mango", flavor_group=syrup, sugar_free_available=True
    )
    print("Mango syrup created")
    peach, _ = Flavor.objects.get_or_create(
        name="Peach", flavor_group=syrup, sugar_free_available=True
    )
    print("Peach syrup created")
    pineapple, _ = Flavor.objects.get_or_create(
        name="Pineapple", flavor_group=syrup, sugar_free_available=True
    )
    print("Pineapple syrup created")
    prickly_pear, _ = Flavor.objects.get_or_create(
        name="Prickly Pear", flavor_group=syrup, sugar_free_available=False
    )
    print("Prickly Pear syrup created")
    raspberry, _ = Flavor.objects.get_or_create(
        name="Raspberry", flavor_group=syrup, sugar_free_available=True
    )
    print("Raspberry syrup created")
    strawberry, _ = Flavor.objects.get_or_create(
        name="Strawberry", flavor_group=syrup, sugar_free_available=True
    )
    print("Strawberry syrup created")
    vanilla, _ = Flavor.objects.get_or_create(
        name="Vanilla", flavor_group=syrup, sugar_free_available=True
    )
    print("Vanilla syrup created")
    mango_puree, _ = Flavor.objects.get_or_create(
        name="Mango Puree", flavor_group=puree, sugar_free_available=False
    )
    print("Mango Puree created")
    raspberry_puree, _ = Flavor.objects.get_or_create(
        name="Raspberry Puree", flavor_group=puree, sugar_free_available=False
    )
    print("Raspberry Puree created")
    coconut_cream, _ = Flavor.objects.get_or_create(
        name="Coconut Cream", flavor_group=coconut_cream, sugar_free_available=False
    )
    print("Coconut Cream created")
    half_and_half, _ = Flavor.objects.get_or_create(
        name="Half & Half", flavor_group=half_and_half, sugar_free_available=False
    )
    print("Half & Half created")
    fresh_lime, _ = Flavor.objects.get_or_create(
        name="Fresh Lime", flavor_group=fruit, sugar_free_available=False
    )
    print("Fresh Lime wedge created")
    cinnamon, _ = Flavor.objects.get_or_create(
        name="Cinnamon", flavor_group=spice, sugar_free_available=False
    )
    print("Cinnamon created")

    pumpkin_spice, _ = Flavor.objects.get_or_create(
        name="Pumpkin Spice", flavor_group=syrup, sugar_free_available=True
    )
    print("Pumpkin Spice created")

    print("\n")
    print("--------------------")
    print("\n")

    ## Add Limited Time Promotions
    lovers_and_friends_fall_2024, _ = LimitedTimePromotion.objects.get_or_create(
        name="Lovers & Friends Fall 2024"
    )
    print("Lovers & Friends Fall 2024 created")

    print("\n")
    print("--------------------")
    print("\n")

    ## Add Menu Items
    got_so_much_soul, _ = MenuItem.objects.get_or_create(
        name="Got So Much Soul", soda=coke
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=got_so_much_soul, flavor=coconut, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=got_so_much_soul, flavor=fresh_lime, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=got_so_much_soul, flavor=coconut_cream, quantity=1
    )
    print("Got So Much Soul created")

    coco_butter_kisses, _ = MenuItem.objects.get_or_create(
        name="Coco Butter Kisses", soda=coke
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=coco_butter_kisses, flavor=vanilla, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=coco_butter_kisses, flavor=half_and_half, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=coco_butter_kisses, flavor=raspberry_puree, quantity=1
    )
    print("Coco Butter Kisses created")

    pineapple_skies, _ = MenuItem.objects.get_or_create(
        name="Pineapple Skies", soda=coke
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=pineapple_skies, flavor=pineapple, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=pineapple_skies, flavor=coconut_cream, quantity=2
    )
    print("Pineapple Skies created")

    thats_frio, _ = MenuItem.objects.get_or_create(name="That's Frio", soda=coke)
    MenuItemFlavor.objects.get_or_create(
        menu_item=thats_frio, flavor=cranberry, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=thats_frio, flavor=elderflower, quantity=1
    )
    print("That's Frio created")

    laugh_now_cry_later, _ = MenuItem.objects.get_or_create(
        name="Laugh Now Cry Later", soda=dp
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=laugh_now_cry_later, flavor=vanilla, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=laugh_now_cry_later, flavor=coconut_cream, quantity=1
    )
    print("Laugh Now Cry Later created")

    ride_wit_me, _ = MenuItem.objects.get_or_create(name="Ride Wit Me", soda=dp)
    MenuItemFlavor.objects.get_or_create(
        menu_item=ride_wit_me, flavor=vanilla, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=ride_wit_me, flavor=peach, quantity=2
    )
    print("Ride Wit Me created")

    everythings_good, _ = MenuItem.objects.get_or_create(
        name="Everything's Good", soda=dp
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=everythings_good, flavor=lavender, quantity=2
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=everythings_good, flavor=strawberry, quantity=1
    )
    print("Everything's Good created")

    my_favorite_part, _ = MenuItem.objects.get_or_create(
        name="My Favorite Part", soda=dp
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=my_favorite_part, flavor=raspberry_puree, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=my_favorite_part, flavor=coconut, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=my_favorite_part, flavor=half_and_half, quantity=1
    )
    print("My Favorite Part created")

    dang, _ = MenuItem.objects.get_or_create(name="Dang!", soda=mtn_dew)
    MenuItemFlavor.objects.get_or_create(menu_item=dang, flavor=hibiscus, quantity=2)
    MenuItemFlavor.objects.get_or_create(menu_item=dang, flavor=coconut, quantity=1)
    MenuItemFlavor.objects.get_or_create(menu_item=dang, flavor=peach, quantity=1)
    print("Dang! created")

    could_you_be_loved, _ = MenuItem.objects.get_or_create(
        name="Could You Be Loved", soda=mtn_dew
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=could_you_be_loved, flavor=elderflower, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=could_you_be_loved, flavor=mango_puree, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=could_you_be_loved, flavor=coconut, quantity=1
    )
    print("Could You Be Loved created")

    livin_on_an_island, _ = MenuItem.objects.get_or_create(
        name="Livin' On An Island", soda=mtn_dew
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=livin_on_an_island, flavor=peach, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=livin_on_an_island, flavor=raspberry, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=livin_on_an_island, flavor=half_and_half, quantity=1
    )
    print("Livin' On An Island created")

    them_summer_nights, _ = MenuItem.objects.get_or_create(
        name="Them Summer Nights", soda=mtn_dew
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=them_summer_nights, flavor=mango_puree, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=them_summer_nights, flavor=strawberry, quantity=2
    )
    print("Them Summer Nights created")

    ride_that_wave, _ = MenuItem.objects.get_or_create(
        name="Ride That Wave", soda=sprite
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=ride_that_wave, flavor=coconut, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=ride_that_wave, flavor=guava, quantity=2
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=ride_that_wave, flavor=fresh_lime, quantity=1
    )
    print("Ride That Wave created")

    suga_suga, _ = MenuItem.objects.get_or_create(name="Suga Suga", soda=sprite)
    MenuItemFlavor.objects.get_or_create(
        menu_item=suga_suga, flavor=prickly_pear, quantity=2
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=suga_suga, flavor=raspberry, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=suga_suga, flavor=strawberry, quantity=1
    )
    print("Suga Suga created")

    still_in_my_vans, _ = MenuItem.objects.get_or_create(
        name="Still In My Vans", soda=sprite
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=still_in_my_vans, flavor=raspberry_puree, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=still_in_my_vans, flavor=vanilla, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=still_in_my_vans, flavor=strawberry, quantity=1
    )
    print("Still In My Vans created")

    young_dumb_and_broke, _ = MenuItem.objects.get_or_create(
        name="Young Dumb & Broke", soda=sprite
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=young_dumb_and_broke, flavor=pineapple, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=young_dumb_and_broke, flavor=coconut_cream, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=young_dumb_and_broke, flavor=strawberry, quantity=1
    )
    print("Young Dumb & Broke created")

    family_business, _ = MenuItem.objects.get_or_create(
        name="Family Business", soda=coke
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=family_business, flavor=vanilla, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=family_business, flavor=pumpkin_spice, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=family_business, flavor=half_and_half, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=family_business, flavor=cinnamon, quantity=1
    )
    LimitedTimeMenuItem.objects.get_or_create(
        menu_item=family_business, limited_time_promo=lovers_and_friends_fall_2024
    )
    print("Family Business created")

    lovers_and_friends, _ = MenuItem.objects.get_or_create(
        name="Lovers & Friends", soda=dp
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=lovers_and_friends, flavor=vanilla, quantity=1
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=lovers_and_friends, flavor=pumpkin_spice, quantity=2
    )
    MenuItemFlavor.objects.get_or_create(
        menu_item=lovers_and_friends, flavor=coconut_cream, quantity=1
    )
    LimitedTimeMenuItem.objects.get_or_create(
        menu_item=lovers_and_friends, limited_time_promo=lovers_and_friends_fall_2024
    )
    print("Lovers & Friends created")

    print("\n")
    print("--------------------")
    print("\n")

    ## Add Locations
    Location.objects.get_or_create(
        name="Midtown Farmer's Market",
        address="1050 20th St",
        city="Sacramento",
        state="CA",
        zip_code="95811",
        is_event=True,
    )
    print("Midtown Farmers Market created")

    Location.objects.get_or_create(
        name="Sactowns Finest Market",
        address="1715 R St",
        city="Sacramento",
        state="CA",
        zip_code="95811",
        is_event=True,
    )
    print("Sactowns Finest Market created")

    Location.objects.get_or_create(
        name="Soda Way",
        address="3341 Soda Way",
        city="Sacramento",
        state="CA",
        zip_code="95834",
        is_event=False,
    )
    print("Soda Way created")

    Location.objects.get_or_create(
        name="World's Worst Second Saturday",
        address="2000 K St",
        city="Sacramento",
        state="CA",
        zip_code="95811",
        is_event=True,
    )
    print("World's Worst Second Saturday created")

    print("\n")
    print("--------------------")
    print("\n")

    ## Add Order Names
    OrderName.objects.get_or_create(name="Aminé")
    print("Aminé created")
    OrderName.objects.get_or_create(name="Busta Rhymes")
    print("Busta Rhymes created")
    OrderName.objects.get_or_create(name="Kanye West The Boy")
    print("Kanye West created")
    OrderName.objects.get_or_create(name="Ashanti")
    print("Ashanti created")
    OrderName.objects.get_or_create(name="Dr. Dre")
    print("Dr. Dre created")
    OrderName.objects.get_or_create(name="Kid Cudi")
    print("Kid Cudi created")
    OrderName.objects.get_or_create(name="50 Cent")
    print("50 Cent created")
    OrderName.objects.get_or_create(name="Lil Rob")
    print("Lil Rob created")
    OrderName.objects.get_or_create(name="Missy Elliott")
    print("Missy Elliott created")
    OrderName.objects.get_or_create(name="Cactus Jack")
    print("Cactus Jack created")
    OrderName.objects.get_or_create(name="Ja Rule")
    print("Ja Rule created")
    OrderName.objects.get_or_create(name="Snoop Dogg")
    print("Snoop Dogg created")
    OrderName.objects.get_or_create(name="2Pac")
    print("2Pac created")
    OrderName.objects.get_or_create(name="Mac Miller")
    print("Mac Miller created")
    OrderName.objects.get_or_create(name="Ludacris")
    print("Ludacris created")
    OrderName.objects.get_or_create(name="Mary J. Blige")
    print("Mary J. Blige created")
    OrderName.objects.get_or_create(name="Usher")
    print("Usher created")
    OrderName.objects.get_or_create(name="Beyoncé")
    print("Beyoncé created")
    OrderName.objects.get_or_create(name="Chance The Rapper")
    print("Chance The Rapper created")
    OrderName.objects.get_or_create(name="Breezy")
    print("Breezy created")
    OrderName.objects.get_or_create(name="Ms. Lauryn Hill")
    print("Ms. Lauryn Hill created")
    OrderName.objects.get_or_create(name="BadGal RiRi")
    print("BadGal RiRi created")
    OrderName.objects.get_or_create(name="Champagne Papi")
    print("Champagne Papi created")
    OrderName.objects.get_or_create(name="Future")
    print("Future created")
    OrderName.objects.get_or_create(name="Jay-Z")
    print("Jay-Z created")
    OrderName.objects.get_or_create(name="BIg Poppa")
    print("Big Poppa created")
    OrderName.objects.get_or_create(name="Slim Shady")
    print("Slim Shady created")
    OrderName.objects.get_or_create(name="Childish Gambino")
    print("Childish Gambino created")
    OrderName.objects.get_or_create(name="Larry Fisherman")
    print("Larry Fisherman created")
    OrderName.objects.get_or_create(name="Bobby Tarantino")
    print("Bobby Tarantino created")
    OrderName.objects.get_or_create(name="Migos")
    print("Migos created")
    OrderName.objects.get_or_create(name="Bow Wow")
    print("Bow Wow created")
    OrderName.objects.get_or_create(name="Ciara")
    print("Ciara created")

    print("\n")
    print("--------------------")
    print("\n")

    ## Add Discounts
    free_discount, _ = Discount.objects.get_or_create(name="Free", code="FREE")
    DiscountPercentOff(discount=free_discount, percent_off=1)
    print("Free discount created")

    lime_bois_am_perk, _ = Discount.objects.get_or_create(
        name="Lime Boi's AM Perk", code="AMPERK202409"
    )
    DiscountPrice.objects.get_or_create(discount=lime_bois_am_perk, price=4)
    DiscountCupSize.objects.get_or_create(discount=lime_bois_am_perk, cup=_16_oz)
    print("Lime Boi's AM Perk discount created")

    print("\n")
    print("--------------------")
    print("\n")

    file_location = os.path.join(BASE_DIR, "files", "Order Tracking.xlsx")
    menu_item_orders = pd.read_excel(file_location, sheet_name="Menu Item Orders")
    custom_orders = pd.read_excel(file_location, sheet_name="BYO Orders")

    cup_mapping = {
        "16 oz": "16",
        "32 oz": "32",
    }

    ## Add Menu Item Orders
    prev_order_num = 0
    for label, row in menu_item_orders.iterrows():
        order_num = row["Order #"]
        date = row["Date"]
        location = row["Location"]
        cup = row["Cup"]
        zero_sugar = row["Zero Sugar"]
        menu_item = row["Menu Item"]
        charged = row["Charged"]
        discount_code = row["Discount Code"]

        location_obj = Location.objects.get(name=location)
        cup_obj = Cup.objects.get(size=cup_mapping[cup])
        menu_item_obj = MenuItem.objects.get(name__iexact=menu_item)

        if order_num != prev_order_num:
            total_charged = charged
            date = date.to_pydatetime()
            pacific = pytz.timezone("US/Pacific")
            utc = pytz.utc
            date = pacific.localize(date).astimezone(utc)

            order = Order.objects.create(
                date=date,
                collected_by=User.objects.first(),
                is_paid=True,
                location=location_obj,
                is_complete=True,
                is_in_progress=False,
            )
            print(f"Order {order_num} created")

            OrderPaidAmount.objects.create(order=order, paid_amount=total_charged)
            print(f"OrderPaidAmount {order_num} ${total_charged} created")
        else:
            total_charged += charged
            OrderPaidAmount.objects.filter(order=order).update(
                paid_amount=total_charged
            )
            print(f"OrderPaidAmount {order_num} ${total_charged} updated")

        order_item = OrderItem.objects.create(
            order=order, cup=cup_obj, low_sugar=zero_sugar, is_prepared=True
        )
        print(f"OrderItem {order_num} {menu_item} created")

        OrderItemMenuItem.objects.create(order_item=order_item, menu_item=menu_item_obj)
        print(f"OrderItemMenuItem {order_num} {menu_item} created")

        if pd.notna(discount_code):
            discount = Discount.objects.get(code=discount_code)
            OrderDiscount.objects.create(order=order, discount=discount)
            print(f"OrderDiscount {order_num} {discount_code} created")
        elif charged == 0:
            OrderDiscount.objects.create(order=order, discount=free_discount)
            print(f"OrderDiscount {order_num} FREE created")

        prev_order_num = order_num

    print("\n")
    print("--------------------")
    print("\n")

    ## Add Custom Orders
    prev_order_num = 0
    for label, row in custom_orders.iterrows():
        order_num = row["Order #"]
        date = row["Date"]
        location = row["Location"]
        cup = row["Cup"]
        zero_sugar = row["Zero Sugar"]
        soda = row["Soda"].strip()
        flavor1 = row["Flavor 1"]
        flavor2 = row["Flavor 2"]
        flavor3 = row["Flavor 3"]
        flavor4 = row["Flavor 4"]
        charged = row["Charged"]

        location_obj = Location.objects.get(name=location)
        cup_obj = Cup.objects.get(size=cup_mapping[cup])
        soda_obj = Soda.objects.get(name=soda)

        flavor1 = Flavor.objects.get(name=flavor1) if pd.notna(flavor1) else None
        flavor2 = Flavor.objects.get(name=flavor2) if pd.notna(flavor2) else None
        flavor3 = Flavor.objects.get(name=flavor3) if pd.notna(flavor3) else None
        flavor4 = Flavor.objects.get(name=flavor4) if pd.notna(flavor4) else None

        if order_num != prev_order_num:
            total_charged = charged
            date = date.to_pydatetime()
            pacific = pytz.timezone("US/Pacific")
            utc = pytz.utc
            date = pacific.localize(date).astimezone(utc)

            order = Order.objects.create(
                date=date,
                collected_by=User.objects.first(),
                is_paid=True,
                location=location_obj,
                is_complete=True,
                is_in_progress=False,
            )
            print(f"Order {order_num} created")

            OrderPaidAmount.objects.create(order=order, paid_amount=total_charged)
            print(f"OrderPaidAmount {order_num} ${total_charged} created")
        else:
            total_charged += charged
            OrderPaidAmount.objects.filter(order=order).update(
                paid_amount=total_charged
            )
            print(f"OrderPaidAmount {order_num} ${total_charged} updated")

        order_item = OrderItem.objects.create(
            order=order, cup=cup_obj, low_sugar=zero_sugar, is_prepared=True
        )
        print(f"OrderItem {order_num} Custom Order created")

        custom_order = CustomOrder.objects.create(
            soda=soda_obj,
        )
        print(f"CustomOrder {order_num} created")

        OrderItemCustomOrder.objects.create(
            order_item=order_item, custom_order=custom_order
        )
        print(f"OrderItemCustomOrder {order_num} created")

        quantity_mapping = {
            "16 oz": 1,
            "32 oz": 2,
        }

        if flavor1:
            custom_flavor1 = CustomOrderFlavor.objects.create(
                flavor=flavor1, quantity=quantity_mapping[cup]
            )
            CustomOrderFlavorCustomOrder.objects.create(
                custom_order_flavor=custom_flavor1, custom_order=custom_order
            )
            print(f"CustomOrderFlavor {order_num} {flavor1} created")
        if flavor2:
            custom_flavor2 = CustomOrderFlavor.objects.create(
                flavor=flavor2, quantity=quantity_mapping[cup]
            )
            CustomOrderFlavorCustomOrder.objects.create(
                custom_order_flavor=custom_flavor2, custom_order=custom_order
            )
            print(f"CustomOrderFlavor {order_num} {flavor2} created")
        if flavor3:
            custom_flavor3 = CustomOrderFlavor.objects.create(
                flavor=flavor3, quantity=quantity_mapping[cup]
            )
            CustomOrderFlavorCustomOrder.objects.create(
                custom_order_flavor=custom_flavor3, custom_order=custom_order
            )
            print(f"CustomOrderFlavor {order_num} {flavor3} created")
        if flavor4:
            custom_flavor4 = CustomOrderFlavor.objects.create(
                flavor=flavor4, quantity=quantity_mapping[cup]
            )
            CustomOrderFlavorCustomOrder.objects.create(
                custom_order_flavor=custom_flavor4, custom_order=custom_order
            )
            print(f"CustomOrderFlavor {order_num} {flavor4} created")

        if charged == 0:
            OrderDiscount.objects.create(order=order, discount=free_discount)
            print(f"OrderDiscount {order_num} FREE created")
