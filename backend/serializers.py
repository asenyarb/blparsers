from rest_framework import serializers
from backend.models import PhoneNumber, Post


class PostPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['number']


class PostSerializer(serializers.ModelSerializer):
    phone_numbers = PostPhoneNumberSerializer(source='phones', many=True)

    class Meta:
        model = Post
        fields = ('text', 'link', 'created_date', 'phone_numbers')
