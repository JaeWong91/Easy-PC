from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, ProductReview


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('rating',)

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)
    length = forms.DecimalField(label='Length (centimetres)')
    width = forms.DecimalField(label='Width (centimetres)')
    height = forms.DecimalField(label='Height (centimetres)')
    weight = forms.DecimalField(label='Weight (kilograms)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-purple rounded-0'


class ReviewForm(forms.ModelForm):

    class Meta:
        model = ProductReview
        fields = ('content', 'individual_rating',)

    # individual_rating = forms.(label='New Rating',)
    content = forms.CharField(label='Comment')
