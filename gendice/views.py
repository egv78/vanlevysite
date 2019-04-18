from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import FormMixin
from django.template.defaulttags import register
from swdice.models import SWRoomToUser, SWRoomChat, SWRoom, SWRoomDestiny, SWDicePool
from swdice.forms import Make_SW_Room, Enter_SW_Room, Enter_SW_Direct, SW_Room_Chat_Form, SW_Dice_Roll
from swdice.dice import *
from swdice.views import *
from accounts.models import VanLevyUser, Avatar
import datetime


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_range(value):
    return range(value)


@register.filter
def split_string(string):
    faces_list = string.split(",")
    return faces_list


def about(request):
    template_name = 'gendice/about_gendiceroller.html'
    return render(request, template_name)


def error_gen(request):
    template_name = '404_gen.html'
    return render(request, template_name)


def direct_view_gen(request, swroom_id, slug):
    current_user_id = request.user.id
    user_to_room_link_candidate = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)
    if len(user_to_room_link_candidate) > 0:
        user_to_room_link = user_to_room_link_candidate[0]
    else:
        user_to_room_link = False
    if user_to_room_link:
        if user_to_room_link.banned:
            return redirect('gendice:confluence')  # will need to change when banning implemented
        else:
            return redirect('gendice:genroom', swroom_id)
    else:
        # make link, redirect
        make_user_room_link(swroom_id, current_user_id, False, False, True, 0)
        return redirect('gendice:genroom', swroom_id)