from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(models.Model):
    user_name = models.CharField('사용자 이름',max_length=50)
    user_password = models.CharField('비밀번호',max_length=50)
    user_score = models.IntegerField('사용자 점수',default=0)

