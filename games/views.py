from django.shortcuts import render, get_object_or_404
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
    

# 게임 목록
@login_required
def user_game_list(request):
    user = request.user  # 현재 로그인된 사용자

    # 사용자가 플레이한 모든 게임 조회
    games = Game.objects.filter(player1=user) | Game.objects.filter(player2=user)
    games = games.order_by('-created_at')  # 최신순 정렬

    # 게임 데이터를 처리
    game_data = []
    for game in games:
        opponent = game.player2 if game.player1 == user else game.player1

        # 결과 확인
        try:
            result = game.result
            if result.draw:
                game_user_result = "Draw"
                game_opponent_result = "Draw"
            elif result.winner == user:
                game_user_result = "Win"
                game_opponent_result = "Lose"
            else:
                game_user_result = "Lose"
                game_opponent_result = "Win"
        except GameResult.DoesNotExist:
            game_user_result = "Pending"
            game_opponent_result = "Pending"

        # 게임 데이터 추가
        game_data.append({
            "game_id": game.id,
            "opponent": opponent.username,
            "user_result": game_user_result,
            "opponent_result": game_opponent_result,
            "status": game.status,  # 게임 상태 추가
        })

    # 템플릿에 데이터 전달
    return render(request, "users/list.html", {
        "user": user,           # 현재 사용자 정보
        "game_data": game_data,  # 게임 목록
    })

# 게임 정보
@login_required
def user_game_data(request, game_id):
    """
    게임 상태에 따라 다른 템플릿으로 연결
    """
    # 게임 객체 가져오기
    game = get_object_or_404(Game, id=game_id)

    # 상태에 따른 템플릿 분기
    if game.status == "waiting":
        template = "games/delete_attack.html"
    elif game.status == "ongoing":
        template = "games/counter_attack.html"
    else: # game.status == "finished":
        template = "games/finished_attack.html"
    
    # 데이터 전달
    context = {
        "game_id": game.id,
        "player1": game.player1.username,
        "player2": game.player2.username,
        "status": game.status,
    }

    return render(request, template, context)
        

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
    return render(request, "games/ranking.html", {"ranking_data": ranking_data})

