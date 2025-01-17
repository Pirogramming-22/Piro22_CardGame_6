from django.urls import path, include
from games import views

app_name = "games"

urlpatterns = [
  path('startgame/', views.game_start, name='game_start'),
]
