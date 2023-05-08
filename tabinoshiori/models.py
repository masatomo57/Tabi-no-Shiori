from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Trip(models.Model):
    title = models.CharField(max_length=100, verbose_name="旅行タイトル")
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー", related_name='username_trip')
    start_date = models.DateField(verbose_name='出発日')
    end_date = models.DateField(verbose_name='帰宅日')
    comment = models.TextField(verbose_name='コメント')
    is_public = models.BooleanField(verbose_name="公開の可不可")
    def __str__(self):
        return self.title
    
class Itinerary(models.Model):
    title = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="旅行タイトル", related_name="title_itinerary")
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー", related_name='username_itinerary')
    action = models.CharField(max_length=100, verbose_name="行動")
    date = models.DateField(verbose_name="日付")
    start_time = models.TimeField(verbose_name="開始時間")
    end_time = models.TimeField(verbose_name="終了時間")
    def __str__(self):
        return self.action