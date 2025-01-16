import random
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Game, Card

User = get_user_model()

# 1. 게임 생성
def start_game(request):
    if request.method == 'POST':
        try:
            player1 = request.user
            player2_id = request.POST.get('player2_id')
            player2 = User.objects.get(id=player2_id)

            # 새로운 게임 생성
            game = Game.objects.create(player1=player1, player2=player2)

            return JsonResponse({
                'game_id': game.id,
                'player1': player1.username,
                'player2': player2.username,
                'status': game.status,
                'winning_condition': game.winning_condition,
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Player2 does not exist.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# 2. 카드 생성
def generate_cards(request, game_id):
    if request.method == 'POST':
        try:
            game = Game.objects.get(id=game_id)
            player = request.user

            # 이미 생성된 카드가 있는지 확인
            if Card.objects.filter(game=game, player=player).exists():
                return JsonResponse({'error': 'Cards already generated for this player.'}, status=400)

            # 랜덤 카드 생성
            numbers = random.sample(range(1, 11), 5)
            cards = []
            for number in numbers:
                card = Card.objects.create(game=game, player=player, number=number)
                cards.append(card.number)

            return JsonResponse({'cards': cards}, status=200)

        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# 3. 게임 상태 업데이트
def update_game_status(request, game_id):
    if request.method == 'POST':
        try:
            game = Game.objects.get(id=game_id)
            new_status = request.POST.get('status')

            # 상태 변경 검증
            valid_statuses = ['waiting', 'ongoing', 'finished']
            if new_status not in valid_statuses:
                return JsonResponse({'error': 'Invalid status value.'}, status=400)

            game.status = new_status
            game.save()

            return JsonResponse({'game_id': game.id, 'status': game.status}, status=200)

        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
