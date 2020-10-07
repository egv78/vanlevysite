from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, View
from django.views.generic.edit import FormMixin

from accounts.models import VanLevyUser, Avatar
from .models import SWRoomToUser, SWRoomChat, SWRoom, SWRoomDestiny, SWDicePool
from .forms import Make_SW_Room, Enter_SW_Room, Enter_SW_Direct, SW_Room_Chat_Form, SW_Dice_Roll
from .dice import *
from .mixins import AjaxFormMixin

import datetime


# Methods used in views

def make_user_room_link(room_id, user_id, gm=False, banned=False, avatar_is_user=True, avatar=0):
    if SWRoomToUser.objects.filter(user_id_id=user_id, room_id_id=room_id):
        link_instance = SWRoomToUser.objects.filter(user_id_id=user_id, room_id_id=room_id)[0]
        new_user = False
    else:
        link_instance = SWRoomToUser()
        new_user = True
    now = datetime.datetime.now()
    link_instance.room_id_id = room_id
    link_instance.user_id = VanLevyUser(pk=user_id)
    link_instance.admitted = True
    link_instance.game_master = gm
    link_instance.banned = banned
    link_instance.default_avatar_is_user = avatar_is_user

    if new_user:
        link_instance.date_link_created = now
        link_instance.date_admitted = now

    if int(avatar) == 0:
        link_instance.avatar_id_id = ""
    else:
        link_instance.avatar_id_id = int(avatar)

    if gm:
        link_instance.date_made_gm = now
    if banned:
        link_instance.date_banned = now

    link_instance.save()


def save_dice_pool(user, avatar, room, image_url, caption="",
                   num_boost_dice=0, num_ability_dice=0, num_proficiency_dice=0,
                   num_setback_dice=0, num_difficulty_dice=0, num_challenge_dice=0, num_force_dice=0,
                   additional_triumph=0, additional_despair=0, additional_success=0, additional_failure=0,
                   additional_advantage=0, additional_threat=0,
                   additional_light_pips=0, additional_dark_pips=0,
                   num_numerical_dice=0, numerical_dice_sides=0, just_caption=True, secret_roll=False):
    new_dice_pool = SWDicePool()
    new_dice_pool.user = user
    new_dice_pool.avatar = avatar
    new_dice_pool.swroom_id = room
    new_dice_pool.caption = caption
    new_dice_pool.image_url = image_url
    new_dice_pool.num_boost_dice = num_boost_dice
    new_dice_pool.num_ability_dice = num_ability_dice
    new_dice_pool.num_proficiency_dice = num_proficiency_dice
    new_dice_pool.num_setback_dice = num_setback_dice
    new_dice_pool.num_difficulty_dice = num_difficulty_dice
    new_dice_pool.num_challenge_dice = num_challenge_dice
    new_dice_pool.num_force_dice = num_force_dice
    new_dice_pool.additional_triumph = additional_triumph
    new_dice_pool.additional_despair = additional_despair
    new_dice_pool.additional_success = additional_success
    new_dice_pool.additional_failure = additional_failure
    new_dice_pool.additional_advantage = additional_advantage
    new_dice_pool.additional_threat = additional_threat
    new_dice_pool.additional_light_pips = additional_light_pips
    new_dice_pool.additional_dark_pips = additional_dark_pips
    new_dice_pool.num_numerical_dice = num_numerical_dice
    new_dice_pool.numerical_dice_sides = numerical_dice_sides
    new_dice_pool.is_just_caption = just_caption
    new_dice_pool.secret_roll = secret_roll

    swdice = {'boost': num_boost_dice, 'ability': num_ability_dice, 'proficiency': num_proficiency_dice,
              'setback': num_setback_dice, 'difficulty': num_difficulty_dice, 'challenge': num_challenge_dice,
              'force': num_force_dice,
              "additional_triumph": additional_triumph, "additional_despair": additional_despair,
              "additional_success": additional_success, "additional_failure": additional_failure,
              "additional_advantage": additional_advantage, "additional_threat": additional_threat,
              "additional_light_pips": additional_light_pips, "additional_dark_pips": additional_dark_pips,
              }

    summary_string, net_results = roll_sw_dice(**swdice)
    new_dice_pool.faces_summary = summary_string
    new_dice_pool.results_triumph = net_results[0]
    new_dice_pool.results_despair = net_results[1]
    new_dice_pool.results_success = net_results[2]
    new_dice_pool.results_failure = net_results[3]
    new_dice_pool.results_advantage = net_results[4]
    new_dice_pool.results_threat = net_results[5]
    new_dice_pool.results_dark_pips = net_results[6]
    new_dice_pool.results_light_pips = net_results[7]
    numerical_meanings = range(1, (numerical_dice_sides + 1))
    numerical_die = Die("Numerical", numerical_meanings, "", True)
    numerical_string, numerical_results = numerical_die.roll(num_numerical_dice)
    new_dice_pool.results_numerical = numerical_string
    sum_results = 0
    for number in net_results:
        sum_results += number
    if sum_results == 0 and not just_caption and num_numerical_dice == 0:
        new_dice_pool.results_cancel = True
    else:
        new_dice_pool.results_cancel = False

    new_dice_pool.save()


def change_destiny(user, avatar, room, image_url, caption="", delta_light=0, delta_dark=0):
    destiny = SWRoomDestiny.objects.get(room_id_id=room)
    light_pips = destiny.light_pips
    dark_pips = destiny.dark_pips
    new_light = light_pips + delta_light
    new_dark = dark_pips + delta_dark
    if new_light >= 0 and new_dark >= 0:
        destiny.light_pips += delta_light
        destiny.dark_pips += delta_dark
        destiny.save()
        kwargs = {"user": user, "avatar": avatar, "room": room, "caption": caption,
                  "image_url": image_url}
        save_dice_pool(**kwargs)
    else:
        pass


