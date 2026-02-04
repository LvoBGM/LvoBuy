from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    return render(request, "bets/index.html", {
        "authenticated": request.user.is_authenticated
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "bets/login.html", {
                "message": "Invalid Credentials",
            })


    return render(request, "bets/login.html")

def logout_view(request):
    logout(request)
    return redirect("index")

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = UserCreationForm()
    
    return render(request, "bets/register.html", {
        "form": form,
    })