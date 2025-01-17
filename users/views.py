from django.shortcuts import render

def card_main(request):
    context = {
        'data': 'hello!',
    }
    return render(request, 'users/login.html', context)