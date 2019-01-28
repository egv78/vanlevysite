from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import FormMixin
from .models import SWRoomToUser, SWRoomChat, SWRoom, SWRoomDestiny, SWDicePool
from .forms import Make_SW_Room, Enter_SW_Room, SW_Room_Chat_Form, SW_Dice_Roll
from .dice import *
from accounts.models import VanLevyUser, Avatar
from django.template.defaulttags import register
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


def make_user_room_link(room_id, user_id, gm=False, banned=False, avatar_is_user=True, avatar=0):
    if SWRoomToUser.objects.filter(user_id_id=user_id, room_id_id=room_id):
        link_instance = SWRoomToUser.objects.filter(user_id_id=user_id, room_id_id=room_id)[0]
    else:
        link_instance = SWRoomToUser()
    now = datetime.datetime.now()
    link_instance.room_id_id = room_id
    link_instance.user_id = VanLevyUser(pk=user_id)
    link_instance.admitted = True
    link_instance.game_master = gm
    link_instance.banned = banned
    link_instance.date_link_created = now
    link_instance.date_admitted = now
    link_instance.default_avatar_is_user = avatar_is_user
    # if avatar is None:
    #     avatar = 0
    print("Make Link")
    print(avatar)
    if int(avatar) == 0:
        link_instance.avatar_id_id = ""
        print("blank")
    else:
        link_instance.avatar_id_id = int(avatar)
        print(avatar)

    if gm:
        link_instance.date_made_gm = now
    link_instance.save()


def save_dice_pool(user, avatar, room, image_url, caption="",
                   num_boost_dice=0, num_ability_dice=0, num_proficiency_dice=0,
                   num_setback_dice=0, num_difficulty_dice=0, num_challenge_dice=0, num_force_dice=0,
                   additional_triumph=0, additional_despair=0, additional_success=0, additional_failure=0,
                   additional_advantage=0, additional_threat=0,
                   additional_light_pips=0, additional_dark_pips=0,
                   num_numerical_dice=0, numerical_dice_sides=0, just_caption=True):
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
    numerical_die = Die("Numerical", numerical_meanings, "")
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


def about(request):
    template_name = 'swdice/about_swdiceroller.html'
    return render(request, template_name)


