from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, ProductReview
from .forms import ProductForm, ReviewForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

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
    user_review = None

    if request.user.is_authenticated:
        user_review = ProductReview.objects.filter(product=product, user=request.user).exists()

    # Add review ------------
    if request.method == 'POST' and request.user.is_authenticated:
        user_review = ProductReview.objects.filter(product=product, user=request.user)

        if user_review:
            messages.error(request, 'You have already reviewed this product.')
            return redirect('product_detail', product_id=product_id)
        else:
            individual_rating = request.POST.get('individual_rating', 3)
            content = request.POST.get('content', '')
            review = ProductReview.objects.create(product=product, user=request.user,
                                                  individual_rating=individual_rating, content=content)

            product.update_rating()
            product.save()

            messages.success(request, 'Thank you for leaving your review!')
            return redirect('product_detail', product_id=product_id)

    context = {
        'product': product,
        'user_review': user_review,
    }

    return render(request, 'products/product_detail.html', context)


# Delete Review
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(ProductReview, pk=review_id)

    if request.user == review.user or request.user.is_superuser:
        review = get_object_or_404(ProductReview, pk=review_id)
        review.delete()

        review.product.update_rating()
        review.product.save()

        messages.success(request, 'You have successfully removed the review!')
        return redirect(reverse('product_detail', args=[review.product.id]))

    else:
        messages.error(request, 'Sorry, you are not permitted to delete this review.')
        return redirect(reverse('product_detail', args=[review.product.id]))


# Edit Review
@login_required
def edit_review(request, review_id):
    """ Edit a review of a product """
    # pre-filling the form by getting the product using get_object_or_404
    review = get_object_or_404(ProductReview, pk=review_id)

    if request.user == review.user or request.user.is_superuser:
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                review.product.update_rating()
                review.product.save()
                messages.success(request, 'Successfully updated review!!')

                return redirect(reverse('product_detail', args=[review.product.id]))
            else:
                messages.error(request, 'Unable to update review. Please check the form is valid.')
        else:
            # instantiating a product form using the product
            form = ReviewForm(instance=review)
            messages.info(request, f'You are editing your review for {review.product}')

    else:
        messages.error(request, 'Sorry, you are not allowed to edit this review.')
        return redirect(reverse('product_detail', args=[review.product.id]))

    template = 'products/edit_review.html'
    context = {
        'form': form,
        'review': review,
    }

    return render(request, template, context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # store the product when calling form.save
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
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

    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated Product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Unable to update product. Please check the form is valid.')
    else:
        form = ProductForm(instance=product)
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
