from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from .models import VanLevyUser, Avatar
from accounts.forms import RegistrationForm, EditProfileForm, EditUserForm, EditAvatarForm, DeleteAvatarForm
import datetime


def about(request):
    template_name = 'accounts/about_accounts.html'
    return render(request, template_name)


def register(request):
    template_name = 'accounts/reg_form.html'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:register_success'))
        else:
            form = RegistrationForm(request.POST or None)
            args = {'form': form}
            return render(request, template_name, args)
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, template_name, args)


def register_success(request):
    template_name = 'accounts/reg_success.html'
    return render(request, template_name)


def view_profile(request):
    current_user_id = request.user.id
    my_avatars_list = Avatar.objects.filter(user_id=current_user_id, deleted=False).order_by('-id')
    if len(my_avatars_list) == 0:
        has_avatars = False
    else:
        has_avatars = True
    template_name = 'accounts/profile_view.html'
    args = {'user': request.user, 'my_avatars_list': my_avatars_list, 'has_avatars': has_avatars}
    return render(request, template_name, args)


def view_profile_other(request, other_user_id):
    other_user = VanLevyUser.objects.get(pk=other_user_id)
    template_name = 'accounts/profile_view_other.html'
    args = {'user': other_user}
    return render(request, template_name, args)


def edit_profile(request):
    if request.method == 'POST' or request.method == 'FILES':
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('accounts:view_profile')
        else:
            args = {'profile_form': profile_form}
            template_name = 'accounts/profile_edit.html'
            return render(request, template_name, args)
    else:
        profile_form = EditProfileForm(instance=request.user.userprofile)
        args = {'profile_form': profile_form}
        template_name = 'accounts/profile_edit.html'
        return render(request, template_name, args)


def edit_avatar(request, avatar_id=0):
    current_user_id = request.user.id

    if avatar_id == 0:  # 0 means creating avatar
        timestamp = datetime.datetime.now()
        should_leave = False
        avatar_form = EditAvatarForm()
    elif "edit" in request.path:
        this_avatar = Avatar.objects.filter(pk=avatar_id)[0]
        timestamp = this_avatar.created_on
        should_leave = not(this_avatar.user_id == current_user_id)
        initial_args = {'user_id': current_user_id, 'created_on': timestamp}
        avatar_form = EditAvatarForm(initial_args)
    else:  # Delete avatar
        this_avatar = Avatar.objects.filter(pk=avatar_id)[0]
        timestamp = datetime.datetime.now()
        should_leave = False
        initial_args = {'user_id': current_user_id, 'created_on': timestamp}
        avatar_form = DeleteAvatarForm(initial_args)

    if should_leave:  # make sure user can't type an avatar id into web browser
        return redirect('accounts:view_profile')
    else:
        if request.method == 'POST' or request.method == 'FILES':
            if avatar_id == 0:  # create
                bad_form_template_name = 'accounts/profile_avatar_create.html'
                avatar_form = EditAvatarForm(request.POST, request.FILES)
                avatar_form.deleted = False
                avatar_form.user_id = current_user_id
                avatar_form.created_on = timestamp
                bad_form_args = {'avatar_form': avatar_form}
            elif "edit" in request.path:
                avatar_form = EditAvatarForm(request.POST, request.FILES, instance=this_avatar)
                bad_form_template_name = 'accounts/profile_avatar_edit.html'
                this_avatar = Avatar.objects.filter(pk=avatar_id)[0]
                bad_form_args = {'avatar_form': avatar_form, 'this_avatar': this_avatar}
            elif "delete" in request.path:
                avatar_form = DeleteAvatarForm(request.POST, request.FILES, instance=this_avatar)
                bad_form_template_name = 'accounts/profile_view.html'
                bad_form_args = {}

            if avatar_form.is_valid():
                avatar_post = avatar_form.save(commit=False)
                avatar_post.user_id = request.user.id
                if avatar_id:
                    avatar_post.id = avatar_id
                avatar_post.created_on = timestamp
                avatar_post.save()
                return redirect('accounts:view_profile')
            else:
                if "delete" in request.path:
                    return redirect('accounts:view_profile')
                else:
                    return render(request, bad_form_template_name, bad_form_args)

        else:  # request.method == GET
            if "create" in request.path:
                # initial_args = {'user_id': current_user_id, 'created_on': timestamp}
                avatar_form = EditAvatarForm()
                template_name = 'accounts/profile_avatar_create.html'
                args = {'avatar_form': avatar_form}
            elif "edit" in request.path:
                avatar_form = EditAvatarForm(instance=this_avatar)
                template_name = 'accounts/profile_avatar_edit.html'
                args = {'avatar_form': avatar_form, 'this_avatar': this_avatar}
            elif "delete" in request.path:
                avatar_form = DeleteAvatarForm(instance=this_avatar)
                template_name = 'accounts/profile_avatar_delete.html'
                args = {'avatar_form': avatar_form, 'this_avatar': this_avatar}
            else:
                return redirect('accounts:view_profile')

            return render(request, template_name, args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed successfully.')
            update_session_auth_hash(request, form.user)
            return render(request, 'accounts/password_success.html')
        else:
            form = PasswordChangeForm(user=request.user)
            message = "There was a problem with your password change request.  Please try again."
            args = {'error_message': message, 'form': form}
            return render(request, 'accounts/password.html', args)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/password.html', args)


def change_password_success(request):
    template_name = 'accounts/password_success.html'
    args = {'user': request.user}
    return render(request, template_name, args)

