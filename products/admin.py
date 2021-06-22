from django.contrib import admin
from .models import Product, Category, ProductReview

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'pk',
        'name',
        'category',
        'price',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product_id',
        'product',
        'user',
        'content',
        'rating',
        'date_added',
    )

    ordering = ('-date_added',)

admin.site.register(Product, ProductAdmin)  # here is ('Class', 'Models'). The Product is the class, ProductAdmin is the model.
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
