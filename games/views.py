from django.shortcuts import render, redirect
import random
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.decorators import login_required
from users.models import User
from games.models import Game

def game_start(request):
    if request.method == "POST":
        # 폼에서 전송된 데이터 가져오기
        card_number = request.POST.get("card_number")  # 선택된 카드 번호
        choice_defender = request.POST.get("choice_defender")  # 선택된 Defender ID
        mylist  = [
        'high', 'Higher number wins',  # 숫자가 큰 카드가 승리
        'low', 'Lower number wins',   # 숫자가 작은 카드가 승리
        ]
        wc = random.choice (mylist)
        attacker = request.user
        defender = User.objects.get(id = choice_defender)

        new_game = Game(status = 'waiting', attacker_card = int(card_number), attacker = attacker, defender = defender, 
                        winning_condition = wc, winner = None, defender_card = None)
        new_game.save()
        return 
    attacker = request.user
    defender = User.objects.exclude(id=attacker.id)
    ctx = {
        'attacker' : attacker,
        'defender' : defender,
    }
    return render(request,'games/game_attack.html', ctx)

def game_list(request):
    attacker = request.user
    attacker_game = Game.models.filter(attacker = attacker.id)
    defender_game = Game.models.filter(defender = attacker.id)

