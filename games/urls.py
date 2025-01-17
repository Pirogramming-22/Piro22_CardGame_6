from django.urls import path
from .views import start_game_page, process_attack

urlpatterns = [
    path('start/', start_game_page, name='start_game_page'),
    path('process-attack/', views.process_attack, name='process_attack'),
]
