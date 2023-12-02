import json
import uuid

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from game.models import Team, Stadium, Match, Reservation, Order
from game.serializers import TeamSerializer, StadiumSerializer, MatchSerializer, ReservationSerializer, OrderSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateListTeamView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class CreateListStadiumView(generics.ListCreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer


class ListReservationsView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    def get_queryset(self):
        match_id = self.kwargs['id']
        return Reservation.objects.filter(order__match_id=match_id)


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


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).prefetch_related('reservations')


class OrderDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def delete(self, request, order_id, format=None):
        order = get_object_or_404(Order, orderId=order_id)

        # Check if the request user is the owner of the order or an admin
        if request.user == order.user or request.user.is_staff:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def create_checkout_session(request):
    price = request.data.get('price')
    match_id = request.data['match_id']
    user_id = request.data['user_id']
    seats = request.data.get('seats') or []
    total_cost = int(price) * len(seats)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': total_cost,
                'product_data': {
                    'name': f'Reservation for match {match_id}',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url="http://localhost:3000/user-reservation",
        cancel_url=f"http://localhost:3000/matches/{match_id}",
        metadata={
            'match_id': match_id,
            'user_id': user_id,
            'seats': json.dumps(seats)
        }
    )

    return Response({'sessionId': checkout_session['id']})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, request.headers.get('Stripe-Signature'), settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Perform order and reservation creation logic here
        create_order_and_reservations(session)

    return HttpResponse(status=200)


def generate_ticket_number():
    ticket_number = uuid.uuid4()
    return ticket_number


def create_order_and_reservations(session):
    metadata = session['metadata']
    match_id = metadata['match_id']
    user_id = metadata['user_id']
    seats = json.loads(metadata['seats'])

    match = Match.objects.get(id=match_id)
    user = get_user_model().objects.get(id=user_id)
    order = Order.objects.create(match=match, orderId=session['id'], user=user)

    for seat in seats:
        seat_str = f"{seat['x']}:{seat['y']}"
        ticket_number = generate_ticket_number()
        Reservation.objects.create(order=order, seat=seat_str, ticketNumber=ticket_number, user=user)


