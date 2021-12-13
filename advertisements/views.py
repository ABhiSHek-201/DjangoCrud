from django.shortcuts import render
from rest_framework.views import APIView
from .models import Advertisements
from users.models import User
from .serializers import AdvertisementSerializer
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
# Create your views here.

class PublishedAdvertisements(APIView):
    def get(self, request):
        ads = Advertisements.objects.filter(is_published = True).all()
        adsList=[]
        for i in range(len(ads)):
            adsList.append(AdvertisementSerializer(ads[i]).data)
        return Response(adsList)

class AllAdvertisements(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated User!!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated User!!")

        # usr = User.objects.filter(id=payload['id']).first()

        ads = Advertisements.objects.filter(creator = payload['id']).all()
        adsList=[]
        for i in range(len(ads)):
            adsList.append(AdvertisementSerializer(ads[i]).data)
        return Response(adsList)

class AddAdvertisements(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated User!!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated User!!")
            
        usr = User.objects.filter(id = payload["id"]).first()
        
        serializer = UserSerializer(usr)
        save_data = dict()
        for _ in request.data.keys():
            save_data[_] = request.data[_]
        save_data['creator'] = serializer.data['id']

        
        adSerializer = AdvertisementSerializer(data = save_data)
        adSerializer.is_valid(raise_exception=True)
        adSerializer.save()
        
        return Response(adSerializer.data)

class ViewAd(APIView):
    def get(self, request, adv_id):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated User!!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated User!!")

        ads = Advertisements.objects.filter(id=adv_id).first()
        if ads is None:
            raise AuthenticationFailed("Invalid Advertisement")
        

        adSerializer = AdvertisementSerializer(ads)
        if adSerializer.data['is_published'] == False:
            if adSerializer.data["creator"] != payload["id"]:
                raise AuthenticationFailed("Unauthenticated Access!!")

        return Response(adSerializer.data)

class PublishAds(APIView):
    def put(self, request, adv_id):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated User!!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated User!!")

        ads = Advertisements.objects.filter(id=adv_id).first()
        if ads is None:
            raise AuthenticationFailed("Invalid Advertisement")
        

        adSerializer = AdvertisementSerializer(ads)
        if adSerializer.data["creator"] != payload["id"]:
            raise AuthenticationFailed("Unauthenticated Access!!")
        publish_data = dict()
        for _ in adSerializer.data.keys():
            publish_data[_] = adSerializer.data[_]
        
        publish_data['is_published'] = True 
        
        adSerializer = AdvertisementSerializer(ads,publish_data)
        adSerializer.is_valid(raise_exception=True)
        adSerializer.save()

        return Response(adSerializer.data)


class EditAds(APIView):
    def put(self, request, adv_id):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated User!!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated User!!")
        ads = Advertisements.objects.filter(id=adv_id).first()
        if ads is None:
            raise AuthenticationFailed("Invalid Advertisement")

        adSerializer = AdvertisementSerializer(ads)
        if adSerializer.data["creator"] != payload["id"]:
            raise AuthenticationFailed("Unauthenticated Access!!")
        
        adSerializer = AdvertisementSerializer(ads,data = request.data)
        adSerializer.is_valid(raise_exception=True)
        adSerializer.save()
        
        return Response(adSerializer.data)

class DeleteAds(APIView):
    def delete(self, request, adv_id):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated User!!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated User!!")
        ads = Advertisements.objects.filter(id=adv_id).first()
        if ads is None:
            raise AuthenticationFailed("Invalid Advertisement")

        adSerializer = AdvertisementSerializer(ads)
        if adSerializer.data["creator"] == payload["id"]:
            ads.delete()
        else:
            raise AuthenticationFailed("Unauthenticated Access!!")

        return Response({
            'message':"Deleted Advertisement"
        })




