from django.db import transaction
from .models import Game
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

#게임 결과를 계산하고 저장하는 함수
def calculate_game_result(game_id):

    # 게임 정보 가져오기
    game = get_object_or_404(Game, id=game_id)

    # 승리 조건에 따라 결과 계산
    winner = None
    loser = None
    draw = False

    if game.winning_condition == 'high':
        if game.attacker_card > game.defender_card:
            winner = game.attacker
            loser = game.defender
        elif game.attacker_card < game.defender_card:
            winner = game.defender
            loser = game.attacker
        else:
            draw = True
    elif game.winning_condition == 'low':
        if game.attacker_card < game.defender_card:
            winner = game.attacker
            loser = game.defender
        elif game.attacker_card > game.defender_card:
            winner = game.defender
            loser = game.attacker
        else:
            draw = True

    # 결과 저장
    with transaction.atomic():
        game.status = 'finished'
        game.winner = winner.id if winner else None
        game.save()

        # 점수 업데이트
        if not draw:
            update_player_scores(game.id)

    # 결과 반환
    return {
        "winner": winner.username if winner else "None",
        "loser": loser.username if loser else "None",
        "draw": draw
    }



# 점수 업데이트
def update_player_scores(game_id):
    # 게임 결과 가져오기
    game = Game.objects.get(id=game_id)
    
    # 승자, 패자, 카드 점수 가져오기
    if game.winner == game.attacker.id:
        winner, loser = game.attacker, game.defender
        winner_card_score, loser_card_score = game.attacker_card, game.defender_card
    else:
        winner, loser = game.defender, game.attacker
        winner_card_score, loser_card_score = game.defender_card, game.attacker_card

    # 점수 업데이트
    winner.user_score += winner_card_score
    loser.user_score -= loser_card_score

    # 저장
    winner.save()
    loser.save()

    return {
        "status": "success",
        "winner_score": winner.user_score,
        "loser_score": loser.user_score,
    }