from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Category, Food, Complaint, Delivery
from api.serializers import CategorySerializer, FoodSerializer, FoodsSerializer, ComplaintSerializer, DeliverySerializer


class CategoriesView(APIView):
    """
    Menuda ko'rinadi
    """

    def get(self, request, restaurant_id):
        queryset = Category.objects.filter(restaurant_id=restaurant_id)
        serializer = CategorySerializer(queryset, many=True)
        return Response({
            'ok': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class CategoryView(APIView):
    """
    Admin Panelda ko'rinadi
    """

    def get(self, request, pk=None):
        if pk is not None:
            try:
                object = Category.objects.get(id=pk)
                serializer = CategorySerializer(object)
                return Response({
                    'ok': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            except:
                return Response({
                    'ok': False,
                    'data': 'Obyekt topilmadi'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Category.objects.filter(restaurant_id=request.user.id)
            serializer = CategorySerializer(queryset, many=True)
            return Response({
                'ok': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'ok': True,
                'data': "Kategoriya muvaffaqiyatli qo'shildi"
            }, status=status.HTTP_201_CREATED)
        return Response({
            'ok': False,
            'data': serializer.errors
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            object = Category.objects.get(id=pk)
            serializer = CategorySerializer(object, data=request.data)
            if serializer.is_valid():
                serializer.update(object, request.data)
                return Response({
                    'ok': True,
                    'data': 'Category tahrirlandi'
                }, status=status.HTTP_200_OK)
            return Response({
                'ok': False,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'ok': False,
                'data': 'Obyekt topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            object = Category.objects.get(id=pk)
            object.delete()
            return Response({
                'ok': True,
                'data': "Kategoriya muvaffaqiyatli o'chirildi"
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'ok': False,
                'data': 'Obyekt topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)


class FoodsView(APIView):
    """
    Menuda ko'rinadi
    """

    def get(self, request, restaurant_id, category_id=None):
        queryset = Food.objects.filter(restaurant_id=restaurant_id, is_active=True).order_by('order')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        serializer = FoodsSerializer(queryset, many=True, context={"request": request})
        return Response({
            'ok': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class FoodView(APIView):
    """
    Admin Panelda ko'rinadi
    """

    def get(self, request, pk=None):
        queryset = Food.objects.filter(restaurant_id=request.user.id)
        if pk is not None:
            try:
                object = queryset.get(id=pk)
                serializer = FoodSerializer(object, context={"request": request})
                return Response({
                    'ok': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            except:
                return Response({
                    'ok': False,
                    'data': 'Obyekt topilmadi'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = FoodsSerializer(queryset, many=True, context={"request": request})
            return Response({
                'ok': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, request=request)
            return Response({
                'ok': True,
                'data': "Taom muvaffaqiyatli qo'shildi"
            }, status=status.HTTP_201_CREATED)
        return Response({
            'ok': False,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            object = Food.objects.get(id=pk)
            serializer = FoodSerializer(object, data=request.data)
            if serializer.is_valid():
                serializer.update(object, request.data)
                return Response({
                    'ok': True,
                    'data': 'Taom tahrirlandi'
                }, status=status.HTTP_200_OK)
            return Response({
                'ok': False,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'ok': False,
                'data': 'Obyekt topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            object = Food.objects.get(id=pk)
            serializer = FoodSerializer(object, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.partial_update(object, request.data)
                return Response({
                    'ok': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'ok': False,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'ok': False,
                'data': 'Obyekt topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            object = Food.objects.get(id=pk)
            object.delete()
            return Response({
                'ok': True,
                'data': "Taom muvaffaqiyatli o'chirildi"
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'ok': False,
                'data': 'Obyekt topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)

class FoodByCategoryView(APIView):
    def get(self, request, pk):
        queryset = Food.objects.filter(restaurant_id=request.user.id, category_id=pk)
        serializer = FoodsSerializer(queryset, many=True, context={"request": request})
        return Response({
            'ok': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class ComplaintView(APIView):
    def get(self, request):
        queryset = Complaint.objects.filter(restaurant_id=request.user.id).order_by('-sana')
        serializer = ComplaintSerializer(queryset, many=True)
        return Response({
            'ok': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'ok': True,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'ok': False,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DeliveryView(APIView):
    def get(self, request):
        queryset = Delivery.objects.filter(restaurant_id=request.user.id).order_by('-sana')
        print(queryset)
        serializer = DeliverySerializer(queryset, many=True)
        return Response({
            'ok': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response({
                'ok': True,
                'data': 'Buyurtma qabul qilindi'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'ok': False,
            'data': serializer.errors
        }, status=status.HTTP_200_OK)
