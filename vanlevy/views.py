from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.template.defaulttags import register
from django.core.mail import send_mail, BadHeaderError

from django.conf import settings  # this is actually the settings of this project
from swdice.models import SWRoomToUser, SWRoom
from accounts.models import VanLevyUser, Avatar
from .forms import ContactForm, AREA_CHOICES, ISSUE_CHOICES

import datetime


# Filters for views
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_range(value):
    return range(value)


# classes and methods used by views
class TempRoom:
    def __init__(self, room_name, avatar, gm, id):
        self.room_name = room_name
        self.avatar = avatar
        self.gm = gm
        self.id = id


# views
def vl_home_view(request):
    if 'contact_message' in request.session:
        contact_message = request.session['contact_message']
        del request.session['contact_message']
        args = {'message': contact_message}
    else:
        args = {}
    template_name = 'vanlevy/vl_home.html'
    return render(request, template_name, args)


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
    template_name = 'vanlevy/vl_dice_rollers.html'
    return render(request, template_name)


def vl_terms_view(request):
    template_name = 'vanlevy/vl_terms.html'
    return render(request, template_name)


def vl_error(request):
    template_name = '404_vl.html'
    return render(request, template_name)


def personal_portal(request):
    if 'requested_url' in request.session:
        requested_url = request.session['requested_url']
        del request.session['requested_url']
        return redirect(requested_url)

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
    number_rooms = 5
    my_sw_rooms_list = []
    my_gen_rooms_list = []
    my_poly_rooms_list = []
    my_myz_rooms_list = []

    for room in my_rooms_reversed_list:
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
                name_in_room = Avatar.objects.filter(user_id=current_user_id, id=room.avatar_id_id)[0]
            except:
                name_in_room = user_name
        new_room = TempRoom(room_name, name_in_room, gm, room_id)
        if this_room.genesys:
            if len(my_gen_rooms_list) < number_rooms and not this_room.disabled:
                my_gen_rooms_list.append(new_room)
        elif this_room.polydice:
            if len(my_poly_rooms_list) < number_rooms and not this_room.disabled:
                my_poly_rooms_list.append(new_room)
        elif this_room.myzdice:
            if len(my_myz_rooms_list) < number_rooms and not this_room.disabled:
                my_myz_rooms_list.append(new_room)
        else:
            if len(my_sw_rooms_list) < number_rooms and not this_room.disabled:
                my_sw_rooms_list.append(new_room)

    outline_button = request.user.userprofile.user_first_name and request.user.userprofile.user_url_image

    template_name = 'vanlevy/vl_portal.html'
    args = {'user': request.user, 'my_sw_rooms_list': my_sw_rooms_list, 'my_gen_rooms_list': my_gen_rooms_list,
            'my_poly_rooms_list': my_poly_rooms_list, 'my_myz_rooms_list': my_myz_rooms_list,
            'my_avatars_list': my_avatars, 'has_avatars': has_avatars, 'number_rooms': number_rooms,
            'outline_button': outline_button}

    if 'contact_message' in request.session:
        contact_message = request.session['contact_message']
        del request.session['contact_message']
        args.update({'message': contact_message})
    return render(request, template_name, args)


class ContactPage(TemplateView, FormView):
    def get(self, request, *args, **kwargs):
        timestamp = datetime.datetime.now()
        if request.user.is_authenticated:
            initial_args = {'created_on': timestamp, 'user': request.user}
        else:
            initial_args = {'created_on': timestamp}
        contact_form = ContactForm(initial=initial_args)
        args = {'contact_form': contact_form}
        template_name = 'vanlevy/vl_contact.html'
        return render(request, template_name, args)

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        if request.user.is_authenticated:
            form = ContactForm(request.POST, instance=request.user)
            logged_in = True
            username = request.user.username
            user_id = request.user.id
            user_email = request.user.email
        else:
            form = ContactForm(request.POST)
            logged_in = False
            username = 'anonymous'
            user_id = 0
            user_email = ''

        timestamp = datetime.datetime.now()
        form.data['created_on'] = timestamp
        if request.user.is_authenticated:
            form.data['user_id'] = request.user.id
        if form.is_valid():
            form.save()
            area = str(AREA_CHOICES[int(form.cleaned_data['area_of_concern'])][1])
            issue = str(ISSUE_CHOICES[int(form.cleaned_data['issue_type'])][1])
            email = form.cleaned_data['given_email']
            message = form.cleaned_data['message']
            email_subject = 'VanLevy contact, re: ' + issue

            email_message = 'We have been sent a message from user: <' + username + '>. '
            if email:
                email_message += 'They have given their email as: <' + email + '> . '
            else:
                email_message += 'They have not given an email. '
            if logged_in:
                email_message += 'Their user information is: <' + username + '>; user id: <' + str(user_id) + \
                                 '>; user_email: <' + user_email + '> . '
            else:
                email_message += 'They were not logged in. '

            email_message += 'They have a concern about <' + area + '>. '
            email_message += 'Their issue is <' + issue + '>. '
            email_message += 'Their message is: ' + message
            email_recipient = ("contact@vanlevy.com",)

            try:
                send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, email_recipient)
            except BadHeaderError:
                args = {'contact_form': form}
                template_name = 'vanlevy/vl_contact.html'
                return render(request, template_name, args)

            request.session['contact_message'] = "Message successfully sent."
            if request.user.is_authenticated:
                return redirect('vanlevy:portal')
            else:
                return redirect('vanlevy:home')
        else:
            args = {'contact_form': form}
            template_name = 'vanlevy/vl_contact.html'
            return render(request, template_name, args)
