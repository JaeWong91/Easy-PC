from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    length = models.DecimalField(max_digits=7, decimal_places=2)  # length, width and height in cm
    width = models.DecimalField(max_digits=7, decimal_places=2)
    height = models.DecimalField(max_digits=7, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)   # weight in kg
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def update_rating(self):   # changed from get_rating
        # get sum of all ratings in review
        total = sum(int(review['individual_rating']) for review in self.reviews.values())   # changed 'rating' to 'individual rating'
        self.rating == 0

        if self.reviews.count() > 0:
            self.rating = total / self.reviews.count()
            self.save()
        else:
            self.rating == 0
            self.save()


# this is from 'Code With Stein' video tutorial - https://www.youtube.com/watch?v=Y5vvGQyHtpM
class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    individual_rating = models.SmallIntegerField(choices=[(i, i) for i in range(1, 6)])

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
