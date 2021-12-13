from django import http
from django.http import response
from django.shortcuts import render, redirect
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        if request.data["password"] == request.data["cnf_password"]:
            serializer = UserSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            raise AuthenticationFailed("Passwords do no Match!!")

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        usr = User.objects.filter(email=email).first()
        if usr is None:
            raise AuthenticationFailed("User Not Found!!")
        if not usr.check_password(password):
            raise AuthenticationFailed("Incorrect Password!!")

        payload= {
            'id':usr.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret',algorithm='HS256')
        
        response =  Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'jwt':token
        }

        return response

class AllUsersView(APIView):
    def get(self,request):
        usr = User.objects.all()
        usrList=[]
        for i in range(len(usr)):
            usrList.append(UserSerializer(usr[i]).data)
        return Response(usrList)

class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated User!!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated User!!")
        usr = User.objects.filter(id = payload["id"]).first()
        
        serializer = UserSerializer(usr)
        
        return Response(serializer.data)
    

class LogoutView(APIView):
    def get(self,request):
        response =Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'Successfully Logged Out!!'
        }
        return response

class EditView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated User!!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated User!!")

        usr = User.objects.filter(id=payload['id']).first()

        serializer=UserSerializer(usr,data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

class DeleteView(APIView):
    def delete(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated User!!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated User!!")

        usr = User.objects.filter(id=payload['id']).first()

        usr.delete()
        
        response =Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'Successfully Deleted User!!'
        }
        return response