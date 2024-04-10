from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import (
    TyresListView,
    TyreDetails,
    BasketView,
    OrderView,
    SortingView,
    FiltrationView
)

app_name = "tyresapp"


urlpatterns = [
    path("", TyresListView.as_view(), name="tyres"),
    path("tyre_detail/<int:pk>/<int:tg_id>", TyreDetails.as_view(), name="tyre_details"),
    path("basket/<int:tg_id>/", BasketView.as_view(), name="basket"),
    path("order/<int:tg_id>", OrderView.as_view(), name="order"),
    path("sorting/", SortingView.as_view(), name="sorting"),
    path("filtration/", FiltrationView.as_view(), name="filtration")
]