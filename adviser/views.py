# from django.shortcuts import render
# from django.http import response
from django.contrib.auth.models import User
from django.http.response import HttpResponseNotAllowed
from .models import advisers, booking
from .serializer import advisersserializer, registeruserserializer, loginserializer, bookingserializer, listbookingserializer
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.


class adviserviewset(viewsets.ModelViewSet):
    queryset = advisers.objects.all()
    serializer_class = advisersserializer
    authentication_classes = [JWTAuthentication,]

    # def get_serializer_class(self):
    #     self.serializer_class = advisersserializer
    #     if self.request.method == "GET":
    #         self.serializer_class = adviserlistserialiser(context={'request': self.request})
    #     return super(adviserviewset, self).get_serializer_class()

    def get_permissions(self):
        self.permission_classes = [IsAdminUser,]
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated,]
        
        return super(adviserviewset,self).get_permissions()   
        

class registerview(APIView):
    def post(self, request):

        serialized = registeruserserializer(data = request.data)
        if serialized.is_valid(raise_exception=True):
            username = serialized.data['username']
            Password = request.data['password']
            email = serialized.data['email']
            user = User(username=username,email=email)
            user.set_password(Password)
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({
            'user_id': user.id,
            'username': user.username,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        },status=status.HTTP_200_OK)
        
        return Response({"exception":"data incorrect"},status = status.HTTP_400_BAD_REQUEST)


class loginapiview(APIView):
    serializer_class = loginserializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = {
            'user_id' : serializer.data['user_id'],
            'access' : serializer.data['access'],
            'refresh' : serializer.data['refresh'],
        }
        return Response(res,status= status.HTTP_200_OK)

    
    
class adviserbookingapi(APIView):
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]
    def post(self, request, pk, pk2):
        if pk == self.request.user.id:
            serializer = bookingserializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                booking_time = serializer.data['booking_time']
                user = User.objects.get(pk=pk)
                advisor = advisers.objects.get(pk=pk2)

                booking.objects.create(
                    user=user,
                    booking_time=booking_time,
                    adviser_appoint=advisor
                )
                return Response(status= status.HTTP_200_OK)
        else:
            return Response({'error':'invalid userid passing in urls'},status=status.HTTP_400_BAD_REQUEST)
                
class bookingslistapi(ListAPIView):
    serializer_class = listbookingserializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            if self.kwargs['pk'] == user.id:
                queryset = booking.objects.filter(pk=user.id)
                return queryset
        