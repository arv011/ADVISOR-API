from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import User, advisers,booking
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

class advisersserializer(serializers.ModelSerializer):
    
    class Meta:
        model = advisers
        fields = ('id','adviser_name','photo_url')

# class advisersbookserializer(serializers.HyperlinkedModelSerializer):
    
#     class Meta:
#         model = advisers
#         fields = ('url','id','adviser_name','photo_url')
    

class registeruserserializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ('id','username','password','email')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate_password(self, value):
        validate_password(value)
        return value

class loginserializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(username=email, password=password)


        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found'
            )
        try:
            refresh = RefreshToken.for_user(user)
            login(self.context['request'], user)
            
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists or incorrect'
            )
        return {
            'email':user.email,
            'user_id':user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    

class bookingserializer(serializers.Serializer):
    booking_time = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
    
class listbookingserializer(serializers.ModelSerializer):
    advisor_id = serializers.CharField(source='adviser_appoint.id', read_only=True)
    advisor_name = serializers.CharField(source='adviser_appoint.adviser_name', read_only=True)
    advisor_photo = serializers.CharField(source='adviser_appoint.photo', read_only=True)
    class Meta:
        model = booking
        fields = ('advisor_id','advisor_name','advisor_photo','booking_time','id')
        extra_kwargs = {
            'id': {'read_only': True},
        }
        label = {
            'id':'booking_id'
        }

# class adviserlistserialiser(serializers.ModelSerializer):
#     # photo_url = serializers.SerializerMethodField()
    
#     class Meta:
#         model = advisers
#         fields = ('id','adviser_name','photo_url','photo')
    
    # def get_photo_url(self,obj):
    #     return self.context['request'].build_absolute_uri( obj.photo_url.url)
