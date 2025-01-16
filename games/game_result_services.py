from django.db import transaction
from .models import Game, Card, GameResult
from django.contrib.auth import get_user_model

User = get_user_model()

def calculate_game_result(game_id):
    """
    게임 결과를 계산하고 저장하는 함수
    """
    # 게임과 카드 정보 가져오기
    game = Game.objects.get(id=game_id)
    player1_card = Card.objects.get(game=game, player=game.player1)
    player2_card = Card.objects.get(game=game, player=game.player2)

    # 승리 조건에 따라 결과 계산
    winner = None
    loser = None
    draw = False

    if game.winning_condition == 'high':
        if player1_card.number > player2_card.number:
            winner = game.player1
            loser = game.player2
        elif player1_card.number < player2_card.number:
            winner = game.player2
            loser = game.player1
        else:
            draw = True
    elif game.winning_condition == 'low':
        if player1_card.number < player2_card.number:
            winner = game.player1
            loser = game.player2
        elif player1_card.number > player2_card.number:
            winner = game.player2
            loser = game.player1
        else:
            draw = True

    # 결과 저장
    with transaction.atomic():
        GameResult.objects.create(
            game=game, winner=winner, loser=loser, draw=draw
        )
        game.status = 'finished'
        game.save()

     # 점수 업데이트
    if not draw:
        update_player_scores(game.id)
        
    # 결과 반환
    return {
        "status": "success",
        "winner": winner.nickname if winner else "None",
        "loser": loser.nickname if loser else "None",
        "draw": draw
    }


# 점수 업데이트
def update_player_scores(game_id):
    # 게임 결과 가져오기
    result = GameResult.objects.get(game_id=game_id)
    if result.draw:
        return {"status": "success", "message": "Draw: No score updates"}
    
    # 승자와 패자 카드 정보 가져오기
    winner_card = Card.objects.get(game=result.game, player=result.winner)
    loser_card = Card.objects.get(game=result.game, player=result.loser)

    # 점수 업데이트
    result.winner.user_score += winner_card.number
    result.loser.user_score -= loser_card.number

    # 저장
    result.winner.save()
    result.loser.save()

    return {
        "status": "success",
        "winner_score": result.winner.user_score,
        "loser_score": result.loser.user_score,
    }