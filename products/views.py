from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q  # special object called Q to generate a search query such that we want the term to be searched in either the product NAME or DESCRIPTION
from .models import Product, Category

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None    # we start with None so we don't get an error loading the page without a search term.
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            # the double underscore '__' is a common syntax in django when making queries. Using is here means we're looking for the name field of the category model.
            # We are able to do this because category and product are related with a foreign key
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)  # converting the list of strings of category names passed through the URL into a list of actual category objects so we can access all their fields in the template.
            
        if 'q' in request.GET:  # we named the text input in the form as 'q'. this checks if 'q' is in request.GET
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")  # when nothing is entered, it will show error message and return to products page
                return redirect(reverse('products'))

            # here we set the variable "queries" equal to the Q object
            # the pipe | is the OR statement. the "i" in icontains makes the queries case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)  # now we pass them to the filter method in order to actually filter the products

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories, 
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product detail """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
