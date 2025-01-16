from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Game(models.Model):
    attacker_id = models.ForeignKey(User, verbose_name="공격자 아이디", on_delete=models.CASCADE)
    defender_id = models.ForeignKey(User, verbose_name="방어자 아이디", on_delete=models.CASCADE)
    game_result = models.IntegerField('게임 결과',default=0)
    attacker_chosen_card = models.IntegerField('공격자 카드',[MinValueValidator(1), MaxValueValidator(9)])
    defender_chosen_card = models.IntegerField('방어자 카드',[MinValueValidator(1), MaxValueValidator(9)])