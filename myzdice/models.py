from django.db import models
from accounts.models import VanLevyUser, Avatar
from swdice.models import SWRoom


class MYZDicePool(models.Model):
    num_base_dice = models.PositiveSmallIntegerField(default=0)
    num_skill_dice = models.SmallIntegerField(default=0)
    num_gear_dice = models.PositiveSmallIntegerField(default=0)
    num_d6_dice = models.PositiveSmallIntegerField(default=0)
    num_d66_dice = models.PositiveSmallIntegerField(default=0)
    num_d666_dice = models.PositiveSmallIntegerField(default=0)
    num_numerical_dice = models.PositiveSmallIntegerField(default=0)
    numerical_dice_sides = models.PositiveSmallIntegerField(default=100)

    faces_summary = models.CharField(max_length=400, null=True, blank=True)
    holdover_faces = models.CharField(max_length=400, null=True, blank=True)

    results_success = models.SmallIntegerField(default=0)
    results_failure = models.SmallIntegerField(default=0)
    results_trauma = models.PositiveSmallIntegerField(default=0)
    results_damage = models.PositiveSmallIntegerField(default=0)
    results_d6 = models.CharField(max_length=50, null=True, blank=True)
    results_d66 = models.CharField(max_length=50, null=True, blank=True)
    results_d666 = models.CharField(max_length=50, null=True, blank=True)
    results_numerical = models.CharField(max_length=50, null=True, blank=True)

    additional_base_success = models.PositiveSmallIntegerField(default=0)
    additional_skill_success = models.PositiveSmallIntegerField(default=0)
    additional_gear_success = models.PositiveSmallIntegerField(default=0)
    additional_trauma = models.PositiveSmallIntegerField(default=0)
    additional_negative_success = models.PositiveSmallIntegerField(default=0)
    additional_gear_damage = models.PositiveSmallIntegerField(default=0)

    num_base_on_push = models.PositiveSmallIntegerField(default=0)
    num_skill_on_push = models.SmallIntegerField(default=0)
    num_gear_on_push = models.PositiveSmallIntegerField(default=0)
    num_base_suc_on_push = models.PositiveSmallIntegerField(default=0)
    num_skill_suc_on_push = models.PositiveSmallIntegerField(default=0)
    num_gear_suc_on_push = models.PositiveSmallIntegerField(default=0)
    num_trauma_on_push = models.PositiveSmallIntegerField(default=0)
    num_neg_suc_on_push = models.PositiveSmallIntegerField(default=0)
    num_damage_on_push = models.PositiveSmallIntegerField(default=0)

    caption = models.CharField(max_length=200, null=True, blank=True)
    is_just_caption = models.BooleanField(default=True)
    roll_is_pushed = models.BooleanField(default=False)
    roll_can_be_pushed = models.BooleanField(default=True)
    results_cancel = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(VanLevyUser, on_delete=models.SET_NULL, null=True)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True)
    image_url = models.URLField(blank=True, null=True)
    swroom = models.ForeignKey(SWRoom, on_delete=models.SET_NULL, null=True)
    secret_roll = models.BooleanField(default=False)
