from django.shortcuts import render
from .models import Product

# Create your views here.


def all_products(request):   # video tutorial here is "all_products"
    """ A view to show the graphics cards, including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
