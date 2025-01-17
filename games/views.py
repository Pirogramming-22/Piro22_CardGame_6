from django.shortcuts import render

def game_main(request):
    context = {
        'data': 'hello!',
    }
<<<<<<< HEAD
    return render(request, 'games/delete_attack.html', context)
=======
    return render(request, 'games/game_defense.html', context)
>>>>>>> 00d6a8eafe8fd5eecb23b9a7f7d254846b3f8f43