def read_chat(chat_form, avatar, swroom_id, current_user, chat_text, image_url):
    recipient_id = chat_form.data['recipient']
    recipient_user = VanLevyUser.objects.filter(id=recipient_id)[0]
    room_user_link_recipient = SWRoomToUser.objects.filter(room_id_id=swroom_id, user_id=recipient_user)[0]
    recipient_avatar = room_user_link_recipient.avatar_id
    is_private = not (recipient_user == current_user)
    new_chat = SWRoomChat()
    new_chat.room_id_id = swroom_id
    new_chat.chat_text = chat_text
    new_chat.user = current_user
    new_chat.avatar = avatar
    new_chat.image_url = image_url
    new_chat.is_private = is_private
    new_chat.recipient = recipient_user if is_private else None
    new_chat.recipient_avatar = recipient_avatar
    return new_chat


def read_dice(dice_form):
    boost_dice = dice_form.cleaned_data['num_boost_dice']
    ability_dice = dice_form.cleaned_data['num_ability_dice']
    proficiency_dice = dice_form.cleaned_data['num_proficiency_dice']
    setback_dice = dice_form.cleaned_data['num_setback_dice']
    difficulty_dice = dice_form.cleaned_data['num_difficulty_dice']
    challenge_dice = dice_form.cleaned_data['num_challenge_dice']
    force_dice = dice_form.cleaned_data['num_force_dice']
    numerical_sides = dice_form.cleaned_data['numerical_dice_sides']
    numerical_dice = dice_form.cleaned_data['num_numerical_dice']
    caption = dice_form.cleaned_data['caption']
    additional_triumph = dice_form.cleaned_data['additional_triumph']
    additional_despair = dice_form.cleaned_data['additional_despair']
    additional_success = dice_form.cleaned_data['additional_success']
    additional_failure = dice_form.cleaned_data['additional_failure']
    additional_advantage = dice_form.cleaned_data['additional_advantage']
    additional_threat = dice_form.cleaned_data['additional_threat']
    additional_light_pips = dice_form.cleaned_data['additional_light_pips']
    additional_dark_pips = dice_form.cleaned_data['additional_dark_pips']
    total_dice = (boost_dice + ability_dice + proficiency_dice + force_dice +
                  setback_dice + difficulty_dice + challenge_dice + numerical_dice +
                  additional_triumph + additional_despair + additional_success + additional_failure +
                  additional_advantage + additional_threat + additional_light_pips + additional_dark_pips
                  )

    if caption or total_dice > 0:
        valid_pool = True
        if total_dice == 0:
            just_caption = True
        else:
            just_caption = False
    else:
        just_caption = False
        valid_pool = False

    dice_pool = {'caption': caption, "total_dice": total_dice,
                 "num_boost_dice": boost_dice, "num_ability_dice": ability_dice,
                 "num_proficiency_dice": proficiency_dice, "num_setback_dice": setback_dice,
                 "num_difficulty_dice": difficulty_dice, "num_challenge_dice": challenge_dice,
                 "num_force_dice": force_dice, "just_caption": just_caption,
                 "num_numerical_dice": numerical_dice, "numerical_dice_sides": numerical_sides,
                 "additional_triumph": additional_triumph, "additional_despair": additional_despair,
                 "additional_success": additional_success, "additional_failure": additional_failure,
                 "additional_advantage": additional_advantage, "additional_threat": additional_threat,
                 "additional_light_pips": additional_light_pips,
                 "additional_dark_pips": additional_dark_pips, "valid_pool": valid_pool,
                 }
    return dice_pool


def get_chat_carryover(request, chat_form, current_user_id):
    chat_text = chat_form.data['chat_text']
    recipient_id = chat_form.data['recipient']
    if chat_text != '':
        request.session['chat_carryover'] = chat_text
    if int(recipient_id) != int(current_user_id):
        request.session['recipient_carryover'] = recipient_id


def get_dice_carryover(request, dice_form):
    if dice_form.is_valid():
        dice_pool = read_dice(dice_form)
        total_dice = dice_pool['total_dice']
        del dice_pool['total_dice']
        valid_pool = dice_pool['valid_pool']
        del dice_pool['valid_pool']
        caption = dice_pool['caption']

        if valid_pool and (caption or total_dice > 0):
            request.session['dice_pool_carryover'] = dice_pool
        else:
            pass
    else:
        pass


class UpdateTimes:
    def __init__(self, action_time, chat_time):
        self.action = action_time
        self.chat = chat_time


# Views

def about(request):
    template_name = 'swdice/about_swdiceroller.html'
    return render(request, template_name)


def error(request):
    template_name = '404_sw.html'
    return render(request, template_name)


class BadRoom(TemplateView):
    def get(self, request):
        template_name = self.template_name
        if 'bad_room' in request.session:
            bad_room_id = request.session['bad_room']
            del request.session['bad_room']
        else:
            bad_room_id = ""

        if 'bad_room_url' in request.session:
            bad_room_url = request.session['bad_room_url']
            del request.session['bad_room_url']
        else:
            bad_room_url = ''
        args = {'bad_room_id': bad_room_id, 'bad_room_url': bad_room_url}
        return render(request, template_name, args)


