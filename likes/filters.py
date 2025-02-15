import django_filters
from .models import LikedItem



class LikedItemFilter(django_filters.FilterSet):
  model_id = django_filters.AllValuesFilter(field_name="content_type")
  
  class Meta:
    model = LikedItem
    fields = (
      'model_id',
    )

