from django.urls import path, include
from games import views

app_name = "games"

urlpatterns = [

    path('startgame/', views.game_start, name='game_start'),
    path('game_list/', views.user_game_list, name='user_game_list'), 
    path('game/<int:game_id>/', views.user_game_data, name='user_game_data'), 
    path('startgame/game_list/', views.user_game_list, name='user_game_list'), 
    path('ranking/', views.user_ranking, name='user_ranking'), #랭킹
    path('game/defense/<int:game_id>/', views.game_defense, name='game_defense'),
    path('game/delete/<int:game_id>/', views.game_delete, name='game_delete'),
    #path('game/<int:game_id>/result/', views.calculate_result, name='calculate_result'), #결과

]

