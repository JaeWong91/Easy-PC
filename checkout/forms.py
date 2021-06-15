from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)       # first call the default init method to set the form up as it would be by default
        placeholders = {                        # dictionary of placeholders to show up in the form fields
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True   # set the autofocus attribute on the full name field to true so the cursor will start in the full name field when the user loads page
        for field in self.fields:                                   # iterate through the forms fields to add a star if its a required field from the model
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder        # setting all the placeholder attributes to their values in the dicitonary above
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'     # add css class
            self.fields[field].label = False                                    # remove form fields as will not need them   
