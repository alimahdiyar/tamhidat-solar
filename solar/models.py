from django.db import models

# Create your models here.

class SolarLevelType(models.Model):
    first_level_share = models.IntegerField()
    other_levels_share = models.IntegerField()
    people_in_a_level = models.IntegerField()
    levels = models.IntegerField()
    tamhidat_card_price = models.IntegerField(default=100000)