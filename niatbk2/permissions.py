from rest_framework.permissions import BasePermission


class AddRestaurantPermission(BasePermission):
    def has_permission(self, request, view):
        return True