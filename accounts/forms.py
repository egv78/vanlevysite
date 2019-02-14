from django import forms
from accounts.models import UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Avatar
from django.core.validators import EMPTY_VALUES


User = get_user_model()
BOOL_CHOICES = [(True, 'Yes'), (False, 'No')]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2')

    def clean(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            error_msg = 'This email already has an account.  Would you like to reset your password?'
            self.add_error('email', error_msg)
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class EditProfileForm(forms.ModelForm):
    user_bio = forms.CharField(required=False, label='User Bio',
                               widget=forms.Textarea(attrs={'rows': 1, 'cols': 60})
                               )
    user_description = forms.CharField(required=False, label='Description',
                                       widget=forms.Textarea(attrs={'rows': 2, 'cols': 60})
                                       )
    user_image = forms.ImageField(required=False)
    user_url_image = forms.URLField(required=False, label='URL for Image',
                                    widget=forms.Textarea(attrs={'rows': 2, 'cols': 60})
                                    )
    user_first_name = forms.CharField(required=False, label='First Name')
    user_last_name = forms.CharField(required=False, label='Last Name')

    class Meta:
        model = UserProfile
        fields = ('user_bio',
                  'user_description',
                  'user_image',
                  'user_url_image',
                  'user_first_name',
                  'user_last_name'
                  )


class EditAvatarForm(forms.ModelForm):
    avatar_name = forms.CharField(required=True, label='name',
                                  widget=forms.TextInput(attrs={'size': 40})
                                  )
    avatar_description = forms.CharField(required=False, label='Description',
                                         widget=forms.Textarea(attrs={'rows': 2, 'cols': 60})
                                         )
    avatar_image = forms.ImageField(required=False)
    avatar_url_image = forms.URLField(required=False, label='URL for Image',
                                      widget=forms.Textarea(attrs={'rows': 2, 'cols': 60})
                                      )

    class Meta:
        model = Avatar
        fields = ('avatar_name',
                  'avatar_description',
                  'avatar_image',
                  'avatar_url_image'
                  )


class DeleteAvatarForm(forms.ModelForm):
    avatar_description = forms.CharField(required=False, label='Description')
    avatar_image = forms.ImageField(required=False)
    avatar_url_image = forms.CharField(required=False, label='URL for Image')

    class Meta:
        model = Avatar
        widgets = {'deleted': forms.RadioSelect}
        fields = ('avatar_name',
                  'avatar_description',
                  'avatar_image',
                  'avatar_url_image',
                  'deleted'
                  )

    def clean(self):
        to_be_deleted = self.cleaned_data.get('deleted')  # , False
        if not to_be_deleted:
            avatar_name = self.cleaned_data.get('avatar_name')  # , None
            if avatar_name in EMPTY_VALUES:
                self.errors['avatar_name'] = self.error_class(['Please enter a name for your Avatar'])
        return self.cleaned_data

