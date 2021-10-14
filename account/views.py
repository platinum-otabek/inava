from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import password_changed
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import CustomUser
from account.serializers import LoginSerializer, CustomUserSerializer, RegisterSerializer, ChangePasswordSerializer, \
    ProfileSerializer, MeSerializer, RestaurantSerializer


class LoginView(APIView):
    permission_classes = (~IsAuthenticated,)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'ok': False,
                'data': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if user is None:
            return Response({
                'ok': False,
                'data': 'Foydalanuvchi topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'ok': True,
            'token': token.key,
            'user': CustomUserSerializer(user).data
        }, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'ok': False,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save(user=request.user)
        return Response({
            'ok': True,
            'data': CustomUserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({
            'ok': True,
            "user": ProfileSerializer(request.user, context={"request": request}).data
        })

    def put(self, request):
        serializer = ProfileSerializer(instance=request.user, data=request.data)
        if not serializer.is_valid():
            return Response({
                'ok': False,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            'ok': True,
            "user": serializer.data
        }, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({
            'ok': True,
            "user": MeSerializer(request.user, context={"request": request}).data
        })


class RestaurantView(APIView):
    def get(self, request, slug):
        restaurant = CustomUser.objects.get(slug_name=slug)
        if restaurant.is_restaurant == False:
            return Response({
                'ok': False,
                'data': 'Restoran emas'
            })
        return Response({
            'ok': True,
            'restaurant': RestaurantSerializer(restaurant).data
        })


class RestaurantsView(APIView):
    def get(self, request):
        restaurant = CustomUser.objects.filter(user_id=request.user.id, is_restaurant=True).order_by('-date_joined')
        return Response({
            'ok': True,
            'restaurants': RestaurantSerializer(restaurant, many=True).data
        })


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response({
                'ok': False,
                'data': serializer.errors
            }, status=status.HTTP_200_OK)

        user.set_password(serializer.validated_data.get("new_password"))
        user.save()

        password_changed(serializer.validated_data['new_password'], request.user)

        return Response({
            'ok': True,
            'data': "Parol o'zgardi"
        }, status=status.HTTP_200_OK)