class MakeDiceRoom(TemplateView, FormMixin):
    def post(self, request, **kwargs):
        gendice = 'gendice' in self.template_name
        polydice = 'polydice' in self.template_name
        myzdice = 'myzdice' in self.template_name

        if gendice:
            url_404 = 'gendice:404'
            hub_url = 'gendice:confluence'
            info_url = 'gendice:genroom_info'
        elif polydice:
            url_404 = 'polydice:404'
            hub_url = 'polydice:dungeon'
            info_url = 'polydice:polyroom_info'
        elif myzdice:
            url_404 = 'myzdice:404'
            hub_url = 'myzdice:the_zone'
            info_url = 'myzdice:myzroom_info'
        else:
            url_404 = 'swdice:404'
            hub_url = 'swdice:dockingbay'
            info_url = 'swdice:swroom_info'

        if "make_room" in request.POST:
            form = Make_SW_Room(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.created_by = request.user
                now = datetime.datetime.now()
                instance.created_on = now
                instance.genesys = gendice
                instance.polydice = polydice
                instance.myzdice = myzdice
                instance.save()
                user_id = request.user.id
                room_id = instance.id
                make_user_room_link(room_id, user_id, True, False, True, 0)
                destiny = SWRoomDestiny()
                destiny.room_id_id = room_id
                destiny.dark_pips = 0
                destiny.light_pips = 0
                destiny.save()
                return redirect(hub_url)
            else:
                args = {'form': form}
                form_template = self.template_name
                return render(request, form_template, args)
        elif "change_passcode" in request.POST:
            form = Make_SW_Room(request.POST)
            swroom_id = self.kwargs['swroom_id']
            try:
                room = SWRoom.objects.get(pk=swroom_id)
            except SWRoom.DoesNotExist:
                return redirect(url_404)

            if form.is_valid():
                room.open_to_all = form.cleaned_data['open_to_all']
                room.passcode = form.cleaned_data['passcode']
                room.save()
                return redirect(info_url, swroom_id)
            else:
                args = {'form': form, 'room_number': swroom_id, 'room': room}
                form_template = self.template_name
                return render(request, form_template, args)
        else:
            return redirect(hub_url)

    def get(self, request, **kwargs):
        now = datetime.datetime.now()
        user_id = request.user.id
        change_passcode = 'change' in self.template_name

        if not change_passcode:
            initial_args = {'open_to_all': True, 'created_on': now, 'created_by': user_id}
            form = Make_SW_Room(initial_args)
            args = {'form': form}
        else:
            swroom_id = self.kwargs['swroom_id']
            try:
                room = SWRoom.objects.get(pk=swroom_id)
            except SWRoom.DoesNotExist:
                if 'gendice' in request.path:
                    return redirect('gendice:404')
                elif 'polydice' in request.path:
                    return redirect('polydice:404')
                elif 'myzdice' in request.path:
                    return redirect('myzdice:404')
                else:
                    return redirect('swdice:404')

            initial_args = {'open_to_all': False, 'name': room.name}
            form = Make_SW_Room(initial_args)
            args = {'form': form, 'room_number': swroom_id, 'room': room}
        return render(request, self.template_name, args)


class DirectLink(TemplateView):
    def get(self, request, swroom_id, slug):
        current_user_id = self.request.user.id
        gendice = 'gendice' in self.template_name
        polydice = 'polydice' in self.template_name
        myzdice = 'myzdice' in self.template_name

        if gendice:
            room_url = 'gendice:genroom'
            redirect_place = 'gendice:confluence'
            bad_room_url = 'gendice:bad_room'
        elif polydice:
            room_url = 'polydice:polyroom'
            redirect_place = 'polydice:dungeon'
            bad_room_url = 'polydice:bad_room'
        elif myzdice:
            room_url = 'myzdice:myzroom'
            redirect_place = 'myzdice:the_zone'
            bad_room_url = 'myzdice:bad_room'
        else:
            room_url = 'swdice:swroom'
            redirect_place = 'swdice:dockingbay'
            bad_room_url = 'swdice:bad_room'

        user_to_room_link_candidate = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)
        try:
            room = SWRoom.objects.get(pk=swroom_id)
            passcode = room.passcode
        except SWRoom.DoesNotExist:
            request.session['bad_room_url'] = 'direct link'
            request.session['bad_room'] = swroom_id
            return redirect(bad_room_url)

        if len(user_to_room_link_candidate) > 0:
            user_to_room_link = user_to_room_link_candidate[0]
        else:
            user_to_room_link = False

        if user_to_room_link:
            if user_to_room_link.banned:
                request.session['problem'] = "You have been banned from that room."
                return redirect(redirect_place)
            else:
                return redirect(room_url, swroom_id)
        else:
            # if passcode is right (or room open), make link, redirect
            if slug == passcode or slug == 'open':
                make_user_room_link(swroom_id, current_user_id, False, False, True, 0)
                return redirect(room_url, swroom_id)
            else:
                request.session['problem'] = "There is a problem with the link to "
                requested_url = request.get_full_path()
                request.session['requested_url'] = requested_url
                return redirect(redirect_place)


