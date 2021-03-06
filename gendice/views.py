from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import FormMixin

from swdice.models import SWRoomToUser, SWRoomChat, SWRoom, SWRoomDestiny, SWDicePool
from swdice.forms import Make_SW_Room, Enter_SW_Room, Enter_SW_Direct, SW_Room_Chat_Form, SW_Dice_Roll
from swdice.dice import *
from swdice.views import *
from accounts.models import VanLevyUser, Avatar
import datetime


def about(request):
    template_name = 'gendice/about_gendiceroller.html'
    return render(request, template_name)


def error_gen(request):
    template_name = '404_gen.html'
    return render(request, template_name)
