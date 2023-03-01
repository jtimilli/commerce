from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>/", views.view_listing, name="listing"),
    path("watchlist/(?P<listing_id>\d+)?/", views.add_watchlist, name="watchlist"),
    path("watchlist/", views.go_watchlist, name="go_watchlist"),
    path("bid/<int:listing_id>", views.update_bid, name="bid"),
    path("close/<int:listing_id>", views.close_bid, name="close_bid"),
    path("categories/", views.categories, name="categories")
]