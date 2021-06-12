from decimal import Decimal
from django.conf import settings


# This is a called a "context processor". Its purpose is to make this
# dictionary available to all templates across the entire application
def bag_contents(request):

    bag_items = []  # start with empty list
    total = 0   # initialize the total to zero
    product_count = 0   #initialize the product count to zero


    # this to calculate if qualifies for free delievery.
    # The STANDARD_DELIVERY_PERCENTAGE is 10% from settings.py at the bottom
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    # this is to add the below to the context so they'll be available
    # throughout the whole site
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
