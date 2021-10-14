from django.urls import path

from api.views import CategoryView, CategoriesView, FoodsView, FoodView, FoodByCategoryView, ComplaintView, DeliveryView

urlpatterns = [
    path('categories/<int:restaurant_id>/', CategoriesView.as_view()),
    path('category/', CategoryView.as_view()),
    path('category/<int:pk>/', CategoryView.as_view()),
    path('foods/<int:restaurant_id>/', FoodsView.as_view()),
    path('foods/<int:restaurant_id>/<int:category_id>/', FoodsView.as_view()),
    path('food/', FoodView.as_view()),
    path('food/<int:pk>/', FoodView.as_view()),
    path('food/category/<int:pk>/', FoodByCategoryView.as_view()),
    path('complaint/', ComplaintView.as_view()),
    path('delivery/', DeliveryView.as_view())
]
