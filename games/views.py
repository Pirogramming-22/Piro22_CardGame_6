from django.shortcuts import render, redirect
from django.http import JsonResponse
import random
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Game, Card

User = get_user_model()

# 1. Start 버튼 눌렀을 때 이동하는 화면
def start_game_page(request):
    if request.user.is_authenticated:
        # 랜덤 카드 5장 생성
        cards = random.sample(range(1, 11), 5)

        # 현재 사용자 제외한 디펜더 리스트
        defenders = User.objects.exclude(id=request.user.id)

        context = {
            'cards': cards,
            'defenders': defenders,
        }
        return render(request, 'games/game_attack.html', context)
    else:
        return redirect('account_login')

# 2. Attack 버튼 눌렀을 때 처리하는 로직
def process_attack(request):
    if request.method == 'POST':
        selected_card = request.POST.get('selected_card')  # 선택된 카드 번호
        defender_id = request.POST.get('defender')  # 선택된 수비자 ID

        # 현재 로그인된 사용자 (공격자)
        attacker = request.user

        # 수비자 정보 가져오기
        defender = User.objects.get(id=defender_id)  

        # 새로운 게임 생성
        game = Game.objects.create(
            player1=attacker,
            player2=defender,
            status='waiting',  # 초기 상태는 "waiting"
        )

        # 공격자의 카드 정보 저장
        Card.objects.create(
            game=game,
            player=attacker,
            number=selected_card
        )

        # 이전 게임 기록 가져오기
        all_games = Game.objects.all().order_by('-created_at')  # 최신 순으로 정렬


        # 게임 ID 및 기본 정보 전달
        context = {
            'game_id': game.id,
            'attacker': attacker,
            'defender': defender,
            'selected_card': selected_card,
            'games': all_games,
        }

        # 게임 리스트 화면 렌더링
        return render(request, 'users/list.html', context)

    # GET 요청일 경우 시작 페이지로 리다이렉트
    return redirect('start_game_page')