def make_sw_room(request):
    if request.method == 'POST':
        form = Make_SW_Room(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            now = datetime.datetime.now()
            instance.created_on = now
            instance.save()
            user_id = request.user.id
            room_id = instance.id
            make_user_room_link(room_id, user_id, True, False, True, 0)
            destiny = SWRoomDestiny()
            destiny.room_id_id = room_id
            destiny.dark_pips = 0
            destiny.light_pips = 0
            destiny.save()
            return redirect('swdice:dockingbay')
        else:
            args = {'form': form}
            return render(request, 'swdice/make_swroom.html', args)
    else:
        now = datetime.datetime.now()
        user_id = request.user.id
        initial_args = {'open_to_all': False, 'created_on': now, 'created_by': user_id}
        form = Make_SW_Room(initial_args)
        args = {'form': form}
        return render(request, 'swdice/make_swroom.html', args)


class DockingBay(FormMixin, TemplateView):
    form_class = Enter_SW_Room

    def get_form_kwargs(self):
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
                my_avatars_choices.append((avatar.id, avatar.avatar_name))
        kwargs['avatar_list'] = my_avatars_choices
        return kwargs

    # if request.method == 'GET'
    def get(self, request, *args, **kwargs):
        try:
            room_id = self.kwargs['swroom_id']
        except:
            room_id = ""

        kwargs = self.get_form_kwargs()
        avatars = dict(kwargs['avatar_list'])
        current_user_id = self.request.user.id
        my_rooms_to_user_list = SWRoomToUser.objects.filter(user_id_id=current_user_id, banned=0).order_by(
            '-admitted')
        my_rooms_list = []
        my_avatars_list = {}

        for room in my_rooms_to_user_list:
            my_rooms_list += SWRoom.objects.filter(pk=room.room_id_id)
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
        args = {'form': form, 'my_rooms_list': my_rooms_list, 'my_avatars_list': my_avatars_list, 'room_id': room_id}

        return render(request, self.template_name, args)

    # if request.method == 'POST':
    def post(self, request, **kwargs):
        kwargs = self.get_form_kwargs()
        form = Enter_SW_Room(**kwargs)
        if form.is_valid():
            swroom_id = form.cleaned_data['room_number']
            passcode_candidate = form.cleaned_data['passcode']
            avatar_id = form.cleaned_data['default_avatar']
            instance = form.save(commit=False)

            use_user_id = True if int(avatar_id) == 0 else False

            try:
                room = SWRoom.objects.get(pk=swroom_id)
                my_rooms_to_user_list = SWRoomToUser.objects.filter(user_id_id=self.request.user.id,
                                                                    banned=0).order_by('-admitted')
                my_rooms_list = []
                for my_room in my_rooms_to_user_list:
                    my_rooms_list += SWRoom.objects.filter(pk=my_room.room_id_id)
                been_there = my_rooms_to_user_list.filter(room_id_id=swroom_id)
                if been_there and not been_there[0].banned and been_there[0].avatar_id_id == avatar_id:
                    return redirect('swdice:swroom', swroom_id)
                elif been_there and not been_there[0].banned:
                    link_instance = been_there[0]
                    link_instance.avatar_id_id = avatar_id if int(avatar_id) > 0 else ""
                    link_instance.default_avatar_is_user = 1 if int(avatar_id) == 0 else 0
                    link_instance.save()
                    # print("here")
                    return redirect('swdice:swroom', swroom_id)
                else:
                    passcode_correct = room.passcode
                    room_is_open = room.open_to_all
                    if room_is_open or (passcode_candidate == passcode_correct):
                        game_master = False
                        banned = False
                        # print(swroom_id, request.user.id, game_master, banned, use_user_id, avatar_id)
                        make_user_room_link(swroom_id, request.user.id, game_master, banned, use_user_id, avatar_id)
                        return redirect('swdice:swroom', swroom_id)
                    else:
                        return redirect('swdice:enter_passcode')

            except SWRoom.DoesNotExist:
                raise Http404("Room has not yet been created")

        else:
            # need to do error handling for form
            pass


class ViewRoom(FormMixin, TemplateView):
    template_name = 'swdice/swroom.html'

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
        current_user = self.request.user
        current_user_id = self.request.user.id
        room_to_user_link = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)[0]
        avatar = room_to_user_link.avatar_id
        if avatar is None:
            image_url = current_user.userprofile.user_image.url if current_user.userprofile.user_image else ""
        elif avatar.avatar_image:
            image_url = avatar.avatar_image.url
        else:
            image_url = ''

        if request.method == "POST" and "chat" in request.POST:
            # form = SW_Room_Chat_Form(request.POST)
            kwargs = self.get_form_kwargs()
            # print("Kwargs")
            # print(kwargs)
            form = SW_Room_Chat_Form(**kwargs)
            text = form.data['chat_text']

            if text != "":
                recipient_id = form.data['recipient']
                recipient_user = VanLevyUser.objects.filter(id=recipient_id)[0]
                room_user_link_recipient = SWRoomToUser.objects.filter(room_id_id=swroom_id, user_id=recipient_user)[0]
                recipient_avatar = room_user_link_recipient.avatar_id
                is_private = not (recipient_user == current_user)
                new_chat = SWRoomChat()
                new_chat.room_id_id = swroom_id
                new_chat.chat_text = text
                new_chat.user = current_user
                new_chat.avatar = avatar
                new_chat.image_url = image_url
                new_chat.is_private = is_private
                new_chat.recipient = recipient_user if is_private else None
                new_chat.recipient_avatar = recipient_avatar
                new_chat.save()
                return redirect('swdice:swroom', swroom_id)
            else:
                return redirect('swdice:swroom', swroom_id)
        elif request.method == "POST" and "add_dark" in request.POST:
            caption_text = " added a DARK destiny point."
            delta_light = 0
            delta_dark = 1
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption_text,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect('swdice:swroom', swroom_id)
        elif request.method == "POST" and "rem_dark" in request.POST:
            caption_text = " removed a DARK destiny point."
            delta_light = 0
            delta_dark = -1
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption_text,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect('swdice:swroom', swroom_id)
        elif request.method == "POST" and "use_dark" in request.POST:
            caption_text = " used a DARK destiny point."
            delta_light = 1
            delta_dark = -1
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption_text,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect('swdice:swroom', swroom_id)
        elif request.method == "POST" and "add_light" in request.POST:
            caption_text = " added a LIGHT destiny point."
            delta_light = 1
            delta_dark = 0
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption_text,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect('swdice:swroom', swroom_id)
        elif request.method == "POST" and "rem_light" in request.POST:
            caption_text = " removed a LIGHT destiny point."
            delta_light = -1
            delta_dark = 0
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption_text,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect('swdice:swroom', swroom_id)
        elif request.method == "POST" and "use_light" in request.POST:
            caption_text = " used a LIGHT destiny point."
            delta_light = -1
            delta_dark = 1
            kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption_text,
                      "image_url": image_url, "delta_light": delta_light, "delta_dark": delta_dark}
            change_destiny(**kwargs)
            return redirect('swdice:swroom', swroom_id)
        elif request.method == "POST" and "roll_dice" in request.POST:
            form = SW_Dice_Roll(request.POST)
            print(form.errors)
            if form.is_valid():
                boost_dice = form.cleaned_data['num_boost_dice']
                ability_dice = form.cleaned_data['num_ability_dice']
                proficiency_dice = form.cleaned_data['num_proficiency_dice']
                setback_dice = form.cleaned_data['num_setback_dice']
                difficulty_dice = form.cleaned_data['num_difficulty_dice']
                challenge_dice = form.cleaned_data['num_challenge_dice']
                force_dice = form.cleaned_data['num_force_dice']
                numerical_sides = form.cleaned_data['numerical_dice_sides']
                numerical_dice = form.cleaned_data['num_numerical_dice']
                caption_text = form.cleaned_data['caption']
                additional_triumph = form.cleaned_data['additional_triumph']
                additional_despair = form.cleaned_data['additional_despair']
                additional_success = form.cleaned_data['additional_success']
                additional_failure = form.cleaned_data['additional_failure']
                additional_advantage = form.cleaned_data['additional_advantage']
                additional_threat = form.cleaned_data['additional_threat']
                additional_light_pips = form.cleaned_data['additional_light_pips']
                additional_dark_pips = form.cleaned_data['additional_dark_pips']
                total_dice = (boost_dice + ability_dice + proficiency_dice + force_dice +
                              setback_dice + difficulty_dice + challenge_dice + numerical_dice +
                              additional_triumph + additional_despair + additional_success + additional_failure +
                              additional_advantage + additional_threat + additional_light_pips + additional_dark_pips
                              )

                if caption_text or total_dice > 0:
                    if total_dice == 0:
                        just_caption = True
                    else:
                        just_caption = False

                    kwargs = {"user": current_user, "avatar": avatar, "room": swroom_id, "caption": caption_text,
                              "image_url": image_url,
                              "num_boost_dice": boost_dice, "num_ability_dice": ability_dice,
                              "num_proficiency_dice": proficiency_dice, "num_setback_dice": setback_dice,
                              "num_difficulty_dice": difficulty_dice, "num_challenge_dice": challenge_dice,
                              "num_force_dice": force_dice, "just_caption": just_caption,
                              "num_numerical_dice": numerical_dice, "numerical_dice_sides": numerical_sides,
                              "additional_triumph": additional_triumph, "additional_despair": additional_despair,
                              "additional_success": additional_success, "additional_failure": additional_failure,
                              "additional_advantage": additional_advantage, "additional_threat": additional_threat,
                              "additional_light_pips": additional_light_pips,
                              "additional_dark_pips": additional_dark_pips,
                              }
                    save_dice_pool(**kwargs)
                else:
                    pass
            else:
                print("Form's busted")

            return redirect('swdice:swroom', swroom_id)

    def get(self, request, *args, **kwargs):
        kwargs = self.get_form_kwargs()
        swroom_id = self.kwargs['swroom_id']
        try:
            room = SWRoom.objects.get(pk=swroom_id)
            room_is_open = room.open_to_all
            room_users_link_list = SWRoomToUser.objects.filter(room_id_id=swroom_id)
            gm_link = room_users_link_list.filter(game_master=1)
            if len(gm_link) > 0:
                gm_id = gm_link[0].user_id_id
            else:
                gm_id = ""
            current_user_id = request.user.id
            user_to_room_link_candidate = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)
            if len(user_to_room_link_candidate) > 0:
                user_to_room_link = user_to_room_link_candidate[0]
            else:
                user_to_room_link = False

            if room_is_open and not user_to_room_link:
                make_user_room_link(swroom_id, current_user_id, False, False, True, 0)
                should_be_here = True
            elif not user_to_room_link:
                should_be_here = False
                return redirect('swdice:request_access')
            elif user_to_room_link.admitted and not user_to_room_link.banned:
                should_be_here = True
            elif user_to_room_link.banned:
                should_be_here = False
                return redirect('swdice:dockingbay')  # will need to change when banning implemented
            else:
                should_be_here = False
                return redirect('swdice:dockingbay')

        except SWRoom.DoesNotExist:
            raise Http404("Room has not yet been created")

        if should_be_here:
            user_to_room_link_candidate = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)
            if len(user_to_room_link_candidate) > 0:
                user_to_room_link = user_to_room_link_candidate[0]
            if not user_to_room_link.default_avatar_is_user:
                avatar_id = user_to_room_link.avatar_id_id
                default_avatar = Avatar.objects.filter(pk=avatar_id)[0]
                if not default_avatar.deleted:
                    name_in_room = default_avatar.avatar_name
                    if default_avatar.avatar_image:
                        icon_src = default_avatar.avatar_image.url
                    else:
                        icon_src = ""
                else:
                    if request.user.userprofile.user_first_name:
                        name_in_room = request.user.userprofile.user_first_name
                    else:
                        name_in_room = request.user.username
                    if request.user.userprofile.user_image:
                        icon_src = request.user.userprofile.user_image.url
                    else:
                        icon_src = ""
            else:
                if request.user.userprofile.user_first_name:
                    name_in_room = request.user.userprofile.user_first_name
                else:
                    name_in_room = request.user.username
                if request.user.userprofile.user_image:
                    icon_src = request.user.userprofile.user_image.url
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
                gm_name = "you" if gm_id == request.user.id else VanLevyUser.objects.filter(pk=gm_id)[0].username
            else:
                gm_name = "No one"
            chat_log = SWRoomChat.objects.filter(room_id_id=swroom_id).order_by('-created_on')
            action_log = SWDicePool.objects.filter(swroom_id=swroom_id).order_by('-created')[:100]
            form = SW_Room_Chat_Form(**kwargs)
            light_pips = room_destiny.light_pips
            dark_pips = room_destiny.dark_pips
            dice_form = SW_Dice_Roll()

            args = {'room': room, 'name_in_room': name_in_room, 'icon': icon_src, 'gm_name': gm_name,
                    'room_number': swroom_id, 'chat_log': chat_log, 'form': form, 'destiny': room_destiny,
                    'light_pips': light_pips, 'dark_pips': dark_pips, 'action_log': action_log,
                    'dice_form': dice_form, 'users_in_room': room_users_link_list}
            template_name = 'swdice/swroom.html'
            return render(request, template_name, args)


