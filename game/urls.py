from django.urls import path, re_path, include

from game.views import CreateListTeamView, CreateListStadiumView, CreateListMatchView, MatchDetailView

game_urls = [
    path("teams", CreateListTeamView.as_view(), name="create and list teams"),
    path("stadiums", CreateListStadiumView.as_view(), name="create and list stadiums"),
    path("matches", CreateListMatchView.as_view(), name="create and list matches"),
    re_path(r"^matches/(?P<id>[a-f0-9]{1,32})$", MatchDetailView.as_view(), name="view single match"),
]

urlpatterns = [
    re_path(r'^v1/', include(game_urls)),
]