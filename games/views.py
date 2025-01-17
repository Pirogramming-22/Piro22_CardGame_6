from django.shortcuts import render

def game_main(request):
    context = {
        'data': 'hello!',
    }
    return render(request, 'games/counter_attack.html', context)