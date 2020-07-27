from rest_framework import serializers
from .models import PublicationPhoneNumber, Publication


class PublicationPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationPhoneNumber
        fields = ['number']


class PublicationSerializer(serializers.ModelSerializer):
    phone_numbers = PublicationPhoneNumberSerializer(source='phones', many=True)

    class Meta:
        model = Publication
        fields = ('text', 'link', 'created_date', 'phone_numbers')
