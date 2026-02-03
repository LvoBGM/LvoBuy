from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "bets/index.html")

def login_view(request):
    return render(request, "bets/login.html")

def logout_view(request):
    ...

def register_view(request):
    return render(request, "register.html"),