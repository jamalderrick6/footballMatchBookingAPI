from rest_framework import generics
from rest_framework.exceptions import ValidationError

from game.models import Team, Stadium, Match
from game.serializers import TeamSerializer, StadiumSerializer, MatchSerializer


class CreateListTeamView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class CreateListStadiumView(generics.ListCreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer


class CreateListMatchView(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def perform_create(self, serializer):
        team1_hash = self.request.data.get('team1')
        team2_hash = self.request.data.get('team2')
        stadium_hash = self.request.data.get('stadium')

        try:
            team1 = Team.objects.get(hash_value=team1_hash)
            team2 = Team.objects.get(hash_value=team2_hash)
            stadium = Stadium.objects.get(hash_value=stadium_hash)
        except (Team.DoesNotExist, Stadium.DoesNotExist):
            raise ValidationError('Invalid team or stadium hash value')

        serializer.save(team1=team1, team2=team2, stadium=stadium)


class MatchDetailView(generics.RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = 'id'


