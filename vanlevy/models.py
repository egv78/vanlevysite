from django.db import models
from accounts.models import VanLevyUser
from django.utils.translation import ugettext_lazy as lazy


class ContactModel(models.Model):
    user = models.ForeignKey(VanLevyUser, on_delete=models.PROTECT, blank=True, null=True)
    created_on = models.DateTimeField()
    area_of_concern = models.CharField(max_length=100, blank=True)
    issue_type = models.CharField(max_length=100, blank=True)
    message = models.CharField(max_length=1023, blank=True, null=True)
    given_email = models.EmailField(lazy('email address'), blank=True, null=True)