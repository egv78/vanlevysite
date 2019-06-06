from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from .models import VanLevyUser, Avatar, PDFCharSheet
from .gravatar import *
from accounts.forms import RegistrationForm, EditProfileForm, EditUserForm, EditAvatarForm, DeleteAvatarForm, \
                           NewPDFForm, SelectPDF
import datetime


# methods and classes used in view


# view methods and classes
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
        email = request.user.email
        vanlevy_email = str(request.user.username) + "@vanlevy.com"
        gravatar_real = gravatar_url_identicon(email)
        gravatar_identicon = gravatar_url_identicon(vanlevy_email)
        gravatar_monsterid = gravatar_url_monsterid(vanlevy_email)
        gravatar_wavatar = gravatar_url_wavatar(vanlevy_email)
        gravatar_retro = gravatar_url_retro(vanlevy_email)
        gravatar_robohash = gravatar_url_robohash(vanlevy_email)
        args = {'profile_form': profile_form, 'gravatar': gravatar_real, 'identicon': gravatar_identicon,
                'monsterid': gravatar_monsterid, 'wavatar': gravatar_wavatar, 'retro': gravatar_retro,
                'robohash': gravatar_robohash, }
        template_name = 'accounts/profile_edit.html'
        return render(request, template_name, args)


def edit_avatar(request, avatar_id=0):
    current_user_id = request.user.id

    if avatar_id == 0:  # 0 means creating avatar
        timestamp = datetime.datetime.now()
        should_leave = False
        avatar_form = EditAvatarForm()
    elif "edit" in request.path:
        # this_avatar = Avatar.objects.filter(pk=avatar_id)[0]
        try:
            this_avatar = Avatar.objects.filter(pk=avatar_id)[0]
        except IndexError:
            return redirect('accounts:view_profile')
        timestamp = this_avatar.created_on
        should_leave = not(this_avatar.user_id == current_user_id)
        initial_args = {'user_id': current_user_id, 'created_on': timestamp}
        avatar_form = EditAvatarForm(initial_args)
    else:  # Delete avatar
        try:
            this_avatar = Avatar.objects.filter(pk=avatar_id)[0]
        except IndexError:
            return redirect('accounts:view_profile')
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
            email = request.user.email
            vanlevy_email = str(request.user.username) + "@vanlevy.com"
            gravatar_real = gravatar_url_identicon(email)
            gravatar_identicon = gravatar_url_identicon(vanlevy_email)
            gravatar_monsterid = gravatar_url_monsterid(vanlevy_email)
            gravatar_wavatar = gravatar_url_wavatar(vanlevy_email)
            gravatar_retro = gravatar_url_retro(vanlevy_email)
            gravatar_robohash = gravatar_url_robohash(vanlevy_email)

            if "create" in request.path:
                # initial_args = {'user_id': current_user_id, 'created_on': timestamp}
                avatar_form = EditAvatarForm()
                template_name = 'accounts/profile_avatar_create.html'
                args = {'avatar_form': avatar_form, 'gravatar': gravatar_real,
                        'identicon': gravatar_identicon, 'monsterid': gravatar_monsterid,
                        'wavatar': gravatar_wavatar, 'retro': gravatar_retro, 'robohash': gravatar_robohash
                        }
            elif "edit" in request.path:
                avatar_form = EditAvatarForm(instance=this_avatar)
                template_name = 'accounts/profile_avatar_edit.html'

                args = {'avatar_form': avatar_form, 'this_avatar': this_avatar, 'gravatar': gravatar_real,
                        'identicon': gravatar_identicon, 'monsterid': gravatar_monsterid,
                        'wavatar': gravatar_wavatar, 'retro': gravatar_retro, 'robohash': gravatar_robohash
                        }
            elif "delete" in request.path:
                avatar_form = DeleteAvatarForm(instance=this_avatar)
                template_name = 'accounts/profile_avatar_delete.html'
                args = {'avatar_form': avatar_form, 'this_avatar': this_avatar}
            else:
                return redirect('accounts:view_profile')

            return render(request, template_name, args)


