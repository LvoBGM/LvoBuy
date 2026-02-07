from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from bets.models import Listing


# Forms
class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "image_url", "current_bid"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Listing Title'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Listing Description'})
        self.fields['image_url'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter An Image URL'})
        self.fields['current_bid'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Starting Bid'})

# Views
def index(request):
    return render(request, "bets/index.html", {
        "authenticated": request.user.is_authenticated,
        "listings": Listing.objects.all(),
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

@login_required() # TODO: Test if validation works even when a user posts an invalid request
def new_listing(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():

            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            
            return redirect("index")
    else:
        form = NewListingForm()

    return render(request, "bets/new_listing.html", {
        "authenticated": request.user.is_authenticated,
        "form": form
    })

@login_required()
def account(request):
    return render(request, "bets/account.html", {
        "authenticated": request.user.is_authenticated,
        "listings": request.user.listings.all(),
        "username": request.user.get_username(),
    })