class RoomInfo(FormMixin, TemplateView):
    template_name = 'swdice/swroom_info.html'

    def get(self, request, *args, **kwargs):
        # kwargs = self.get_form_kwargs()
        swroom_id = self.kwargs['swroom_id']
        try:
            room = SWRoom.objects.get(pk=swroom_id)
            room_is_open = room.open_to_all
            room_users_link_list = SWRoomToUser.objects.filter(room_id_id=swroom_id)
            gm_link = room_users_link_list.filter(game_master=1)
            if len(gm_link) > 0:
                gm_id = gm_link[0].user_id_id
            else:
                gm_id = ""
            current_user_id = request.user.id
            user_to_room_link_candidate = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)
            if len(user_to_room_link_candidate) > 0:
                user_to_room_link = user_to_room_link_candidate[0]
            else:
                user_to_room_link = False

            if room_is_open and not user_to_room_link:
                make_user_room_link(swroom_id, current_user_id, False, False, True, 0)
                should_be_here = True
            elif not user_to_room_link:
                should_be_here = False
                return redirect('swdice:request_access')
            elif user_to_room_link.admitted and not user_to_room_link.banned:
                should_be_here = True
            elif user_to_room_link.banned:
                should_be_here = False
                return redirect('swdice:dockingbay')  # will need to change when banning implemented
            else:
                should_be_here = False
                return redirect('swdice:dockingbay')

        except SWRoom.DoesNotExist:
            raise Http404("Room has not yet been created")

        if should_be_here:
            user_to_room_link_candidate = SWRoomToUser.objects.filter(user_id_id=current_user_id, room_id_id=swroom_id)
            if len(user_to_room_link_candidate) > 0:
                user_to_room_link = user_to_room_link_candidate[0]
            if not user_to_room_link.default_avatar_is_user:
                avatar_id = user_to_room_link.avatar_id_id
                default_avatar = Avatar.objects.filter(pk=avatar_id)[0]
                if not default_avatar.deleted:
                    name_in_room = default_avatar.avatar_name
                    if default_avatar.avatar_image:
                        icon_src = default_avatar.avatar_image.url
                    else:
                        icon_src = ""
                else:
                    if request.user.userprofile.user_first_name:
                        name_in_room = request.user.userprofile.user_first_name
                    else:
                        name_in_room = request.user.username
                    if request.user.userprofile.user_image:
                        icon_src = request.user.userprofile.user_image.url
                    else:
                        icon_src = ""
            else:
                if request.user.userprofile.user_first_name:
                    name_in_room = request.user.userprofile.user_first_name
                else:
                    name_in_room = request.user.username
                if request.user.userprofile.user_image:
                    icon_src = request.user.userprofile.user_image.url
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
                gm_name = "you" if gm_id == request.user.id else VanLevyUser.objects.filter(pk=gm_id)[0].username
            else:
                gm_name = "No one"
            chat_log = SWRoomChat.objects.filter(room_id_id=swroom_id).order_by('-created_on')
            action_log = SWDicePool.objects.filter(swroom_id=swroom_id).order_by('-created')
            light_pips = room_destiny.light_pips
            dark_pips = room_destiny.dark_pips

            args = {'room': room, 'name_in_room': name_in_room, 'icon': icon_src, 'gm_name': gm_name,
                    'room_number': swroom_id, 'chat_log': chat_log,  'destiny': room_destiny,
                    'light_pips': light_pips, 'dark_pips': dark_pips, 'action_log': action_log,
                    'users_in_room': room_users_link_list}
            template_name = 'swdice/swroom_info.html'
            return render(request, template_name, args)

