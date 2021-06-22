from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'  # this is to fix the spelling mistake you can see on the admin. It would normally appear as "Categorys"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)  # more friendly looking in the front=end. blank=True means is optional

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    length = models.DecimalField(max_digits=4, decimal_places=2)  # length, width and height in cm
    width = models.DecimalField(max_digits=4, decimal_places=2)
    height = models.DecimalField(max_digits=4, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)   # weight in kg
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # product_rating = models.ForeignKey('ProductReview', on_delete=models.CASCADE )   # try to get it so all products page sorts the products by rating!
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) # need to change this so that it uses the average ratings somehow
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_rating(self):
        total = sum(int(review['rating']) for review in self.reviews.values())  # get sum of all ratings in review

        if total > 0:
            total / self.reviews.count()


# this is from 'Code With Stein' video tutorial - https://www.youtube.com/watch?v=Y5vvGQyHtpM
class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)

    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField()

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rating
