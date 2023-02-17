from django.utils.text import slugify
from rest_framework import serializers
from .models import Wish


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('title', 'description', 'fulfilled',)

    def create(self, validated_data):
        validated_data['user'] = self.context
        validated_data['slug'] = slugify(validated_data['title'][:20])
        return Wish.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('title') is not None:
            instance.title = validated_data['title']
            instance.slug = slugify(validated_data['title'])

        if validated_data.get('description') is not None:
            instance.description = validated_data['description']

        if validated_data.get('fulfilled') is not None:
            instance.fulfilled = validated_data['fulfilled']

        instance.save()
        return instance
