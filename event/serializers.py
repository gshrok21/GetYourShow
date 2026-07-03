from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def validate(self, data):
        is_online = data.get('is_online')
        online_link = data.get('online_link')
        is_free = data.get('is_free')
        price = data.get('price')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if is_online and not online_link:
            raise serializers.ValidationError({
                "online_link": "Online link is required for online events."
            })

        if not is_free and not price:
            raise serializers.ValidationError({
                "price": "Price is required for paid events."
            })

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError({
                    "end_date": "End date must be after start date."
                })

        return data