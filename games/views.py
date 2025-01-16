from django.shortcuts import render
import random
from django.http import JsonResponse
from .models import Game, Card

def generate_cards(request, game_id):
    """
    랜덤으로 5장의 카드를 생성하여 게임과 연관된 카드로 저장.
    """
    try:
        # 특정 게임 가져오기
        game = Game.objects.get(id=game_id)
        player = request.user  # 요청을 보낸 유저를 플레이어로 설정

        # 이미 생성된 카드가 있다면 에러 반환
        if Card.objects.filter(game=game, player=player).exists():
            return JsonResponse({'error': 'Cards already generated for this player.'}, status=400)

        # 랜덤한 5개의 숫자 생성
        numbers = random.sample(range(1, 11), 5)

        # Card 모델에 생성된 숫자를 저장
        cards = []
        for number in numbers:
            card = Card.objects.create(game=game, player=player, number=number)
            cards.append(card.number)

        return JsonResponse({'cards': cards}, status=200)

    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found.'}, status=404)