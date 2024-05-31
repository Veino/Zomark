from django.shortcuts import render
from .models import ZomarkUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserRegistrationSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(["POST"])
def register(request):
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = "Account Created"
            data['email'] = account.email
        else:
            data = serializer.errors
        
        return Response(data)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def updateAccount(request, uid):
    if request.method == 'POST':
        data = request.data
        user = ZomarkUser.objects.get(id=uid)

        if 'image' in data:
            user.image = data['image']

        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    print(request.user)
    return Response({'message' : 'Success'})