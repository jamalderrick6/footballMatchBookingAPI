from django.urls import path, re_path, include

from game.views import CreateListTeamView, CreateListStadiumView, CreateListMatchView, MatchDetailView, \
    ListReservationsView, create_checkout_session, stripe_webhook, OrderListView, OrderDeleteView

game_urls = [
    path("teams", CreateListTeamView.as_view(), name="create and list teams"),
    path("stadiums", CreateListStadiumView.as_view(), name="create and list stadiums"),
    path("matches/<int:id>/reservations", ListReservationsView.as_view(), name="list reservations for a match"),
    path("matches", CreateListMatchView.as_view(), name="create and list matches"),
    re_path(r"^matches/(?P<id>[a-f0-9]{1,32})$", MatchDetailView.as_view(), name="view single match"),
    path('create-checkout-session', create_checkout_session, name='create-checkout-session'),
    path('stripe-webhook', stripe_webhook, name='stripe-webhook'),
    path('reservations', OrderListView.as_view(), name='get a list of reservation orders'),
    path('reservations/<str:order_id>/delete', OrderDeleteView.as_view(), name='delete a reservation order'),
]

urlpatterns = [
    re_path(r'^v1/', include(game_urls)),
]