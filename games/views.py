from django.shortcuts import render

def game_main(request):
    context = {
        'data': 'hello!',
    }
    return render(request, 'games/game_defense.html', context)