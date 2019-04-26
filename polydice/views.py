from django.shortcuts import render, redirect
# from django.http import Http404
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import FormMixin
from django.template.defaulttags import register

from accounts.models import VanLevyUser, Avatar
from swdice.dice import *
from swdice.models import SWRoomToUser, SWRoomChat, SWRoom
from swdice.forms import SW_Room_Chat_Form, SW_Dice_Roll
from swdice.views import make_user_room_link, get_chat_carryover, read_chat, UpdateTimes

from .forms import PolyDicePoolForm
from .models import PolyDicePool


# Filters for Jinja2
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


# Methods for use in view classes
def read_poly_dice(dice_form):
    num_d4 = dice_form.cleaned_data['num_d4']
    num_d6 = dice_form.cleaned_data['num_d6']
    num_d8 = dice_form.cleaned_data['num_d8']
    num_d10 = dice_form.cleaned_data['num_d10']
    num_d12 = dice_form.cleaned_data['num_d12']
    num_d20 = dice_form.cleaned_data['num_d20']
    num_d100 = dice_form.cleaned_data['num_d100']
    numerical_sides = dice_form.cleaned_data['numerical_dice_sides']
    numerical_dice = dice_form.cleaned_data['num_numerical_dice']
    caption = dice_form.cleaned_data['caption']
    bonus = dice_form.cleaned_data['bonus']
    total_dice = (num_d4 + num_d6 + num_d8 + num_d10 + num_d12 + num_d20 + num_d100 + numerical_dice)

    if caption or total_dice > 0:
        valid_pool = True
        if total_dice == 0:
            just_caption = True
        else:
            just_caption = False
    else:
        just_caption = False
        valid_pool = False

    dice_pool = {'caption': caption, "total_dice": total_dice, 'bonus': bonus,
                 "num_d4": num_d4, "num_d6": num_d6, "num_d8": num_d8, "num_d10": num_d10,
                 "num_d12": num_d12, "num_d20": num_d20, "num_d100": num_d100, "just_caption": just_caption,
                 "num_numerical_dice": numerical_dice, "numerical_dice_sides": numerical_sides,
                 "valid_pool": valid_pool,
                 }
    return dice_pool


def get_dice_carryover(request, dice_form):
    if dice_form.is_valid():
        dice_pool = read_poly_dice(dice_form)
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


def save_dice_pool(user, avatar, room, image_url, caption="", bonus=0,
                   num_d4=0, num_d6=0, num_d8=0, num_d10=0, num_d12=0, num_d20=0, num_d100=0,
                   num_numerical_dice=0, numerical_dice_sides=0, just_caption=True, secret_roll=False):
    new_dice_pool = PolyDicePool()
    new_dice_pool.user = user
    new_dice_pool.avatar = avatar
    new_dice_pool.swroom_id = room
    new_dice_pool.caption = caption
    new_dice_pool.image_url = image_url
    new_dice_pool.num_d4 = num_d4
    new_dice_pool.num_d6 = num_d6
    new_dice_pool.num_d8 = num_d8
    new_dice_pool.num_d10 = num_d10
    new_dice_pool.num_d12 = num_d12
    new_dice_pool.num_d20 = num_d20
    new_dice_pool.num_d100 = num_d100
    new_dice_pool.bonus = bonus
    new_dice_pool.num_numerical_dice = num_numerical_dice
    new_dice_pool.numerical_dice_sides = numerical_dice_sides
    new_dice_pool.is_just_caption = just_caption
    new_dice_pool.secret_roll = secret_roll

    d4_string, d4_results = D4.roll(num_d4)
    d6_string, d6_results = D6.roll(num_d6)
    d8_string, d8_results = D8.roll(num_d8)
    d10_string, d10_results = D10.roll(num_d10)
    d12_string, d12_results = D12.roll(num_d12)
    d20_string, d20_results = D20.roll(num_d20)
    d100_string, d100_results = D100.roll(num_d100)
    numerical_meanings = range(1, (numerical_dice_sides + 1))
    numerical_die = Die("Numerical", numerical_meanings, "")
    numerical_string, numerical_results = numerical_die.roll(num_numerical_dice)

    new_dice_pool.results_d4 = d4_string
    new_dice_pool.results_d6 = d6_string
    new_dice_pool.results_d8 = d8_string
    new_dice_pool.results_d10 = d10_string
    new_dice_pool.results_d12 = d12_string
    new_dice_pool.results_d20 = d20_string
    new_dice_pool.results_d100 = d100_string
    new_dice_pool.results_numerical = numerical_string

    new_dice_pool.results_total = d4_results + d6_results + d8_results + d10_results + d12_results + \
                                  d20_results + d100_results + numerical_results + bonus

    new_dice_pool.results_cancel = False

    new_dice_pool.save()


