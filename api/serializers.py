from rest_framework import serializers
from api.models import Category, Food, Complaint, Delivery


class CategorySerializer(serializers.ModelSerializer):
    # restaurant = MeSerializer()
    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'restaurant_id']

    def save(self, user=None, **kwargs):
        category = Category(
            restaurant_id=user.id,
            name_uz=self.validated_data['name_uz'],
            name_ru=self.validated_data['name_ru'],
            name_en=self.validated_data['name_en']
        )
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name_uz = validated_data.get('name_uz', instance.name_uz)
        instance.name_ru = validated_data.get('name_ru', instance.name_ru)
        instance.name_en = validated_data.get('name_en', instance.name_en)
        instance.save()
        return instance


class FoodsSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ['id', 'restaurant_id', 'category_id', 'title_uz', 'title_ru', 'title_en', 'subtitle_uz',
                  'subtitle_ru', 'subtitle_en', 'price', 'photo', 'order', 'is_active']

    def get_photo(self, food):
        try:
            request = self.context.get('request')
            photo_url = food.photo.url
            return request.build_absolute_uri(photo_url)
        except:
            pass


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'category_id', 'title_uz', 'title_ru', 'title_en', 'subtitle_uz',
                  'subtitle_ru', 'subtitle_en', 'price', 'photo', 'order', 'is_active']
        extra_kwargs = {
            'photo': {'read_only': True}
        }

    def save(self, user, request, **kwargs):
        food = Food(
            restaurant_id=user.id,
            category_id=request.data['category_id'],
            title_uz=self.validated_data['title_uz'],
            title_ru=self.validated_data['title_ru'],
            title_en=self.validated_data['title_en'],
            subtitle_uz=self.validated_data['subtitle_uz'],
            subtitle_ru=self.validated_data['subtitle_ru'],
            subtitle_en=self.validated_data['subtitle_en'],
            price=self.validated_data['price'],
            photo=request.data['photo'],
            order=self.validated_data['order'],
            is_active=self.validated_data['is_active']
        )
        food.save()
        return food

    def update(self, instance, validated_data):
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.title_uz = validated_data.get('title_uz', instance.title_uz)
        instance.title_ru = validated_data.get('title_ru', instance.title_ru)
        instance.title_en = validated_data.get('title_en', instance.title_en)
        instance.subtitle_uz = validated_data.get('subtitle_uz', instance.subtitle_uz)
        instance.subtitle_ru = validated_data.get('subtitle_ru', instance.subtitle_ru)
        instance.subtitle_en = validated_data.get('subtitle_en', instance.subtitle_en)
        instance.price = validated_data.get('price', instance.price)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.order = validated_data.get('order', instance.order)
        if validated_data.get('is_active') == 'true':
            instance.is_active = True
        elif validated_data.get('is_active') == 'false':
            instance.is_active = False
        else:
            instance.is_active = instance.is_active
        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

    # def save(self, request, **kwargs):
    #     complaint = Complaint(
    #         restaurant_id=request.user.id,
    #         full_name=self.validated_data['full_name'],
    #         phone=self.validated_data['phone'],
    #         message=self.validated_data['message']
    #     )
    #     complaint.save()
    #     return complaint


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['restaurant_id', 'food', 'full_name', 'phone',
                  'address', 'message', 'type', 'sana']
        extra_kwargs = {
            'sana': {'read_only': True},
            'message': {'read_only': True}
        }

    def save(self, request, **kwargs):
        delivery = Delivery(
            restaurant_id=request.data['restaurant_id'],
            food=self.validated_data['food'],
            full_name=self.validated_data['full_name'],
            phone=self.validated_data['phone'],
            address=self.validated_data['address'],
            message=request.data['message'],
            type=self.validated_data['type']
        )
        delivery.save()
        return delivery
