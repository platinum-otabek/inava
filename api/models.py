import datetime

from django.db import models

from account.models import CustomUser


class Category(models.Model):
    restaurant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)

    def __str__(self):
        return self.name_uz


class Food(models.Model):
    restaurant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title_uz = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    subtitle_uz = models.TextField()
    subtitle_ru = models.TextField()
    subtitle_en = models.TextField()
    price = models.IntegerField()
    photo = models.ImageField(upload_to=f'food/{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)


class Complaint(models.Model):
    restaurant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    message = models.TextField(max_length=200)
    sana = models.DateTimeField(auto_now_add=True)


class Delivery(models.Model):
    choices = [
        ('Uy', 'Uyga yetkazish'),
        ('Stol', 'Stolga buyurtma berish')
    ]
    restaurant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food = models.JSONField()
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    message = models.TextField(max_length=200)
    type = models.CharField(max_length=10, choices=choices, default='Stol')
    sana = models.DateTimeField(auto_now_add=True)
