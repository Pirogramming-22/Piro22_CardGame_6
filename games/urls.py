from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('game_list/', views.user_game_list, name='user_game_list'), 
    path('game/<int:game_id>/', views.user_game_data, name='user_game_data'), 
    
    path('ranking/', views.user_ranking, name='user_ranking'), #랭킹
    
    path('game/<int:game_id>/result/', views.calculate_result, name='calculate_result'), #결과

]