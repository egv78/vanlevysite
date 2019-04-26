from django.db import models
from accounts.models import VanLevyUser, Avatar
from swdice.models import SWRoom


class PolyDicePool(models.Model):
    num_d4 = models.PositiveSmallIntegerField(default=0)
    num_d6 = models.PositiveSmallIntegerField(default=0)
    num_d8 = models.PositiveSmallIntegerField(default=0)
    num_d10 = models.PositiveSmallIntegerField(default=0)
    num_d12 = models.PositiveSmallIntegerField(default=0)
    num_d20 = models.PositiveSmallIntegerField(default=0)
    num_d100 = models.PositiveSmallIntegerField(default=0)
    num_numerical_dice = models.PositiveSmallIntegerField(default=0)
    numerical_dice_sides = models.PositiveSmallIntegerField(default=2)
    bonus = models.SmallIntegerField(default=0)

    results_d4 = models.CharField(max_length=150, null=True, blank=True)
    results_d6 = models.CharField(max_length=150, null=True, blank=True)
    results_d8 = models.CharField(max_length=150, null=True, blank=True)
    results_d10 = models.CharField(max_length=150, null=True, blank=True)
    results_d12 = models.CharField(max_length=150, null=True, blank=True)
    results_d20 = models.CharField(max_length=150, null=True, blank=True)
    results_d100 = models.CharField(max_length=150, null=True, blank=True)
    results_numerical = models.CharField(max_length=250, null=True, blank=True)
    results_total = models.SmallIntegerField(default=0)

    caption = models.CharField(max_length=200, null=True, blank=True)
    is_just_caption = models.BooleanField(default=True)
    results_cancel = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(VanLevyUser, on_delete=models.SET_NULL, null=True)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True)
    image_url = models.URLField(blank=True, null=True)
    swroom = models.ForeignKey(SWRoom, on_delete=models.SET_NULL, null=True)
    secret_roll = models.BooleanField(default=False)

