from django.urls import path

from . import views

urlpatterns = [
    path("", views.bets_root, name="root"),
    path("home", views.home, name="home"),
    path("home/<int:page_number>", views.home_specific_page, name="home_specific_page"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("new-listing", views.new_listing, name="new_listing"),
    path("account/<str:username>/", views.account, name="account"),
    path("account/<str:username>/listings/<int:page_number>", views.account_listings, name="account_listings"),
    path("listing/<int:id>", views.listing, name="listing"),
]
