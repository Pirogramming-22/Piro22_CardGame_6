from django.db import models
from users.models import User
from django.db import models
from django.contrib.auth.models import User  # Django 기본 User 모델 사용

class Game(models.Model):
    """
    게임 자체를 나타내는 모델. 한 번의 게임을 정의.
    """
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),  # 게임 진행 중
        ('waiting', 'Waiting'),  # 상대방의 반격 대기 중
        ('finished', 'Finished'),  # 게임 종료
    ]

    player1 = models.ForeignKey(User, related_name='initiated_games', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='received_games', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game between {self.player1.username} and {self.player2.username}"


class Card(models.Model):
    """
    플레이어가 선택한 카드 정보를 저장하는 모델.
    """
    game = models.ForeignKey(Game, related_name='cards', on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()  # 1부터 10까지의 카드 숫자

    def __str__(self):
        return f"Card {self.number} by {self.player.username} in Game {self.game.id}"


class GameResult(models.Model):
    """
    게임의 결과를 저장하는 모델.
    """
    game = models.OneToOneField(Game, related_name='result', on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='won_games', on_delete=models.CASCADE, null=True, blank=True)
    loser = models.ForeignKey(User, related_name='lost_games', on_delete=models.CASCADE, null=True, blank=True)
    draw = models.BooleanField(default=False)  # 무승부 여부
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.draw:
            return f"Game {self.game.id}: Draw"
        return f"Game {self.game.id}: {self.winner.username} won against {self.loser.username}"
