from django.shortcuts import render
from .models import Game
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

    # 사용자가 공격자(attacker) 또는 수비자(defender)로 참여한 모든 게임 조회
    # 사용자가 참여한 모든 게임 (오래된 순으로 정렬)
    games = Game.objects.filter(attacker=user) | Game.objects.filter(defender=user)
    games = games.order_by('created_at')  # 오래된 순 정렬

    # 게임 ID와 인덱스 매핑
    games_with_index = [
        {"index": idx + 1, "game": game}
        for idx, game in enumerate(games)
    ]

    # 템플릿에 모델 인스턴스를 직접 전달
    return render(request, "users/list.html", {
        "user": user,               # 현재 사용자 정보
        "games_with_index": games_with_index  # 인덱스와 게임 모델 포함
    })


# 게임 정보
@login_required
def user_game_data(request, game_id):
    user = request.user  # 현재 로그인된 사용자

    # 사용자가 참여한 모든 게임 (오래된 순으로 정렬)
    games = Game.objects.filter(attacker=user) | Game.objects.filter(defender=user)
    games = games.order_by('created_at')  # 오래된 순 정렬

    # 게임 ID와 인덱스 매핑
    games_with_index = [
        {"index": idx + 1, "game": game}
        for idx, game in enumerate(games)
    ]

    # 요청된 게임 데이터와 인덱스 가져오기(딕셔너리)
    game_data = next((item for item in games_with_index if item["game"].id == game_id), None)


    # 게임 객체와 인덱스 추출
    game = game_data["game"]
    game_index = game_data["index"]

    # 템플릿 결정
    if game.status == "finished":
        template = "games/finished_attack.html"
    else:
        if game.attacker == user:
            template = "games/delete_attack.html"
        else:
            template = "games/counter_attack.html"

    # 데이터 전달
    context = {
        "user": user,             # 현재 사용자 정보
        "game": game,             # 요청된 게임 객체
        "index": game_index,      # 요청된 게임의 인덱스
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
