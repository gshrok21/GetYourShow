from rest_framework import serializers
from .models import event_category
class category_serializer(serializers.ModelSerializer):
    class Meta:
        model=event_category
        fields="__all__"
        