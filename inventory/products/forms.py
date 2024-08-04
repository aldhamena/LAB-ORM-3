# from django import forms
# from products.models import Product

# # Create the form class.
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = "__all__"
#         widgets = {
#             'title' : forms.TextInput({"class" : "form-control"})
#         }

from django import forms
from products.models import Product

# Create the form class.
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'title' : forms.TextInput({"class" : "form-control"})
        }