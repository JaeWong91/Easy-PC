from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents       # this imported function just returns a Python dictionary, we use the variable below "current_bag" to not overrite the bag variable that already exists

import stripe


# this will prevent people from manually accessing the URL by typing '/checkout'
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)         # this is so it does not overwrite the bag variable that already exists
    total = current_bag['grand_total']          # get the grand_total key out of the current bag
    stripe_total = round(total * 100)           # multiply by 100 and round it to zero decimal places using the round function since stripe will require the amount to charge as an integer
    stripe.api_key = stripe_secret_key          # set secret key on stripe
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
