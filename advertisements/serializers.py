from rest_framework import serializers
from .models import Advertisements
from rest_framework.exceptions import AuthenticationFailed
from users.serializers import UserSerializer
from users.models import User
import jwt, datetime

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisements
        fields = ['id','ad_name','ad_title','ad_desc','creator','is_published']

    def update(self,instance,validated_data):
        if validated_data.get('is_published'):
            instance.is_published = validated_data.get('is_published', instance.is_published)
        else:
            instance.ad_name = validated_data.get('ad_name', instance.ad_name)
            instance.ad_title = validated_data.get('ad_title', instance.ad_title)
            instance.ad_desc = validated_data.get('ad_desc', instance.ad_desc)
        instance.save()
        return instance

