from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Game(models.Model):
    attacker = models.ForeignKey(
        User, 
        verbose_name="공격자", 
        on_delete=models.CASCADE, 
        related_name="attacker_games"
    )
    defender = models.ForeignKey(
        User, 
        verbose_name="방어자", 
        on_delete=models.CASCADE, 
        related_name="defender_games"
    )
    game_result = models.IntegerField(
        verbose_name="게임 결과", 
        default=0
    )
    attacker_chosen_card = models.IntegerField(
        verbose_name="공격자가 선택한 카드", 
        validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    defender_chosen_card = models.IntegerField(
        verbose_name="방어자가 선택한 카드", 
        validators=[MinValueValidator(1), MaxValueValidator(9)]
    )

    class Meta:
        verbose_name = "게임"
        verbose_name_plural = "게임들"
        ordering = ["-id"]

    def __str__(self):
        return f"Game {self.id}: {self.attacker} vs {self.defender}"