from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from home.models import *
from home.serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from.permission import IsAdminUser
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed  
from django.db.models import Q

# Create your views here.


class RegisterAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": RegisterSerializer(user).data,
                "message": "User created successfully"
            })
        return Response(serializer.errors, status=400)

 
class PublicEventViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']
    
    
    @action(detail=False, methods=['GET'])
    def search_events(Self, request):
        search = request.GET.get("search")
        events = Event.objects.all()
        if search:
            events = events.filter(Q(title__icontains=search) | Q(description__icontains=search))

        serializer = EventSerializer(events, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        })    

    
    # def create(self, request):
    #     raise MethonNotAllowed('POST')
    
    # def update(self, request, *args, **kwargs):
    #     raise MethonNotAllowed('PUT')
    
    # def destroy(self, request, *args, **kwargs):
    #     raise MethonNotAllowed('DELETE')
    
    
        
    
    
    
    
class PrivateEventViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(username=user)
                token, created = Token.objects.get_or_create(user=user)
                if user.check_password(password):
                    return Response({"message": "Login successful",
                                     "user": {
                                         "username": user.username,
                                         "email": user.email,
                                         "first_name": user.first_name,
                                         "last_name": user.last_name
                                     },
                                     "token": token.key}, status=200)
                else:
                    return Response({"error": "Invalid credentials"}, status=400)
            except User.DoesNotExist:
                return Response({"error": "User does not exist"}, status=404)
        return Response(serializer.errors, status=400)