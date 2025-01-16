import random
from django.http import JsonResponse
from django.shortcuts import render
from .models import Game, Card

# 1. 게임 생성
def start_game(request):
    """
    새로운 게임을 생성하는 API
    """
    if request.method == 'POST':
        try:
            player1 = request.user
            player2_id = request.POST.get('player2_id')
            player2 = User.objects.get(id=player2_id)

            # 랜덤으로 'high' 또는 'low' 결정
            winning_condition = random.choice(['high', 'low'])

            # 새로운 게임 생성
            game = Game.objects.create(
                player1=player1,
                player2=player2,
                winning_condition=winning_condition
            )

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
    """
    랜덤으로 5장의 카드를 생성하여 게임과 연관된 카드로 저장.
    """
    if request.method == 'POST':  # POST 요청만 허용
        try:
            # 게임과 요청한 사용자 가져오기
            game = Game.objects.get(id=game_id)
            player = request.user

            # 이미 카드가 생성된 경우 에러 반환
            if Card.objects.filter(game=game, player=player).exists():
                return JsonResponse({'error': 'Cards already generated for this player.'}, status=400)

            # 랜덤한 5개의 숫자 생성
            numbers = random.sample(range(1, 11), 5)
            cards = []
            for number in numbers:
                # 카드 생성 및 저장
                card = Card.objects.create(game=game, player=player, number=number)
                cards.append(card.number)

            # 생성된 카드 반환
            return JsonResponse({'cards': cards}, status=200)

        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# 3. 게임 상태 업데이트
def update_game_status(request, game_id):
    """
    게임 상태를 업데이트하는 API
    """
    if request.method == 'POST':  # POST 요청만 허용
        try:
            # 게임 가져오기
            game = Game.objects.get(id=game_id)

            # 클라이언트가 보낸 새로운 상태 가져오기
            new_status = request.POST.get('status')

            # 유효한 상태 값인지 확인
            valid_statuses = ['waiting', 'ongoing', 'finished']
            if new_status not in valid_statuses:
                return JsonResponse({'error': 'Invalid status value.'}, status=400)

            # 상태 변경
            game.status = new_status
            game.save()

            # 성공적으로 변경된 상태 반환
            return JsonResponse({
                'game_id': game.id,
                'new_status': game.status
            }, status=200)

        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# 4. 승패 판단 로직
def determine_winner(game_id, card_player1, card_player2):
    """
    게임 ID와 양쪽 플레이어가 선택한 카드를 바탕으로 승패를 판단.
    """
    try:
        # 게임 정보 가져오기
        game = Game.objects.get(id=game_id)

        # 승리 조건 확인
        winning_condition = game.winning_condition

        # 승패 판정
        if winning_condition == 'high':
            # 높은 카드가 승리
            if card_player1 > card_player2:
                winner = game.player1
                loser = game.player2
            elif card_player1 < card_player2:
                winner = game.player2
                loser = game.player1
            else:
                winner = None  # 무승부
                loser = None
        elif winning_condition == 'low':
            # 낮은 카드가 승리
            if card_player1 < card_player2:
                winner = game.player1
                loser = game.player2
            elif card_player1 > card_player2:
                winner = game.player2
                loser = game.player1
            else:
                winner = None  # 무승부
                loser = None

        return winner, loser

    except Game.DoesNotExist:
        raise ValueError("Game not found.")


# 5. 게임 승패와 상태 처리
def process_turn(request, game_id):
    """
    한 턴의 결과를 처리하고, 게임 상태를 업데이트.
    """
    if request.method == 'POST':
        try:
            # 게임 정보 가져오기
            game = Game.objects.get(id=game_id)

            # 플레이어1과 플레이어2의 선택된 카드 가져오기
            card_player1 = int(request.POST.get('card_player1'))
            card_player2 = int(request.POST.get('card_player2'))

            # 승패 판단
            winner, loser = determine_winner(game.id, card_player1, card_player2)

            if winner:
                # 결과 저장 (Game 상태 업데이트)
                game.status = 'finished'
                game.save()

                # 결과 반환
                return JsonResponse({
                    'game_id': game.id,
                    'winner': winner.username,
                    'loser': loser.username
                }, status=200)
            else:
                # 무승부 처리
                return JsonResponse({'message': 'It\'s a tie!'}, status=200)

        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