class HubView(FormMixin, TemplateView):
    form_class = Enter_SW_Room

    def get_form_kwargs(self):
        # get avatar choices for enter room forms
        kwargs = super().get_form_kwargs()
        if self.request.user.userprofile.user_first_name:
            user_name = self.request.user.userprofile.user_first_name
        else:
            user_name = self.request.user.username
        # instantiate avatars list, start with user name
        my_avatars = Avatar.objects.filter(user_id=self.request.user.id)
        my_avatars_choices = [(0, user_name)]
        for avatar in my_avatars:
            if avatar.deleted != 1:
                if len(avatar.avatar_name) < 40:
                    my_avatars_choices.append((avatar.id, avatar.avatar_name))
                else:
                    my_avatars_choices.append((avatar.id, avatar.avatar_name[:37]+"..."))
        kwargs['avatar_list'] = my_avatars_choices
        return kwargs

    def get(self, request, *args, **kwargs):
        # import problems with POST
        if 'problem' in request.session:
            problem = request.session['problem']
            del request.session['problem']
            if 'requested_url' in request.session:
                requested_url = request.session['requested_url']
                del request.session['requested_url']
            else:
                requested_url = ""
        else:
            problem = ""
            requested_url = ""

        # this is for enter with passcode and switch avatar
        try:
            room_id = self.kwargs['swroom_id']
        except:
            room_id = ""

        kwargs = self.get_form_kwargs()
        avatars = dict(kwargs['avatar_list'])
        current_user_id = self.request.user.id
        genesys = 'gendice' in self.template_name
        polydice = 'polydice' in self.template_name
        myzdice = 'myzdice' in self.template_name

        # get rooms for links / information in Rooms Table
        my_rooms_to_user_list_first = SWRoomToUser.objects.filter(user_id_id=current_user_id,
                                                                  banned=0
                                                                  ).order_by('-admitted')
        my_rooms_to_user_list = my_rooms_to_user_list_first[::-1]
        my_rooms_list = []
        my_avatars_list = {}
        gms_list = {}
        player_numbers_list = {}
        has_archived_rooms = False
        number_of_rooms = 0

        for room in my_rooms_to_user_list:
            maybe_this_room = SWRoom.objects.filter(pk=room.room_id_id,
                                                    genesys=genesys,
                                                    polydice=polydice,
                                                    myzdice=myzdice
                                                    )
            if len(maybe_this_room) > 0:
                this_room = maybe_this_room[0]
                if this_room.disabled:
                    has_archived_rooms = True
                else:
                    number_of_rooms += 1

                my_rooms_list += SWRoom.objects.filter(pk=room.room_id_id)

                if room.game_master:
                    gms_list[room.room_id_id] = "you"
                else:
                    gm_rooms = SWRoomToUser.objects.filter(room_id=room.room_id, game_master=True)
                    if gm_rooms:
                        gm_id = gm_rooms[0].user_id
                        gm_name = gm_id.username
                        gms_list[room.room_id_id] = gm_name
                    else:
                        gms_list[room.room_id_id] = "no one"

                number_players = len(SWRoomToUser.objects.filter(room_id=room.room_id, game_master=False, banned=0))
                player_numbers_list[room.room_id_id] = number_players
                if room.default_avatar_is_user == 1:
                    my_avatars_list[room.room_id_id] = avatars[0]
                else:
                    try:
                        my_avatars_list[room.room_id_id] = avatars[room.avatar_id_id]
                    except:
                        my_avatars_list[room.room_id_id] = avatars[0]
                        game_master = room.game_master
                        make_user_room_link(room.room_id_id, current_user_id, game_master, False, 1, 0)

        form = Enter_SW_Room(**kwargs)
        form_direct = Enter_SW_Direct(**kwargs)
        my_avatar_objects = Avatar.objects.filter(user_id=self.request.user.id, deleted=0)
        args = {'form': form, 'my_rooms_list': my_rooms_list, 'my_avatars_list': my_avatars_list, 'room_id': room_id,
                'my_avatar_objects': my_avatar_objects, 'gms_list': gms_list, 'form_direct': form_direct,
                'player_numbers_list': player_numbers_list, 'number_of_rooms': number_of_rooms,
                'problem': problem, 'requested_url': requested_url, 'has_archived_rooms': has_archived_rooms}
        return render(request, self.template_name, args)

    # if request.method == 'POST':
    def post(self, request, **kwargs):
        # determine the room type
        genesys = 'gendice' in self.template_name
        polydice = 'polydice' in self.template_name
        myzdice = 'myzdice' in self.template_name

        if genesys:
            room_url = 'gendice:genroom'
            hub_url = 'gendice:confluence'
            enter_url = 'gendice:enter_passcode_room'
            bad_room = 'gendice:bad_room'
        elif polydice:
            room_url = 'polydice:polyroom'
            hub_url = 'polydice:dungeon'
            enter_url = 'polydice:enter_passcode_room'
            bad_room = 'polydice:bad_room'
        elif myzdice:
            room_url = 'myzdice:myzroom'
            hub_url = 'myzdice:the_zone'
            enter_url = 'myzdice:enter_passcode_room'
            bad_room = 'myzdice:bad_room'
        else:
            room_url = 'swdice:swroom'
            hub_url = 'swdice:dockingbay'
            enter_url = 'swdice:enter_passcode_room'
            bad_room = 'swdice:bad_room'

        kwargs = self.get_form_kwargs()
        form = Enter_SW_Room(**kwargs)
        form_direct = Enter_SW_Direct(**kwargs)

        if request.method == "POST" and "passcode" in request.POST:
            if form.is_valid():
                swroom_id = form.cleaned_data['room_number']
                passcode_candidate = form.cleaned_data['passcode']
                avatar_id = form.cleaned_data['default_avatar']
                instance = form.save(commit=False)
                instance.user = request.user

                use_user_id = True if int(avatar_id) == 0 else False

                try:
                    room = SWRoom.objects.get(pk=swroom_id)
                    my_rooms_to_user_list = SWRoomToUser.objects.filter(user_id_id=self.request.user.id).order_by('-admitted')
                    my_rooms_list = []
                    for my_room in my_rooms_to_user_list:
                        my_rooms_list += SWRoom.objects.filter(pk=my_room.room_id_id)
                    been_there = my_rooms_to_user_list.filter(room_id_id=swroom_id)
                    if been_there and not been_there[0].banned and been_there[0].avatar_id_id == avatar_id:
                        return redirect(room_url, swroom_id)
                    elif been_there and not been_there[0].banned:
                        link_instance = been_there[0]
                        link_instance.avatar_id_id = avatar_id if int(avatar_id) > 0 else ""
                        link_instance.default_avatar_is_user = 1 if int(avatar_id) == 0 else 0
                        link_instance.save()
                        return redirect(room_url, swroom_id)
                    elif been_there and been_there[0].banned:
                        request.session['problem'] = "You have been banned from that room."
                        return redirect(hub_url)
                    else:
                        passcode_correct = room.passcode
                        room_is_open = room.open_to_all
                        if room_is_open or (passcode_candidate == passcode_correct):
                            game_master = False
                            banned = False
                            make_user_room_link(swroom_id, request.user.id, game_master, banned, use_user_id, avatar_id)
                            instance.save()
                            return redirect(room_url, swroom_id)
                        else:
                            return redirect(enter_url, swroom_id)
                except SWRoom.DoesNotExist:
                    request.session['bad_room'] = swroom_id
                    return redirect(bad_room)

            else:
                request.session['problem'] = "There is a problem with the information you provided."
                return redirect(hub_url)

        elif request.method == "POST" and "direct" in request.POST:
            if form_direct.is_valid():
                init_direct_link = form_direct.cleaned_data['direct']
                if 'swdice' in init_direct_link:
                    first_bit = "www.vanlevy.com/swdice/room/"
                elif 'gendice' in init_direct_link:
                    first_bit = "www.vanlevy.com/gendice/room/"
                elif 'polydice' in init_direct_link:
                    first_bit = "www.vanlevy.com/polydice/room/"

                end_bit = init_direct_link.replace(first_bit, "", 1)
                number_string = ""
                i = 0
                while i < len(end_bit):
                    character = end_bit[i]
                    if character.isdigit():
                        number_string += str(character)
                        i += 1
                    else:
                        i = len(end_bit)
                next_bit = number_string + "/direct/"
                passcode = end_bit.replace(next_bit, "", 1)
                swroom_id = int(number_string)
                avatar_id = form_direct.cleaned_data['default_avatar']
                use_user_id = True if int(avatar_id) == 0 else False
                new_room_list = SWRoom.objects.filter(id=swroom_id, passcode=passcode)
                if len(new_room_list) > 0:
                    new_room = new_room_list[0]
                    my_rooms_to_user_list = SWRoomToUser.objects.filter(user_id_id=self.request.user.id).order_by(
                        '-admitted')
                    been_there = my_rooms_to_user_list.filter(room_id_id=new_room.id)
                    if been_there and not been_there[0].banned:
                        return redirect(room_url, new_room.id)
                    elif not been_there:
                        game_master = False
                        banned = False
                        make_user_room_link(new_room.id, request.user.id, game_master, banned, use_user_id, avatar_id)
                        return redirect(room_url, new_room.id)
                    elif been_there and been_there[0].banned:
                        request.session['problem'] = "You have been banned from that room."
                        return redirect(hub_url)
                    else:
                        request.session['problem'] = "There is a problem with the link you provided."
                        return redirect(hub_url)
                else:
                    request.session['problem'] = "There is a problem with the link you provided."
                    return redirect(hub_url)
            else:
                request.session['problem'] = "There is a problem with the information you provided."
                return redirect(hub_url)
        else:
            return redirect(hub_url)


