from django.db import models
from accounts.models import VanLevyUser, Avatar

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))


class SWRoom(models.Model):
    name = models.CharField(max_length=200, blank=False)
    passcode = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField()
    created_by = models.ForeignKey(VanLevyUser, on_delete=models.CASCADE)
    open_to_all = models.BooleanField(choices=BOOL_CHOICES, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "S.W. Room"
        verbose_name_plural = "S.W. Rooms"


class SWRoomToUser(models.Model):
    room_id = models.ForeignKey(SWRoom, on_delete=models.CASCADE)
    user_id = models.ForeignKey(VanLevyUser, on_delete=models.CASCADE)
    admitted = models.BooleanField(default=True)
    game_master = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    date_link_created = models.DateTimeField(auto_now_add=True)
    date_admitted = models.DateTimeField(blank=True, null=True)
    date_made_gm = models.DateTimeField(blank=True, null=True)
    date_banned = models.DateTimeField(blank=True, null=True)
    default_avatar_is_user = models.BooleanField(default=True)
    avatar_id = models.ForeignKey(Avatar, on_delete=models.CASCADE, default="", blank=True, null=True)

    def __str__(self):
        name_string = "ROOM #" + str(self.room_id.name) + "# to USER *" + str(self.user_id.username) + "*"
        return name_string

    class Meta:
        verbose_name = "S.W. Room to User Link"
        verbose_name_plural = "S.W. Room to User Links"


# need to implement saving at some point?
class EnterSWRoom(models.Model):
    room_number = models.IntegerField(blank=False)
    passcode = models.CharField(max_length=100, blank=True, null=True)
    default_avatar = models.IntegerField(default=0)


class SWRoomDestiny(models.Model):
    room_id = models.OneToOneField(SWRoom, on_delete=models.CASCADE)
    light_pips = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    dark_pips = models.PositiveSmallIntegerField(default=0, blank=True, null=True)


class SWRoomChat(models.Model):
    room_id = models.ForeignKey(SWRoom, on_delete=models.CASCADE)
    chat_text = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(VanLevyUser, on_delete=models.CASCADE)
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, default="", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    recipient = models.ForeignKey(VanLevyUser, on_delete=models.CASCADE, default="", blank=True, null=True,
                                  related_name="recipient")
    recipient_avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, default="", blank=True, null=True,
                                         related_name="recipient_avatar")


class SWDicePool(models.Model):
    num_boost_dice = models.PositiveSmallIntegerField(default=0)
    num_setback_dice = models.PositiveSmallIntegerField(default=0)
    num_ability_dice = models.PositiveSmallIntegerField(default=0)
    num_difficulty_dice = models.PositiveSmallIntegerField(default=0)
    num_proficiency_dice = models.PositiveSmallIntegerField(default=0)
    num_challenge_dice = models.PositiveSmallIntegerField(default=0)
    num_force_dice = models.PositiveSmallIntegerField(default=0)
    num_numerical_dice = models.PositiveSmallIntegerField(default=0)
    numerical_dice_sides = models.PositiveSmallIntegerField(default=100)

    faces_summary = models.CharField(max_length=400, null=True, blank=True)

    results_triumph = models.PositiveSmallIntegerField(default=0)
    results_despair = models.PositiveSmallIntegerField(default=0)
    results_success = models.PositiveSmallIntegerField(default=0)
    results_failure = models.PositiveSmallIntegerField(default=0)
    results_advantage = models.PositiveSmallIntegerField(default=0)
    results_threat = models.PositiveSmallIntegerField(default=0)
    results_light_pips = models.PositiveSmallIntegerField(default=0)
    results_dark_pips = models.PositiveSmallIntegerField(default=0)
    results_numerical = models.CharField(max_length=50, null=True, blank=True)

    additional_triumph = models.PositiveSmallIntegerField(default=0)
    additional_despair = models.PositiveSmallIntegerField(default=0)
    additional_success = models.PositiveSmallIntegerField(default=0)
    additional_failure = models.PositiveSmallIntegerField(default=0)
    additional_advantage = models.PositiveSmallIntegerField(default=0)
    additional_threat = models.PositiveSmallIntegerField(default=0)
    additional_light_pips = models.PositiveSmallIntegerField(default=0)
    additional_dark_pips = models.PositiveSmallIntegerField(default=0)

    caption = models.CharField(max_length=200, null=True, blank=True)
    is_just_caption = models.BooleanField(default=True)
    results_cancel = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(VanLevyUser, on_delete=models.SET_NULL, null=True)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True)
    image_url = models.URLField(blank=True, null=True)
    swroom = models.ForeignKey(SWRoom, on_delete=models.SET_NULL, null=True)
    secret_roll = models.BooleanField(default=False)
