from django.urls import path
from .views import generate_cards

urlpatterns = [
    path('generate-cards/<int:game_id>/', generate_cards, name='generate_cards'),
]
