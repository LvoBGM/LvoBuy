from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Max
from bets.models import Listing, Bid, Comments
from datetime import date


# Forms
class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "image_url", "starting_bid"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Listing Title'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Listing Description'})
        self.fields['image_url'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter An Image URL'})
        self.fields['starting_bid'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Starting Bid'})

class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Leave a comment...'
            }),
        }

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

def account(request, username):
    user = get_user_model().objects.filter(username=username).first()
    return render(request, "bets/account.html", {
        "authenticated": request.user.is_authenticated,
        "listings": user.listings.all(),
        "username": user.get_username(),
    })

def listing(request, id):
    queryset = Listing.objects.filter(id=id)
    bid_form = NewBidForm()
    comment_form = NewCommentForm()
    message = ""

    if queryset.exists():
        listing = queryset.first()
        comments = Comments.objects.filter(listing=listing)
        bids = listing.bids.all()
        if request.method == 'POST': #TODO: I think this needs to be redone, like if there are not bids the user should only have the option to bid the starting amount 

            # Bid Form
            if 'submit_bid' in request.POST:
                if not request.user.is_authenticated:
                    message = "You need to be logged in to bid!"
                    return render(request, "bets/listing.html", {
                        "authenticated": request.user.is_authenticated,
                        "listing": listing,
                        "message": message,
                        "bids": bids,
                        "comments": comments,
                    })

                bid_form = NewBidForm(request.POST)
                if bid_form.is_valid():
                    highest_bid = Bid.objects.filter(listing=listing).aggregate(Max('amount'))['amount__max']
                    bid = bid_form.save(commit=False)
                    bid.bidder = request.user
                    bid.listing = listing
                    # If bid is the highest bid or is the first bid with enough cash to go through
                    message = "You cannot outbid the highest bidder with such a low bid!"
                    if (highest_bid is not None and highest_bid < bid.amount) or (highest_bid is None and bid.amount >= int(listing.starting_bid)):
                        bid.save()
                        message = "You are now the highest bidder!"
                    return render(request, "bets/listing.html", {
                        "authenticated": request.user.is_authenticated,
                        "listing": listing,
                        "bid_form": bid_form,
                        "comment_form": comment_form,
                        "message": message,
                        "bids": bids,
                        "comments": comments,
                    })
            # Comment Form
            elif 'submit_comment' in request.POST:
                if not request.user.is_authenticated:
                    return render(request, "bets/listing.html", {
                        "authenticated": False,
                        "listing": listing,
                        "message": message,
                        "bids": bids,
                        "comments": comments,
                    })
                comment_form = NewCommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.commenter = request.user
                    comment.listing = listing
                    comment.date = date.today()

                    print("aaaaaaaaaaaaa")

                    comment.save()
                    return render(request, "bets/listing.html", {
                        "authenticated": request.user.is_authenticated,
                        "listing": listing,
                        "bid_form": bid_form,
                        "comment_form": NewCommentForm(),
                        "message": message,
                        "comments": comments,
                    })
    else:
        return redirect("index") # TODO: This should display a page not found error or smth
        
    return render(request, "bets/listing.html", {
        "authenticated": request.user.is_authenticated,
        "listing": listing,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "bids": bids,
        "comments": comments,
    })