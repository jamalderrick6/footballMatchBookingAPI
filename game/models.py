from hashlib import blake2b

from django.contrib.auth import get_user_model
from django.db import models


class Team(models.Model):

    name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    hash_value = models.CharField(max_length=32, blank=False, null=False, unique=True)

    class Meta:
        managed = True
        db_table = 'team'

    def save(self, *args, **kwargs):
        super(Team, self).save(*args, **kwargs)
        if not self.hash_value:
            self.hash_value = blake2b(
                key=type(self).__name__.lower().encode(), digest_size=16)
            self.hash_value.update(str(self.id).encode())
            self.hash_value = self.hash_value.hexdigest()
            self.save(update_fields=['hash_value'])



class Stadium(models.Model):

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    width = models.IntegerField()
    height = models.IntegerField()
    image = models.CharField(max_length=200, blank=True)
    hash_value = models.CharField(max_length=32, blank=True, null=True, unique=True)

    class Meta:
        managed = True
        db_table = 'stadium'

    def save(self, *args, **kwargs):
        super(Stadium, self).save(*args, **kwargs)
        if not self.hash_value:
            self.hash_value = blake2b(
                key=type(self).__name__.lower().encode(), digest_size=16)
            self.hash_value.update(str(self.id).encode())
            self.hash_value = self.hash_value.hexdigest()
            self.save(update_fields=['hash_value'])



class Match(models.Model):
    name = models.CharField(max_length=100)
    team1 = models.ForeignKey(Team, related_name='home', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='away', on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    linesMan1 = models.CharField(max_length=50)
    linesMan2 = models.CharField(max_length=50)
    mainReferee = models.CharField(max_length=50)
    seatPrice = models.IntegerField()
    date = models.CharField(max_length=50)
    hash_value = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'match'

    def save(self, *args, **kwargs):
        super(Match, self).save(*args, **kwargs)
        if not self.hash_value:
            self.hash_value = blake2b(
                key=type(self).__name__.lower().encode(), digest_size=16)
            self.hash_value.update(str(self.id).encode())
            self.hash_value = self.hash_value.hexdigest()
            self.save(update_fields=['hash_value'])



class Order(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    orderId = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'order'

class Reservation(models.Model):
    seat = models.CharField(max_length=100)
    ticketNumber = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='reservations', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'reservation'





            