# View methods and classes
def about(request):
    template_name = 'polydice/about_polydiceroller.html'
    return render(request, template_name)


def error(request):
    template_name = '404_poly.html'
    return render(request, template_name)


class PolyRoomViews(FormMixin, TemplateView):

    def get_form_kwargs(self):
        swroom_id = self.kwargs['swroom_id']
        kwargs = super().get_form_kwargs()
        user_id = self.request.user.id
        room_users_link_list = SWRoomToUser.objects.filter(room_id_id=swroom_id).exclude(user_id_id=user_id)

        if room_users_link_list:
            recipients_list = [(self.request.user.id, "Send to all")]  # self as recipient = key for not private
            for user_in_room in room_users_link_list:
                if not user_in_room.banned:
                    user_name = user_in_room.user_id.username
                    if user_in_room.default_avatar_is_user:
                        name_in_room = "themself"
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

        gendice = room.genesys
        polydice = room.polydice
        myzdice = room.myzdice
        swdice = not gendice and not polydice and not myzdice

        if gendice:
            room_url = 'gendice:genroom'
            info_url = 'gendice:genroom_info'
        elif polydice:
            room_url = 'polydice:polyroom'
            info_url = 'polydice:polyroom_info'
        elif myzdice:
            room_url = 'myzdice:myzroom'
            info_url = 'myzdice:myzroom_info'
        else:
            room_url = 'swdice:swroom'
            info_url = 'swdice:swroom_info'

        viewing_player_info = "player" in self.template_name
        viewing_room_info = "info" in self.template_name

        # Player Info view functions
        if viewing_player_info:
            player_id = self.kwargs['player_id']
            gm_user_id = self.request.user.id
            room_player_link = SWRoomToUser.objects.filter(user_id_id=player_id, room_id_id=swroom_id)[0]
            player_avatar_is_user = room_player_link.default_avatar_is_user
            player_avatar = int(room_player_link.avatar_id_id) if room_player_link.avatar_id else 0

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
            else:
                return redirect(info_url, swroom_id)

        # Room Info Functions
        elif viewing_room_info:
            if request.method == "POST" and "restore_real" in request.POST:
                room.disabled = 0
                room.save()
                return redirect(info_url, swroom_id)
            elif request.method == "POST" and "archive_real" in request.POST:
                room.disabled = 1
                room.save()
                return redirect(info_url, swroom_id)
            else:
                return redirect(info_url, swroom_id)

        # Regular Room functions
        else:
            room_to_user_link = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)[0]
            avatar = room_to_user_link.avatar_id
            if avatar is None:
                image_url = current_user.userprofile.user_url_image if current_user.userprofile.user_url_image else ""
            elif avatar.avatar_url_image:
                image_url = avatar.avatar_url_image
            else:
                image_url = ''

            if request.method == "POST" and "chat" in request.POST:
                kwargs = self.get_form_kwargs()
                chat_form = SW_Room_Chat_Form(**kwargs)
                chat_text = chat_form.data['chat_text']

                # grab any dice stuff not submitted and keep around
                dice_form = PolyDicePoolForm(request.POST)
                get_dice_carryover(request, dice_form)

                if chat_text != "":
                    new_chat = read_chat(chat_form, avatar, swroom_id, current_user, chat_text, image_url)
                    new_chat.save()
                    return redirect(room_url, swroom_id)
                else:
                    return redirect(room_url, swroom_id)

            elif request.method == "POST" and ("roll_dice" in request.POST or "roll_dice_secret" in request.POST):
                # grab any chat stuff not submitted and keep around
                kwargs = self.get_form_kwargs()
                chat_form = SW_Room_Chat_Form(**kwargs)
                get_chat_carryover(request, chat_form, current_user_id)

                dice_form = PolyDicePoolForm(request.POST)
                secret_roll = "roll_dice_secret" in request.POST

                if dice_form.is_valid():
                    if gendice:
                        dice_form.cleaned_data['num_force_dice'] = 0
                    dice_pool = read_poly_dice(dice_form)
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
                    print("Form's busted")
                    return redirect(room_url, swroom_id)

                return redirect(room_url, swroom_id)

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
                if default_avatar.avatar_url_image:
                    icon_src = default_avatar.avatar_url_image
                else:
                    icon_src = ""
            else:
                if request.user.userprofile.user_first_name:
                    name_in_room = request.user.userprofile.user_first_name
                else:
                    name_in_room = request.user.username
                if request.user.userprofile.user_url_image:
                    icon_src = request.user.userprofile.user_url_image
                else:
                    icon_src = ""
        else:
            if request.user.userprofile.user_first_name:
                name_in_room = request.user.userprofile.user_first_name
            else:
                name_in_room = request.user.username
            if request.user.userprofile.user_url_image:
                icon_src = request.user.userprofile.user_url_image
            else:
                icon_src = ""

        if len(gm_link) > 0:
            player_is_gm = 1 if gm_id == request.user.id else 0
        else:
            player_is_gm = 0

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

            dice_form = PolyDicePoolForm(initial_args)  # update
            chat_form = SW_Room_Chat_Form(initial_args_chat, **kwargs)

            chats_all = SWRoomChat.objects.filter(room_id_id=swroom_id).order_by('-created_on')
            chat_log = []
            for chat in chats_all[:100]:
                if not room_users_link_list.filter(user_id=chat.user)[0].banned:
                    chat_log.append(chat)
            if len(chat_log) > 0:
                last_chat_time = chat_log[0].created_on
            else:
                last_chat_time = room.created_on

            actions_all = PolyDicePool.objects.filter(swroom_id=swroom_id).order_by('-created')
            action_log = []
            for action in actions_all[:100]:
                if not room_users_link_list.filter(user_id=action.user)[0].banned:
                    action_log.append(action)
            if len(action_log) > 0:
                last_action_time = action_log[0].created
            else:
                last_action_time = room.created_on

            update_times = UpdateTimes(last_action_time, last_chat_time)

            args = {'room': room, 'name_in_room': name_in_room, 'icon': icon_src, 'player_is_gm': player_is_gm,
                    'room_number': swroom_id, 'chat_log': chat_log, 'chat_form': chat_form, 'action_log': action_log,
                    'dice_form': dice_form, 'users_in_room': room_users_link_list,
                    'update_times': update_times, 'viewing_basic_room': viewing_basic_room,
                    'start_whisper': start_whisper, }

        elif viewing_player_info:
            player_id = self.kwargs['player_id']
            try:
                player = VanLevyUser.objects.get(pk=player_id)
            except VanLevyUser.DoesNotExist:
                return redirect(info_url, swroom_id)

            chat_log = SWRoomChat.objects.filter(room_id_id=swroom_id, user_id=player_id).order_by('-created_on')
            action_log = PolyDicePool.objects.filter(swroom_id=swroom_id, user_id=player_id).order_by('-created')
            args = {'room': room, 'name_in_room': name_in_room, 'icon': icon_src, 'player_is_gm': player_is_gm,
                    'room_number': swroom_id, 'chat_log': chat_log, 'action_log': action_log,
                    'users_in_room': room_users_link_list, 'player_id': player_id,
                    'viewing_basic_room': viewing_basic_room}

        else:
            chats_all = SWRoomChat.objects.filter(room_id_id=swroom_id).order_by('-created_on')
            chat_log = []
            for chat in chats_all:
                if not room_users_link_list.filter(user_id=chat.user)[0].banned:
                    chat_log.append(chat)
            actions_all = PolyDicePool.objects.filter(swroom_id=swroom_id).order_by('-created')
            action_log = []
            for action in actions_all:
                if not room_users_link_list.filter(user_id=action.user)[0].banned:
                    action_log.append(action)
            args = {'room': room, 'name_in_room': name_in_room, 'icon': icon_src, 'player_is_gm': player_is_gm,
                    'room_number': swroom_id, 'chat_log': chat_log, 'action_log': action_log,
                    'users_in_room': room_users_link_list, 'viewing_basic_room': viewing_basic_room}

        return render(request, self.template_name, args)
