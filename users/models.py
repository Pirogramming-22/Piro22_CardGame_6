from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=10, null=True, verbose_name="이름")
    email = models.EmailField(unique=True, verbose_name="이메일")
    #nickname = models.CharField(max_length=20, null=True, verbose_name="닉네임")
    user_score = models.IntegerField(default=0, verbose_name="사용자 점수")

def __str__(self):
    return self.name

