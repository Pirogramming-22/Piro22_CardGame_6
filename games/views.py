from django.shortcuts import render
from .models import Game, Card, GameResult
from django.http import JsonResponse
from .game_result_services import calculate_game_result
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required  # 로그인된 사용자만 접근할 수 있도록 제한
User = get_user_model()

# Create your views here.

# 게임 결과
def calculate_result(request, game_id):
    if request.method == "POST":
        result = calculate_game_result(game_id)
        return JsonResponse(result) #결과 : 딕셔너리 형식(JSON)
    else:
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
    
    
# 랭킹
def user_ranking(request):
    if request.method == "GET":
        # 모든 사용자를 점수 기준으로 정렬 (내림차순)
        users = User.objects.order_by('-user_score', 'id') # 점수 같을 경우, id순
        top_users = users[:3] # 상위 3명
        
        ranking_data = [
            {
                "rank": index + 1,
                "username": user.username,
                "nickname": user.nickname,
                "user_score": user.user_score,
            }
            for index, user in enumerate(top_users)
        ]
    return JsonResponse({"status": "success", "ranking": ranking_data})


# 게임 전적 조회
@login_required
def user_game_history(request):
    user = request.user # 현재 로그인된 사용자
    
    # 사용자가 플레이한 모든 게임 가져오기
    games = Game.objects.filter(player1=user) | Game.objects.filter(player2=user)
    games = games.order_by('-created_at')  # 최신순 정렬
    
    game_data = []
    for game in games:
        
        # 상대 플레이어 결정
        opponent = game.player2 if game.player1 == user else game.player1
        
        # 결과 확인
        # game.result: Game 모델의 related_name='result'을 통해 연결된 GameResult 객체를 가져옴
        try:
            result = game.result  # GameResult 객체
            if result.draw:
                game_result = "Draw"
            elif result.winner == user:
                game_result = "Win"
            else:
                game_result = "Lose"
        except GameResult.DoesNotExist:
            game_result = "Pending"  # 결과가 없는 경우
            
        game_data.append({
            "game_id": game.id,
            "opponent": opponent.username,
            "status": game.status,
            "result": game_result,
        })

    return JsonResponse({"status": "success", "games": game_data})
                
        