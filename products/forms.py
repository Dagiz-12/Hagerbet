from django.forms import ModelForm
from products.models import Catagories


# Create the form class.
class MakeForm(ModelForm):
    class Meta:
        model = Catagories
        fields = '__all__'
        labels = {
            'field_name': 'Your Label',  # Explicit label
        }
