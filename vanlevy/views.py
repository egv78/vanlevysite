from django.shortcuts import render
from django.views.generic import TemplateView
from swdice.models import SWRoomToUser, SWRoom
from accounts.models import VanLevyUser, Avatar
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_range(value):
    return range(value)


class TempRoom:
    def __init__(self, room_name, avatar, gm, id):
        self.room_name = room_name
        self.avatar = avatar
        self.gm = gm
        self.id = id


def vl_home_view(request):
    template_name = 'vanlevy/vl_home.html'
    return render(request, template_name)


def vl_about_view(request):
    template_name = 'vanlevy/vl_about.html'
    return render(request, template_name)


def vl_resources_view(request):
    template_name = 'vanlevy/vl_resources.html'
    return render(request, template_name)


def vl_cool_stuff_view(request):
    template_name = 'vanlevy/vl_cool_stuff.html'
    return render(request, template_name)


def vl_dice_rollers_view(request):
    template_name = 'vanlevy/dice_rollers.html'
    return render(request, template_name)


def vl_terms_view(request):
    template_name = 'vanlevy/vl_terms.html'
    return render(request, template_name)


def personal_portal(request):
    current_user_id = request.user.id
    user_name = request.user.username
    my_avatars = Avatar.objects.filter(user_id=current_user_id, deleted=False).order_by('-id')
    if len(my_avatars) == 0:
        has_avatars = False
    else:
        has_avatars = True
    my_rooms_to_user_list = SWRoomToUser.objects.filter(user_id_id=current_user_id, banned=0).order_by(
        '-admitted')
    my_rooms_reversed_list = my_rooms_to_user_list[::-1]
    number_rooms = 5 if (len(my_rooms_to_user_list) > 5) else len(my_rooms_to_user_list)

    my_rooms_list = []

    for room in my_rooms_reversed_list[:number_rooms]:
        this_room = SWRoom.objects.filter(pk=room.room_id_id)[0]
        room_name = (this_room.name[:38] + '..') if len(this_room.name) > 40 else this_room.name
        room_id = room.room_id_id
        if room.game_master:
            gm = "you"
        else:
            gm_rooms = SWRoomToUser.objects.filter(room_id=room.room_id, game_master=True)
            if gm_rooms:
                gm_id = gm_rooms[0].user_id
                gm_name = gm_id.username
                gm = gm_name
            else:
                gm = "no one"
        if room.default_avatar_is_user == 1:
            name_in_room = user_name
        else:
            try:
                name_in_room = Avatar.objects.filter(user_id=current_user_id,id=room.avatar_id_id)[0]
            except:
                name_in_room = user_name
        new_room = TempRoom(room_name, name_in_room, gm, room_id)
        my_rooms_list.append(new_room)

    template_name = 'vanlevy/vl_portal.html'
    args = {'user': request.user, 'my_rooms_list': my_rooms_list, 'my_avatars_list': my_avatars,
            'has_avatars': has_avatars, 'number_rooms': number_rooms}
    return render(request, template_name, args)
