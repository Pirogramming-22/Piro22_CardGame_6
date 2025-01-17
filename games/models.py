from django.db import models
from django.conf import settings  # AUTH_USER_MODEL 사용을 위해 import

class Game(models.Model):
    """
    게임 자체를 나타내는 모델. 한 번의 게임을 정의.
    """
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),  # 대기 중
        ('finished', 'Finished'),  # 게임 종료
    ]
    
    WINNING_CONDITION_CHOICES = [
    ('high', 'Higher number wins'),  # 숫자가 큰 카드가 승리
    ('low', 'Lower number wins'),   # 숫자가 작은 카드가 승리
    ]

    attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='initiated_games',
        on_delete=models.CASCADE,
        default=None
    )
    defender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='received_games',
        on_delete=models.CASCADE
    )
    
    attacker_card = models.IntegerField(default=0)
    defender_card = models.IntegerField(null=True, blank=True)
    winning_condition = models.CharField(max_length=10, choices=WINNING_CONDITION_CHOICES, default='high')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='won_games',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    
    def __str__(self):
        return f"Game between {self.attacker} and {self.defender}"

    