class SWRoomViews(FormMixin, AjaxFormMixin, TemplateView):

    def get_form_kwargs(self):
        swroom_id = self.kwargs['swroom_id']
        kwargs = super().get_form_kwargs()
        user_id = self.request.user.id
        room_users_link_list = SWRoomToUser.objects.filter(room_id_id=swroom_id).exclude(user_id_id=user_id)

        if room_users_link_list:
            recipients_list = [(self.request.user.id, "Send to all")]  # self as recipient = key for not private
            for user_in_room in room_users_link_list:
                if not user_in_room.banned:
                    if len(user_in_room.user_id.username) > 14:
                        user_name = user_in_room.user_id.username[:11] + "..."
                        name_length = 14
                    else:
                        user_name = user_in_room.user_id.username
                        name_length = len(user_name)
                    if user_in_room.default_avatar_is_user:
                        name_in_room = "themself"
                    else:
                        if len(user_in_room.avatar_id.avatar_name) > 34-name_length:
                            name_in_room = user_in_room.avatar_id.avatar_name[:(31-name_length)] + "..."
                        else:
                            name_in_room = user_in_room.avatar_id.avatar_name
                    display_name = user_name + " as " + name_in_room
                    recipients_list.append((user_in_room.user_id_id, display_name))

        else:
            recipients_list = [(self.request.user.id, "No other users in room")]

        kwargs['recipients_list'] = recipients_list
        return kwargs

    def post(self, request, *args, **kwargs):
        swroom_id = self.kwargs['swroom_id']
        room = SWRoom.objects.get(pk=swroom_id)
        current_user = self.request.user
        current_user_id = self.request.user.id
        genesys = room.genesys
        room_url = 'gendice:genroom' if genesys else 'swdice:swroom'
        hub_url = 'gendice:confluence' if genesys else 'swdice:dockingbay'
        info_url = 'gendice:genroom_info' if genesys else 'swdice:swroom_info'

        viewing_player_info = "player" in self.template_name
        if viewing_player_info:
            player_id = self.kwargs['player_id']
            gm_user_id = self.request.user.id
            room_player_link = SWRoomToUser.objects.filter(user_id_id=player_id, room_id_id=swroom_id)[0]
            player_avatar_is_user = room_player_link.default_avatar_is_user
            player_avatar = int(room_player_link.avatar_id_id) if room_player_link.avatar_id else 0

        viewing_basic_room = "info" not in self.template_name
        if viewing_basic_room:
            room_to_user_link = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)[0]
            avatar = room_to_user_link.avatar_id
            if avatar is None:
                image_url = current_user.userprofile.user_url_image if current_user.userprofile.user_url_image else ""
            elif avatar.avatar_url_image:
                image_url = avatar.avatar_url_image
            else:
                image_url = ''

        # Player Info view functions
        if request.method == "POST" and "make_gm_real" in request.POST:
            # make player new gm
            user_id = player_id
            avatar_is_user = player_avatar_is_user
            avatar = player_avatar
            make_user_room_link(swroom_id, user_id, True, False, avatar_is_user, avatar)
            room_old_gm_link = SWRoomToUser.objects.filter(user_id_id=gm_user_id, room_id_id=swroom_id)[0]
            # change old gm to player
            old_gm_avatar_is_user = room_old_gm_link.default_avatar_is_user
            old_gm_avatar = room_old_gm_link.avatar_id_id if room_old_gm_link.avatar_id else 0
            user_id = gm_user_id
            avatar_is_user = old_gm_avatar_is_user
            avatar = old_gm_avatar
            make_user_room_link(swroom_id, user_id, False, False, avatar_is_user, avatar)
            return redirect(info_url, swroom_id)
        elif request.method == "POST" and "ban_real" in request.POST:
            make_user_room_link(swroom_id, player_id, False, True, player_avatar_is_user, player_avatar)
            return redirect(info_url, swroom_id)
        elif request.method == "POST" and "unban_real" in request.POST:
            make_user_room_link(swroom_id, player_id, False, False, player_avatar_is_user, player_avatar)
            return redirect(info_url, swroom_id)
        # Room Info Functions
        elif request.method == "POST" and "restore_real" in request.POST:
            room.disabled = 0
            room.save()
            return redirect(info_url, swroom_id)
        elif request.method == "POST" and "archive_real" in request.POST:
            room.disabled = 1
            room.save()
            return redirect(info_url, swroom_id)
        # Regular Room functions
        elif request.method == "POST" and "chat" in request.POST:
            kwargs = self.get_form_kwargs()
            chat_form = SW_Room_Chat_Form(**kwargs)
            chat_text = chat_form.data['chat_text']

            # grab any dice stuff not submitted and keep around
            dice_form = SW_Dice_Roll(request.POST)
            if 'gendice' in self.template_name:
                dice_form.num_force_dice = 0
            get_dice_carryover(request, dice_form)

            if chat_text != "":
                new_chat = read_chat(chat_form, avatar, swroom_id, current_user, chat_text, image_url)
                new_chat.save()
                return redirect(room_url, swroom_id)
            else:
                return redirect(room_url, swroom_id)
        elif request.method == "POST" and "add_dark" in request.POST:
            print(request.POST)
            # grab any chat stuff not submitted and keep around
            kwargs = self.get_form_kwargs()
            chat_form = SW_Room_Chat_Form(**kwargs)
            get_chat_carryover(request, chat_form, current_user_id)

            # grab any dice stuff not submitted and keep around
            dice_form = SW_Dice_Roll(request.POST)
            if 'gendice' in self.template_name:
                dice_form.num_force_dice = 0
            get_dice_carryover(request, dice_form)

            caption = " added a GM story point." if genesys else " added a DARK destiny point."
            delta_light = 0
            delta_dark = 1
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect(room_url, swroom_id)
        elif request.method == "POST" and "rem_dark" in request.POST:
            # grab any chat stuff not submitted and keep around
            kwargs = self.get_form_kwargs()
            chat_form = SW_Room_Chat_Form(**kwargs)
            get_chat_carryover(request, chat_form, current_user_id)

            # grab any dice stuff not submitted and keep around
            dice_form = SW_Dice_Roll(request.POST)
            if 'gendice' in self.template_name:
                dice_form.num_force_dice = 0
            get_dice_carryover(request, dice_form)

            caption = " removed a GM story point." if genesys else " removed a DARK destiny point."
            delta_light = 0
            delta_dark = -1
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect(room_url, swroom_id)
        elif request.method == "POST" and "use_dark" in request.POST:
            print(request.POST)
            # grab any chat stuff not submitted and keep around
            kwargs = self.get_form_kwargs()
            chat_form = SW_Room_Chat_Form(**kwargs)
            get_chat_carryover(request, chat_form, current_user_id)

            # grab any dice stuff not submitted and keep around
            dice_form = SW_Dice_Roll(request.POST)
            if 'gendice' in self.template_name:
                dice_form.num_force_dice = 0
            get_dice_carryover(request, dice_form)

            caption = " used a GM story point." if genesys else " used a DARK destiny point."
            delta_light = 1
            delta_dark = -1
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect(room_url, swroom_id)
        elif request.method == "POST" and "add_light" in request.POST:
            # grab any chat stuff not submitted and keep around
            kwargs = self.get_form_kwargs()
            chat_form = SW_Room_Chat_Form(**kwargs)
            get_chat_carryover(request, chat_form, current_user_id)

            # grab any dice stuff not submitted and keep around
            dice_form = SW_Dice_Roll(request.POST)
            if 'gendice' in self.template_name:
                dice_form.num_force_dice = 0
            get_dice_carryover(request, dice_form)

            caption = " added a Player story point." if genesys else " added a LIGHT destiny point."
            delta_light = 1
            delta_dark = 0
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect(room_url, swroom_id)
        elif request.method == "POST" and "rem_light" in request.POST:
            # grab any chat stuff not submitted and keep around
            kwargs = self.get_form_kwargs()
            chat_form = SW_Room_Chat_Form(**kwargs)
            get_chat_carryover(request, chat_form, current_user_id)

            # grab any dice stuff not submitted and keep around
            dice_form = SW_Dice_Roll(request.POST)
            if 'gendice' in self.template_name:
                dice_form.num_force_dice = 0
            get_dice_carryover(request, dice_form)

            caption = " removed a Player story point." if genesys else " removed a LIGHT destiny point."
            delta_light = -1
            delta_dark = 0
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect(room_url, swroom_id)
        elif request.method == "POST" and "use_light" in request.POST:
            # grab any chat stuff not submitted and keep around
            kwargs = self.get_form_kwargs()
            chat_form = SW_Room_Chat_Form(**kwargs)
            get_chat_carryover(request, chat_form, current_user_id)

            # grab any dice stuff not submitted and keep around
            dice_form = SW_Dice_Roll(request.POST)
            if 'gendice' in self.template_name:
                dice_form.num_force_dice = 0
            get_dice_carryover(request, dice_form)

            caption = " used a Player story point." if genesys else " used a LIGHT destiny point."
            delta_light = -1
            delta_dark = 1
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect(room_url, swroom_id)
        elif request.method == "POST" and "clear_destiny" in request.POST:
            # grab any chat stuff not submitted and keep around
            kwargs = self.get_form_kwargs()
            chat_form = SW_Room_Chat_Form(**kwargs)
            get_chat_carryover(request, chat_form, current_user_id)

            # grab any dice stuff not submitted and keep around
            dice_form = SW_Dice_Roll(request.POST)
            if 'gendice' in self.template_name:
                dice_form.num_force_dice = 0
            get_dice_carryover(request, dice_form)

            destiny = SWRoomDestiny.objects.filter(room_id=room)[0]
            light = destiny.light_pips
            dark = destiny.dark_pips
            caption = " removed all story points." if genesys else " removed all destiny points."
            delta_light = -1 * light
            delta_dark = -1 * dark
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect(room_url, swroom_id)
        elif request.method == "POST" and ("roll_dice" in request.POST or "roll_dice_secret" in request.POST):
            # grab any chat stuff not submitted and keep around
            kwargs = self.get_form_kwargs()
            chat_form = SW_Room_Chat_Form(**kwargs)
            get_chat_carryover(request, chat_form, current_user_id)

            dice_form = SW_Dice_Roll(request.POST)
            secret_roll = "roll_dice_secret" in request.POST

            if dice_form.is_valid():
                if genesys:
                    dice_form.cleaned_data['num_force_dice'] = 0
                dice_pool = read_dice(dice_form)
                total_dice = dice_pool['total_dice']
                del dice_pool['total_dice']
                valid_pool = dice_pool['valid_pool']
                del dice_pool['valid_pool']
                caption = dice_pool['caption']

                # if caption or total_dice > 0:
                if valid_pool:
                    kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "image_url": image_url, }
                    kwargs.update(dice_pool)
                    kwargs.update({"secret_roll": secret_roll})
                    save_dice_pool(**kwargs)
                else:
                    pass
            else:
                return redirect(room_url, swroom_id)

            return redirect(room_url, swroom_id)
        else:
            print(request.POST)

    def get(self, request, *args, **kwargs):
        # kwargs = self.get_form_kwargs()
        swroom_id = self.kwargs['swroom_id']

        gen_path = 'gendice' in request.path
        poly_path = 'polydice' in request.path
        myz_path = 'myzdice' in request.path
        sw_path = 'swdice' in request.path

        try:
            room = SWRoom.objects.get(pk=swroom_id)
        except SWRoom.DoesNotExist:
            request.session['bad_room_url'] = 'url'
            request.session['bad_room'] = swroom_id
            if gen_path:
                return redirect('gendice:bad_room')
            elif poly_path:
                return redirect('polydice:bad_room')
            elif myz_path:
                return redirect('myzdice:bad_room')
            else:
                return redirect('swdice:bad_room')

        gendice = room.genesys
        polydice = room.polydice
        myzdice = room.myzdice
        swdice = not gendice and not polydice and not myzdice

        # Redirect if wrong room url
        if gendice and not gen_path:
            return redirect('gendice:genroom', swroom_id)
        elif polydice and not poly_path:
            return redirect('polydice:polyroom', swroom_id)
        elif myzdice and not myz_path:
            return redirect('myzdice:myzroom', swroom_id)
        elif swdice and not sw_path:
            return redirect('swdice:swroom', swroom_id)
        else:
            pass

        # create appropriate redirects
        if gendice:
            room_url = 'gendice:genroom'
            hub_url = 'gendice:confluence'
            info_url = 'gendice:genroom_info'
            enter_url = 'gendice:enter_passcode_room'
        elif polydice:
            room_url = 'polydice:polyroom'
            hub_url = 'polydice:dungeon'
            info_url = 'polydice:polyroom_info'
            enter_url = 'polydice:enter_passcode_room'
        elif myzdice:
            room_url = 'myzdice:myzroom'
            hub_url = 'myzdice:dungeon'
            info_url = 'myzdice:myzroom_info'
            enter_url = 'myzdice:enter_passcode_room'
        else:
            room_url = 'swdice:swroom'
            hub_url = 'swdice:dockingbay'
            info_url = 'swdice:swroom_info'
            enter_url = 'swdice:enter_passcode_room'

        viewing_player_info = "player" in self.template_name
        viewing_basic_room = "info" not in self.template_name

        room_is_open = room.open_to_all
        room_users_link_list = SWRoomToUser.objects.filter(room_id_id=swroom_id)
        gm_link = room_users_link_list.filter(game_master=1)
        if len(gm_link) > 0:  # this should ALWAYS be true
            gm_id = gm_link[0].user_id_id
        else:
            gm_id = ""  # this needs to raise an error
        current_user_id = request.user.id
        user_to_room_link_candidate = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)
        if len(user_to_room_link_candidate) > 0:
            user_to_room_link = user_to_room_link_candidate[0]
        else:
            user_to_room_link = False

        # testing whether a user should be able to view a page
        if user_to_room_link:
            if user_to_room_link.banned:
                request.session['problem'] = "You have been banned from that room."
                return redirect(hub_url)
            elif viewing_player_info and not user_to_room_link.game_master:
                return redirect(info_url, swroom_id)
            else:
                pass
        else:
            if room_is_open and viewing_basic_room:
                make_user_room_link(swroom_id, current_user_id, False, False, True, 0)
                # should_be_here = True
            elif room_is_open:
                make_user_room_link(swroom_id, current_user_id, False, False, True, 0)
                return redirect(room_url, swroom_id)
            else:  # room is not open, player has not been there
                return redirect(enter_url, swroom_id)  # update

        # player should be here, if they got through all of the above filters
        user_to_room_link_candidate = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)
        if len(user_to_room_link_candidate) > 0:
            user_to_room_link = user_to_room_link_candidate[0]
        if not user_to_room_link.default_avatar_is_user:
            avatar_id = user_to_room_link.avatar_id_id
            default_avatar = Avatar.objects.filter(pk=avatar_id)[0]
            if not default_avatar.deleted:
                name_in_room = default_avatar.avatar_name
                use_pdf_char = default_avatar.use_char_sheet == 1
                use_gen_char = default_avatar.use_char_sheet == 2
                has_char = (use_pdf_char + use_gen_char) > 0
                char_pdf = default_avatar.char_pdf if use_pdf_char else ""
                avatar_id = default_avatar.id

                if default_avatar.avatar_url_image:
                    icon_src = default_avatar.avatar_url_image
                else:
                    icon_src = ""
            else:
                use_pdf_char = False
                use_gen_char = False
                has_char = False
                char_pdf = ""
                avatar_id = 0
                if request.user.userprofile.user_first_name:
                    name_in_room = request.user.userprofile.user_first_name
                else:
                    name_in_room = request.user.username
                if request.user.userprofile.user_url_image:
                    icon_src = request.user.userprofile.user_url_image
                else:
                    icon_src = ""
        else:
            use_pdf_char = False
            use_gen_char = False
            has_char = False
            char_pdf = ""
            avatar_id = 0
            if request.user.userprofile.user_first_name:
                name_in_room = request.user.userprofile.user_first_name
            else:
                name_in_room = request.user.username
            if request.user.userprofile.user_url_image:
                icon_src = request.user.userprofile.user_url_image
            else:
                icon_src = ""

        if not SWRoomDestiny.objects.filter(room_id_id=swroom_id):          # can remove next re-initialization
            destiny = SWRoomDestiny()                                       # maybe not
            destiny.room_id_id = swroom_id
            destiny.dark_pips = 0
            destiny.light_pips = 0
            destiny.save()
        room_destiny = SWRoomDestiny.objects.get(room_id=swroom_id)

        if len(gm_link) > 0:
            player_is_gm = 1 if gm_id == request.user.id else 0
        else:
            player_is_gm = 0

        light_pips = room_destiny.light_pips
        dark_pips = room_destiny.dark_pips

        if viewing_basic_room:
            kwargs = self.get_form_kwargs()

            # instantiate carryover data
            initial_args_chat = {}
            if 'chat_carryover' in request.session:
                initial_args_chat['chat_text'] = request.session['chat_carryover']
                del request.session['chat_carryover']
            if 'recipient_carryover' in request.session:
                initial_args_chat['recipient'] = request.session['recipient_carryover']
                del request.session['recipient_carryover']
                start_whisper = True
            else:
                start_whisper = False
            if 'dice_pool_carryover' in request.session:
                initial_args = request.session['dice_pool_carryover']
                del request.session['dice_pool_carryover']
            else:
                initial_args = {}

            dice_form = SW_Dice_Roll(initial_args)  # update
            chat_form = SW_Room_Chat_Form(initial_args_chat, **kwargs)

            chats_all = SWRoomChat.objects.filter(room_id_id=swroom_id).order_by('-created_on')
            chat_log = []
            for chat in chats_all[:50]:
                if not room_users_link_list.filter(user_id=chat.user)[0].banned:
                    chat_log.append(chat)
            if len(chat_log) > 0:
                last_chat_time = chat_log[0].created_on
            else:
                last_chat_time = room.created_on

            actions_all = SWDicePool.objects.filter(swroom_id=swroom_id).order_by('-created')
            action_log = []
            for action in actions_all[:50]:
                if not room_users_link_list.filter(user_id=action.user)[0].banned:
                    action_log.append(action)
            if len(action_log) > 0:
                last_action_time = action_log[0].created
            else:
                last_action_time = room.created_on

            update_times = UpdateTimes(last_action_time, last_chat_time)

            args = {'room': room, 'name_in_room': name_in_room, 'icon': icon_src, 'player_is_gm': player_is_gm,
                    'room_number': swroom_id, 'chat_log': chat_log, 'chat_form': chat_form, 'destiny': room_destiny,
                    'light_pips': light_pips, 'dark_pips': dark_pips, 'action_log': action_log,
                    'dice_form': dice_form, 'users_in_room': room_users_link_list,
                    'update_times': update_times, 'viewing_basic_room': viewing_basic_room,
                    'start_whisper': start_whisper, 'use_pdf_char': use_pdf_char, 'use_gen_char': use_gen_char,
                    'has_char': has_char, 'char_pdf': char_pdf, 'avatar_id': avatar_id,
                    }  # 'start_secret_roll': start_secret_roll

        elif viewing_player_info:
            player_id = self.kwargs['player_id']
            try:
                player = VanLevyUser.objects.get(pk=player_id)
            except VanLevyUser.DoesNotExist:
                return redirect(info_url, swroom_id)

            chat_log = SWRoomChat.objects.filter(room_id_id=swroom_id, user_id=player_id).order_by('-created_on')
            action_log = SWDicePool.objects.filter(swroom_id=swroom_id, user_id=player_id).order_by('-created')
            args = {'room': room, 'name_in_room': name_in_room, 'icon': icon_src, 'player_is_gm': player_is_gm,
                    'room_number': swroom_id, 'chat_log': chat_log, 'destiny': room_destiny,
                    'light_pips': light_pips, 'dark_pips': dark_pips, 'action_log': action_log,
                    'users_in_room': room_users_link_list, 'player_id': player_id,
                    'viewing_basic_room': viewing_basic_room}

        else:
            chats_all = SWRoomChat.objects.filter(room_id_id=swroom_id).order_by('-created_on')
            chat_log = []
            for chat in chats_all:
                if not room_users_link_list.filter(user_id=chat.user)[0].banned:
                    chat_log.append(chat)
            actions_all = SWDicePool.objects.filter(swroom_id=swroom_id).order_by('-created')
            action_log = []
            for action in actions_all:
                if not room_users_link_list.filter(user_id=action.user)[0].banned:
                    action_log.append(action)
            args = {'room': room, 'name_in_room': name_in_room, 'icon': icon_src, 'player_is_gm': player_is_gm,
                    'room_number': swroom_id, 'chat_log': chat_log, 'destiny': room_destiny,
                    'light_pips': light_pips, 'dark_pips': dark_pips, 'action_log': action_log,
                    'users_in_room': room_users_link_list, 'viewing_basic_room': viewing_basic_room}

        return render(request, self.template_name, args)

