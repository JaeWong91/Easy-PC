from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product     # importing Product class from the products.models

# This is a called a "context processor". Its purpose is to make this
# dictionary available to all templates across the entire application
def bag_contents(request):

    bag_items = []  # start with empty list
    total = 0   # initialize the total to zero
    product_count = 0   # initialize the product count to zero
    bag = request.session.get('bag', {})     # getting bag if it already exists or initializing a dictionaty if not

    # this is a loop to show the total price of the shopping bag on the navbar
    # bag.items() is the bag from the session
    for item_id, item_data in bag.items():  # in the below lines, we changed "item_date" from "quantity". the video lessons did this for the sizes of clothing because items may have same id but different sizes
        product = get_object_or_404(Product, pk=item_id)
        total += item_data * product.price
        product_count += item_data
        bag_items.append({
            'item_id': item_id,
            'quantity': item_data,
            'product': product,     # adding the product object itself so can access the images and so on
        })

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
