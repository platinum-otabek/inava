from rest_framework import serializers

from account.models import CustomUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)


# Restoran
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    slug_name = serializers.SlugField(default='slug')

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'name', 'user_id', 'slug_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, user, **kwargs):
        if self.validated_data['slug_name'] == 'slug':
            customuser = CustomUser(
                username=self.validated_data['username'],
                name=self.validated_data['name'],
                user_id=user.id,
                is_restaurant=True,
                slug_name=self.validated_data['username']
            )
        else:
            customuser = CustomUser(
                username=self.validated_data['username'],
                name=self.validated_data['name'],
                user_id=user.id,
                is_restaurant=True,
                slug_name=self.validated_data['slug_name']
            )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'data': 'Parollar bir xil emas'})
        customuser.set_password(password)
        customuser.save()
        return customuser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            "username": {
                'required': False
            },
            "password": {
                'required': False
            }
        }


class MeSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = '__all__'

    def get_logo(self, restaurant):
        try:
            request = self.context.get('request')
            logo_url = restaurant.logo.url
            return request.build_absolute_uri(logo_url)
        except:
            pass


class RestaurantSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'main_language', 'name', 'description', 'currency', 'location', 'is_calculation', 'logo', 'date_joined', 'slug_name']

    def get_logo(self, restaurant):
        try:
            request = self.context.get('request')
            logo_url = restaurant.logo.url
            return request.build_absolute_uri(logo_url)
        except:
            pass


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=4, max_length=50, error_messages={
            "min_length": "Parol kamida 4 ta belgidan iborat bo'lishi lozim.",
            "max_length": "Parol ko'pi bilan 50 ta belgidan iborat bo'lishi mumkin."
        })
    confirm_password = serializers.CharField(required=True, min_length=4, max_length=50, error_messages={
            "min_length": "Parol kamida 4 ta belgidan iborat bo'lishi lozim.",
            "max_length": "Parol ko'pi bilan 50 ta belgidan iborat bo'lishi mumkin."
        })

    def validate(self, data):
        errors = {}
        if not self.context['request'].user.check_password(data.get('old_password')):
            errors['old_password'] = "Parol noto'g'ri kiritilgan."

        if data.get('new_password') != data.get('confirm_password'):
            errors['confirm_password'] = "Parollar bir xil bo'lishi shart."

        if data.get('new_password') == data.get('old_password'):
            errors['new_password'] = "Parol hozirgi parol bilan bir xil."

        if errors:
            raise serializers.ValidationError(errors)

        return data
