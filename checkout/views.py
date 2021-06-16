from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


# this will prevent people from manually accessing the URL by typing '/checkout'
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Ir5QtAPbj4ekIUpdLJKuxrfxxClHrLV5zbTXF4Hk3ILdkqcc2wRBvOpa6FfC17a5rzfh0LNhbAQAiyh0Rk6ZvO0000muCSYeT',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
