from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.
def index(request):
    return render(request, 'users/main.html')

def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            ctx = {'new_user': new_user}
            return render(request, 'registration/register_done.html', ctx)
    else:
        user_form = RegisterForm()
        ctx = {'form': user_form}
    return render(request, 'registration/register.html', ctx)
def card_main(request):
    context = {
        'data': 'hello!',
    }
    return render(request, 'users/list.html', context)