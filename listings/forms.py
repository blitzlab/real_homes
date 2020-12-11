from django import forms
from .models import Property, Gallery

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        labels = {
            "address": "Property Address", "description": "Property Description",
            "category": "Property Category", "price": "Property Price",
            "city":"Property City", "featured_image": "Property Featured Image",
            "bedrooms":"No. Bedrooms", "bathrooms": "No. Bathrooms",
            "area_size": "Area Size (sq ft)", "type": "Property Type"
        }
        exclude = ("agent", "status", "slug", )
        # widgets = {'gallery': forms.ClearableFileInput( attrs={'multiple': True})}

#
class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        labels = {
            "image":"Property Gallery"
        }
        fields = ("image", )
        widgets = {'image': forms.ClearableFileInput( attrs={'multiple': True})}
