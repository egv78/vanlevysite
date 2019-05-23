from django.db import models
from accounts.models import VanLevyUser, Avatar, BOOL_CHOICES


class GenCharSheet(models.Model):
    user = models.ForeignKey(VanLevyUser, on_delete=models.CASCADE)
    char_name = models.CharField(max_length=200, default='', blank=True)
    char_description = models.CharField(max_length=500, default='', blank=True)
    char_url_image = models.URLField(max_length=300, blank=True, default='')
    created_on = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(choices=BOOL_CHOICES, default=False)
