from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product
# Create your views here.


def view_bag(request):
    """ A view tthat renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))    # converting to integer since itll come from the template as a string
    redirect_url = request.POST.get('redirect_url')     # this is to get the redirect url from the form 
    bag = request.session.get('bag', {})    # this bag variable will access the request's session, trying to get the variable if it exists or initializing it to an empty dictionary if it doesn't

    # this will update the bag or update the quantity if it already exists
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag    # and then overwrite the variable in the session with the updated version.
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ adjust the quantity of the specified product to the specified amount """

    quantity = int(request.POST.get('quantity'))    # converting to integer since itll come from the template as a string
    bag = request.session.get('bag', {})    # this bag variable will access the request's session, trying to get the variable if it exists or initializing it to an empty dictionary if it doesn't

    if quantity > 0:
        bag[item_id] = quantity
    else:
        bag.pop(item_id)

    request.session['bag'] = bag    # and then overwrite the variable in the session with the updated version.
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ remove the item from shopping bag """
    try:
        bag = request.session.get('bag', {})    # this bag variable will access the request's session, trying to get the variable if it exists or initializing it to an empty dictionary if it doesn't
        bag.pop(item_id)

        request.session['bag'] = bag    # and then overwrite the variable in the session with the updated version.
        return HttpResponse(status=200)     # use HttpResponse 200 status to imply item was successfully removed

    except Exception as e:
        return HttpResponse(status=500)
