from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view tthat renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))    # converting to integer since itll come from the template as a string
    redirect_url = request.POST.get('redirect_url')     # this is to get the redirect url from the form 
    bag = request.session.get('bag', {})    # this bag variable will access the request's session, trying to get the variable if it exists or initializing it to an empty dictionary if it doesn't

    # this will update the bag or update the quantity if it already exists
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag    # and then overwrite the variable in the session with the updated version.
    return redirect(redirect_url)
