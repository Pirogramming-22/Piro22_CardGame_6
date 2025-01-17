from django.shortcuts import render, redirect
import random
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.decorators import login_required
from users.models import User
from games.models import Game
from django.http import JsonResponse
from .game_result_services import calculate_game_result
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
User = get_user_model()

@login_required
def game_start(request):
    if request.method == "POST":
        # 폼에서 전송된 데이터 가져오기
        card_number = request.POST.get("card_number")  # 선택된 카드 번호
        choice_defender = request.POST.get("choice_defender")  # 선택된 Defender ID
        mylist  = [
        'high',  # 숫자가 큰 카드가 승리
        'low',   # 숫자가 작은 카드가 승리
        ]
        wc = random.choice (mylist)
        attacker = request.user
        defender = User.objects.get(id = choice_defender)

        new_game = Game(status = 'waiting', attacker_card = int(card_number), attacker = attacker, defender = defender, 
                        winning_condition = wc, winner = None, defender_card = None)
        new_game.save()
        return redirect('game_list/')
    attacker = request.user
    defender = User.objects.exclude(id=attacker.id)
    ctx = {
        'attacker' : attacker,
        'defender' : defender,
    }
    return render(request,'games/game_attack.html', ctx)

'''def calculate_result(request, game_id):
    if request.method == "POST":
        result = calculate_game_result(game_id)
        return JsonResponse(result) #결과 : 딕셔너리 형식(JSON)
    else:
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)'''
    
#def game_result(request, game_id):
'''
def game_defense(request, game_id):
    #print(request.get_full_path())
        if request.method == "POST":
        # 폼에서 전송된 데이터 가져오기
        card_number = request.POST.get("card_number")  # 선택된 카드 번호
        game = Game.objects.get(id=game_id)
        game.defender_card = int(card_number)
        game.status = "finished"
        game.save()
        result = calculate_game_result(game_id)
        return redirect('games:game_list/')
    
    game = Game.objects.get(id=game_id)
    ctx = {
        'game_id' : game_id
    }
    return render(request,'games/game_defense.html', ctx)'''

def game_defense(request, game_id):
    # 특정 게임 객체 가져오기
    game = get_object_or_404(Game, id=game_id)

    # POST 요청 처리 (추후 활성화 가능)

    if request.method == "POST":
        card_number = request.POST.get("card_number")
        game.defender_card = int(card_number)
        game.status = "finished"
        game.save()
        result = calculate_game_result(game_id)
        return redirect('games:user_game_list')
    

    # 템플릿에 게임 객체 전달
    ctx = {
        'game': game  # 게임 객체 전체를 전달
    }
    return render(request, 'games/game_defense.html', ctx)


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
                #"nickname": user.nickname,
                "user_score": user.user_score,
            }
            for index, user in enumerate(top_users)
        ]
    return render(request, "games/ranking.html", {"ranking_data": ranking_data})


def game_delete(request, game_id):
    game = Game.objects.get(id = game_id)
    game.delete()
    return redirect('games:user_game_list')
