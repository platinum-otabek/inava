from django.urls import path

from account.views import LoginView, RegisterView, ChangePasswordView, ProfileView, MeView, RestaurantView, \
    RestaurantsView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('me/', MeView.as_view()),
    path('restaurant/<str:slug>/', RestaurantView.as_view()),
    path('restaurants/', RestaurantsView.as_view())
]