from rest_framework import serializers
from .models import *

class CryptoObjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    coin_id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    symbol = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=355)
    last_updated = serializers.DateTimeField()

    class Meta:
        model = cryptoObject
        fields = ('id', 'coin_id', 'name', 'symbol', 'image', 'last_updated')
    
class NotificationSerializer(serializers.Serializer):
    coin = CryptoObjectSerializer()
    value_type = serializers.CharField(max_length=255)  
    initial_value = serializers.FloatField()
    final_value = serializers.FloatField()
    enabled = serializers.BooleanField()
    via_mail = serializers.BooleanField()

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.coin = attrs.get('coin', instance.coin)
            instance.value_type = attrs.get('value_type', instance.value_type)
            instance.initial_value = attrs.get('initial_value', instance.initial_value)
            instance.final_value = attrs.get('final_value', instance.final_value)
            instance.enabled = attrs.get('enabled', instance.enabled)
            instance.via_mail = attrs.get('via_mail', instance.via_mail)
            return instance
        return Notification(**attrs)
