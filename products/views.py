from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # special object called Q to generate a search query such that we want the term to be searched in either the product NAME or DESCRIPTION
from django.db.models.functions import Lower

from .models import Product, Category, ProductReview
from .forms import ProductForm

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None    # we start with None so we don't get an error loading the page without a search term.
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:       # check whether 'sort' is in request.GET
            sortkey = request.GET['sort']   # if it is, then we set it equal to both 'sort' and 'sortkey' (which will be 'NONE' at this point).
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'   # then we rename 'sortkey' to 'lower_name' in the event the user is sorting by name
                products = products.annotate(lower_name=Lower('name'))  # then we annotate the current list of products with a new field.
            if sortkey == 'category':
                sortkey = 'category__name'  # the double underscore here allows us to drill into a related model
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':         # then check whether the direction is descending in order to decide whether to reverse the order
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)   # finally, this is the order by model method

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

    current_sorting = f'{sort}_{direction}'  # since we have both the sort and direction variables stored, this string formatting will return it to th e template

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product detail """

    product = get_object_or_404(Product, pk=product_id)

    # Add review -- not working
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating', 3)  # set default to 3
        content = request.POST.get('content', '')
        review = ProductReview.objects.create(product=product, user=request.user, rating=rating, content=content)
        messages.success(request, 'Successfully added review!')

        return redirect('product_detail', product_id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()       # store the product when calling form.save
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))      # send the product id to the redirect URL, this way it will redirect to the product detail page of recently added product
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)     # pre-filling the form by getting the product using get_object_or_404
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated Product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Unable to update product. Please check the form is valid.')
    else:
        form = ProductForm(instance=product)        # instantiating a product form using the product
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
        
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
