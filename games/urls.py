from django.urls import path
from .views import *
urlpatterns = [
    path('game/<int:game_id>/result/', calculate_result, name='calculate_result'), #결과
    path('ranking/', user_ranking, name='user_ranking'), #랭킹
    path('history/', user_game_history, name='user_game_history'), # 전적
]
