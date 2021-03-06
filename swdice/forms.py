from django import forms
from django.contrib.auth import get_user_model
from .models import SWRoom, EnterSWRoom, SWRoomToUser, SWRoomChat, SWDicePool
from accounts.models import Avatar

User = get_user_model()


class Make_SW_Room(forms.ModelForm):
    def clean(self):
        is_open = self.cleaned_data.get('open_to_all')
        passcode = self.cleaned_data.get('passcode')

        if is_open:
            self.cleaned_data['passcode'] = ''
        else:
            if passcode == '':
                msg = forms.ValidationError("You must add a passcode to a restricted (i.e. not open) room")
                self.add_error('passcode', msg)

        return self.cleaned_data

    class Meta:
        model = SWRoom
        widgets = {'open_to_all': forms.RadioSelect}
        fields = ('name', 'passcode', 'open_to_all')

    name = forms.CharField(required=True, label='Name',
                           widget=forms.TextInput(
                               attrs={'placeholder': "Enter your room's name.", 'size': 40}
                           )
                           )
    passcode = forms.SlugField(required=False, label='Passcode',
                               widget=forms.TextInput(
                                   attrs={'placeholder': "e.g. swordfish", 'size': 40}
                               )
                               )


class Enter_SW_Room(forms.ModelForm):
    class Meta:
        model = EnterSWRoom
        widgets = {'default_avatar': forms.Select()}
        fields = ('room_number', 'passcode', 'default_avatar')

    def __init__(self, *args, **kwargs):
        imported_list = kwargs.pop('avatar_list')
        super().__init__(*args, **kwargs)
        self.fields['default_avatar'].choices = imported_list

    default_avatar = forms.ChoiceField(choices=[],
                                       widget=forms.Select(
                                           attrs={'style': "width: 30ch;"}
                                       ))
    room_number = forms.IntegerField(required=True, label='Room ID',
                                     widget=forms.NumberInput(
                                         attrs={'placeholder': "Room #",
                                                'style': "width: 10ch;"}
                                     ))
    passcode = forms.CharField(required=False, label='Passcode',
                               widget=forms.TextInput(
                                   attrs={'placeholder': "CaSe sENsiTivE", 'style': "width: 30ch;"}
                               ))


class Enter_SW_Direct(forms.ModelForm):
    class Meta:
        model = EnterSWRoom
        widgets = {'default_avatar': forms.Select()}
        fields = ('direct', 'default_avatar')

    def __init__(self, *args, **kwargs):
        imported_list = kwargs.pop('avatar_list')
        super().__init__(*args, **kwargs)
        self.fields['default_avatar'].choices = imported_list

    default_avatar = forms.ChoiceField(choices=[])

    direct = forms.CharField(required=True, label='Direct',
                             widget=forms.TextInput(
                                 attrs={'placeholder': "CaSe sENsiTivE", 'style': "width: 100%;"}
                             )
                             )


class SW_Room_to_User_Form(forms.ModelForm):
    class Meta:
        model = SWRoomToUser
        fields = ('room_id', 'user_id', 'admitted', 'game_master', 'banned',
                  'date_made_gm', 'date_banned', 'default_avatar_is_user', 'avatar_id')


class SW_Room_Chat_Form(forms.ModelForm):
    recipient = forms.ChoiceField(choices=[], widget=forms.Select(
        attrs={'onchange': "highlightChat();", }))
    chat_text = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'id': "chat_text", 'rows': 3, 'class': "chat-textbox", 'maxlength': "255", }
    ))

    class Meta:
        model = SWRoomChat
        widgets = {'is_private': forms.RadioSelect}
        fields = ('chat_text', 'is_private', 'recipient')

    def __init__(self, *args, **kwargs):
        imported_list = kwargs.pop('recipients_list')
        super().__init__(*args, **kwargs)
        self.fields['recipient'].choices = imported_list


class SW_Dice_Roll(forms.ModelForm):
    num_boost_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Boost Dice", 'value': 0, 'required': False, 'id': "boost",
            'class': "sml-input"
        }
    ))
    num_setback_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Setback Dice", 'value': 0, 'required': False, 'id': "setback",
            'class': "sml-input"
        }
    ))
    num_ability_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Ability Dice", 'value': 0, 'required': False, 'id': "ability",
            'class': "sml-input"
        }
    ))
    num_difficulty_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Difficulty Dice", 'value': 0, 'required': False, 'id': "difficulty",
            'class': "sml-input"
        }
    ))
    num_proficiency_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Proficiency Dice", 'value': 0, 'required': False, 'id': "proficiency",
            'class': "sml-input"
        }
    ))
    num_challenge_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Challenge Dice", 'value': 0, 'required': False, 'id': "challenge",
            'class': "sml-input"
        }
    ))
    num_force_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Force Dice", 'value': 0, 'required': False, 'id': "force",
            'class': "sml-input"
        }
    ))
    num_numerical_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Numerical Dice", 'value': 0, 'required': False, 'id': "numerical",
            'class': "sml-input"
        }
    ))
    numerical_dice_sides = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 100, 'min': 0, 'title': "Sides", 'value': 100, 'required': False, 'id': "sides",
            'class': "med-input"
        }
    ))
    additional_triumph = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Triumph", 'value': 0, 'required': False, 'id': "triumph",
            'class': "sml-input"
        }
    ))
    additional_despair = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Despair", 'value': 0, 'required': False, 'id': "despair",
            'class': "sml-input"
        }
    ))
    additional_success = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Success", 'value': 0, 'required': False, 'id': "success",
            'class': "sml-input"
        }
    ))
    additional_failure = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Failure", 'value': 0, 'required': False, 'id': "failure",
            'class': "sml-input"
        }
    ))
    additional_advantage = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Advantage", 'value': 0, 'required': False, 'id': "advantage",
            'class': "sml-input"
        }
    ))
    additional_threat = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Threat", 'value': 0, 'required': False, 'id': "threat",
            'class': "sml-input"
        }
    ))
    additional_light_pips = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Light Pips", 'value': 0, 'required': False, 'id': "lightpip",
            'class': "sml-input"
        }
    ))
    additional_dark_pips = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Dark Pips", 'value': 0, 'required': False, 'id': "darkpip",
            'class': "sml-input"
        }
    ))
    caption = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': "roll-caption", 'placeholder': "Caption",
        }
    ))

    class Meta:
        model = SWDicePool
        fields = ('num_boost_dice', 'num_ability_dice', 'num_proficiency_dice', 'num_setback_dice',
                  'num_difficulty_dice', 'num_challenge_dice', 'num_force_dice', 'num_numerical_dice',
                  'numerical_dice_sides', 'additional_triumph', 'additional_despair', 'additional_success',
                  'additional_failure', 'additional_advantage', 'additional_threat',
                  'additional_light_pips', 'additional_dark_pips', 'caption',
                  )