class ViewPDFChars(FormMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        current_user = request.user
        if request.method == "POST" and "archive" in request.POST:
            pdf_id = request.POST['archive']
            pdf_to_archive = PDFCharSheet.objects.get(id=pdf_id)
            pdf_to_archive.archived = True
            pdf_to_archive.save()
            return redirect('accounts:pdf_charsheets')
        elif request.method == "POST" and "activate" in request.POST:
            pdf_id = request.POST['activate']
            pdf_to_archive = PDFCharSheet.objects.get(id=pdf_id)
            pdf_to_archive.archived = False
            pdf_to_archive.save()
            return redirect('accounts:pdf_charsheets')
        elif request.method == "POST" and "new_pdf" in request.POST:
            new_pdf_form = NewPDFForm(request.POST)
            if new_pdf_form.is_valid():
                new_pdf_post = new_pdf_form.save(commit=False)
                test_url = new_pdf_post.pdf_url
                if 'drive.google.com' in test_url:
                    if 'open?id=' in test_url:
                        test_url = test_url.replace('open?id=', 'file/d/', 1)
                    if 'preview' not in test_url:
                        if 'view' in test_url:
                            test_url = test_url.replace('view', 'preview', 1)
                        else:
                            test_url += '/preview'
                    new_pdf_post.pdf_url = test_url
                new_pdf_post.user = current_user
                new_pdf_post.created_on = datetime.datetime.now()
                new_pdf_post.save()
                return redirect('accounts:pdf_charsheets')
            else:
                pdf_list_active = PDFCharSheet.objects.filter(user=current_user, archived=False)
                if len(pdf_list_active) > 0:
                    num_pdfs_active = len(pdf_list_active)
                else:
                    num_pdfs_active = 0

                pdf_list_archived = PDFCharSheet.objects.filter(user=current_user, archived=True)
                if len(pdf_list_archived) > 0:
                    num_pdfs_archived = len(pdf_list_archived)
                else:
                    num_pdfs_archived = 0

                num_pdfs_total = num_pdfs_active + num_pdfs_archived

                args = {'pdf_list_active': pdf_list_active, 'pdf_list_archived': pdf_list_archived,
                        'num_pdfs_total': num_pdfs_total, 'num_pdfs_active': num_pdfs_active,
                        'num_pdfs_archived': num_pdfs_archived, 'new_pdf_form': new_pdf_form}
                template_name = 'accounts/profile_pdf_chars.html'
                return render(request, template_name, args)

        else:
            return redirect('vanlevy:portal')

    def get(self, request, *args, **kwargs):
        current_user = request.user
        pdf_list_active = PDFCharSheet.objects.filter(user=current_user, archived=False).order_by('-created_on')
        if len(pdf_list_active) > 0:
            num_pdfs_active = len(pdf_list_active)
        else:
            num_pdfs_active = 0

        pdf_list_archived = PDFCharSheet.objects.filter(user=current_user, archived=True).order_by('-created_on')
        if len(pdf_list_archived) > 0:
            num_pdfs_archived = len(pdf_list_archived)
        else:
            num_pdfs_archived = 0

        new_pdf_form = NewPDFForm()

        num_pdfs_total = num_pdfs_active + num_pdfs_archived

        args = {'pdf_list_active': pdf_list_active, 'pdf_list_archived': pdf_list_archived,
                'num_pdfs_total': num_pdfs_total, 'num_pdfs_active': num_pdfs_active,
                'num_pdfs_archived': num_pdfs_archived, 'new_pdf_form': new_pdf_form}
        template_name = 'accounts/profile_pdf_chars.html'
        return render(request, template_name, args)


class ViewAvatar(FormMixin, TemplateView):
    # request, avatar_id=0

    def get_form_kwargs(self):
        # get avatar choices for enter room forms
        kwargs = super().get_form_kwargs()
        current_user_id = self.request.user.id
        my_pdfs = PDFCharSheet.objects.filter(user=current_user_id, archived=False)
        if len(my_pdfs) > 0:
            pdfs_list = [(0, 'Remove PDF')]
            for pdf in my_pdfs:
                pdfs_list.append((pdf.id, pdf.pdf_name))
        else:
            pdfs_list = [(0, 'no saved pdfs')]
        kwargs['select_pdf'] = pdfs_list
        return kwargs

    def get(self, request, *args, **kwargs):
        kwargs = self.get_form_kwargs()
        dropdown_form = SelectPDF(**kwargs)
        current_user_id = request.user.id
        try:
            avatar_id = self.kwargs['avatar_id']
            if not avatar_id > 0:
                raise ValueError
        except ValueError:
            return redirect('accounts:view_profile')

        try:
            this_avatar = Avatar.objects.filter(pk=avatar_id)[0]
        except IndexError:
            return redirect('accounts:view_profile')

        if this_avatar.user_id != current_user_id:
            return redirect('accounts:view_profile')

        new_pdf_form = NewPDFForm()
        has_no_sheet = (this_avatar.use_char_sheet == 0)
        args = {'this_avatar': this_avatar, 'new_pdf_form': new_pdf_form, 'pdf_dropdown': dropdown_form,
                'has_no_sheet': has_no_sheet}
        template_name = 'accounts/profile_avatar_view.html'

        return render(request, template_name, args)

    def post(self, request, *args, **kwargs):
        current_user_id = request.user.id
        try:
            avatar_id = self.kwargs['avatar_id']
            if not avatar_id > 0:
                raise ValueError
        except ValueError:
            return redirect('accounts:view_profile')

        try:
            this_avatar = Avatar.objects.filter(pk=avatar_id)[0]
        except IndexError:
            return redirect('accounts:view_profile')

        if this_avatar.user_id != current_user_id:
            return redirect('accounts:view_profile')

        if (request.method == 'POST' or request.method == 'FILES') and "new_pdf" in request.POST:
            new_pdf_form = NewPDFForm(request.POST, request.FILES)

            if new_pdf_form.is_valid():
                new_pdf_post = new_pdf_form.save(commit=False)
                test_url = new_pdf_post.pdf_url
                if 'drive.google.com' in test_url:
                    if 'open?id=' in test_url:
                        test_url = test_url.replace('open?id=', 'file/d/', 1)
                    if 'preview' not in test_url:
                        if 'view' in test_url:
                            test_url = test_url.replace('view', 'preview', 1)
                        else:
                            test_url += '/preview'
                    new_pdf_post.pdf_url = test_url
                new_pdf_post.user_id = current_user_id
                new_pdf_post.created_on = datetime.datetime.now()
                new_pdf_post.save()
                try:
                    use_this_pdf = PDFCharSheet.objects.filter(id=new_pdf_post.id)[0]
                    this_avatar.use_char_sheet = 1
                    this_avatar.char_pdf = use_this_pdf
                    this_avatar.save()
                except IndexError:
                    pass

                return redirect('accounts:view_profile')
            else:
                args = {'this_avatar': this_avatar, 'new_pdf_form': new_pdf_form}
                template_name = 'accounts/profile_avatar_view.html'

                return render(request, template_name, args)

        elif (request.method == 'POST' or request.method == 'FILES') and "old_pdf" in request.POST:
            kwargs = self.get_form_kwargs()
            new_pdf_form = SelectPDF(**kwargs)
            pdf_id = new_pdf_form.data['select_pdf']

            if new_pdf_form.is_valid():
                if pdf_id == '0':
                    this_avatar.use_char_sheet = 0
                    this_avatar.char_pdf = None
                    this_avatar.save()
                try:
                    use_this_pdf = PDFCharSheet.objects.filter(id=pdf_id)[0]
                    this_avatar.use_char_sheet = 1
                    this_avatar.char_pdf = use_this_pdf
                    this_avatar.save()
                except IndexError:
                    pass

                return redirect('accounts:view_profile')
            else:
                args = {'this_avatar': this_avatar, 'new_pdf_form': new_pdf_form}
                template_name = 'accounts/profile_avatar_view.html'

                return render(request, template_name, args)

        else:
            new_pdf_form = NewPDFForm()
            args = {'this_avatar': this_avatar, 'new_pdf_form': new_pdf_form}
            template_name = 'accounts/profile_avatar_view.html'
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

