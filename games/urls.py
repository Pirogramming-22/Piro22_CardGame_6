from django.urls import path
from .views import start_game, generate_cards, update_game_status

urlpatterns = [
    path('start-game/', start_game, name='start_game'),
    path('generate-cards/<int:game_id>/', generate_cards, name='generate_cards'),
    path('update-game-status/<int:game_id>/', update_game_status, name='update_game_status'),
]
