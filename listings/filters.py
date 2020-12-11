import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        # fields = "__all__"
        exclude = ["agent", "address", "description", "status", "slug", "price", "published_on", "featured_image", "area_size"]
