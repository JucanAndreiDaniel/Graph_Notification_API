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
        fields = ("id", "coin_id", "name", "symbol", "image", "last_updated")


class NotificationSerializer(serializers.Serializer):
    coin = CryptoObjectSerializer()
    value_type = serializers.CharField(max_length=255)
    initial_value = serializers.FloatField()
    final_value = serializers.FloatField()
    enabled = serializers.BooleanField()
    via_mail = serializers.BooleanField()

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.coin = attrs.get("coin", instance.coin)
            instance.value_type = attrs.get("value_type", instance.value_type)
            instance.initial_value = attrs.get("initial_value", instance.initial_value)
            instance.final_value = attrs.get("final_value", instance.final_value)
            instance.enabled = attrs.get("enabled", instance.enabled)
            instance.via_mail = attrs.get("via_mail", instance.via_mail)
            return instance
        return Notification(**attrs)


class NewsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    source_name = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)
    published_at = serializers.DateTimeField(7)

    class Meta:
        model = News
        fields = (
            "id",
            "source_name",
            "author",
            "title",
            "description",
            "url",
            "image_url",
            "published_at",
        )

class NewsListSerializer(serializers.ListSerializer):
    child = NewsSerializer()
    many=True

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.source_name = attrs.get("source_name", instance.source_name)
            instance.author = attrs.get("author", instance.author)
            instance.title = attrs.get("title", instance.title)
            instance.description = attrs.get("description", instance.description)
            instance.url = attrs.get("url", instance.url)
            instance.image_url = attrs.get("image_url", instance.image_url)
            instance.published_at = attrs.get("published_at", instance.published_at)
            return instance
        return News(**attrs)
