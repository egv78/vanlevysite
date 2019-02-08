from django import forms
from django.contrib.auth import get_user_model
from .models import SWRoom, EnterSWRoom, SWRoomToUser, SWRoomChat, SWDicePool
from accounts.models import Avatar

User = get_user_model()


class Make_SW_Room(forms.ModelForm):
    class Meta:
        model = SWRoom
        widgets = {'open_to_all': forms.RadioSelect}
        fields = ('name', 'passcode', 'open_to_all')


class Enter_SW_Room(forms.ModelForm):
    class Meta:
        model = EnterSWRoom
        widgets = {'default_avatar': forms.Select()}
        fields = ('room_number', 'passcode', 'default_avatar')

    def __init__(self, *args, **kwargs):
        imported_list = kwargs.pop('avatar_list')
        super().__init__(*args, **kwargs)
        self.fields['default_avatar'].choices = imported_list

    default_avatar = forms.ChoiceField(choices=[])


class SW_Room_to_User_Form(forms.ModelForm):
    class Meta:
        model = SWRoomToUser
        fields = ('room_id', 'user_id', 'admitted', 'game_master', 'banned',
                  'date_made_gm', 'date_banned', 'default_avatar_is_user', 'avatar_id')


class SW_Room_Chat_Form(forms.ModelForm):
    recipient = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'onchange': "highlightChat();"}))
    chat_text = forms.CharField(widget=forms.Textarea(
        attrs={
            'id': "chat_text", 'rows': 2, 'width': "50%"
        }
    ))

    class Meta:
        model = SWRoomChat
        # widgets = {'is_private': forms.RadioSelect, 'recipient': forms.Select(attrs={'onchange': "highlightChat();"})}
        widgets = {'is_private': forms.RadioSelect}
        fields = ('chat_text', 'is_private', 'recipient')

    def __init__(self, *args, **kwargs):
        imported_list = kwargs.pop('recipients_list')
        super().__init__(*args, **kwargs)
        self.fields['recipient'].choices = imported_list


class SW_Dice_Roll(forms.ModelForm):
    num_boost_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Boost", 'value': 0, 'required': False, 'id': "boost", 'label': "Boost",
            'class': "sml-input"
        }
    ))
    num_setback_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Setback", 'value': 0, 'required': False, 'id': "setback", 'label': "Setback",
            'class': "sml-input"
        }
    ))
    num_ability_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Ability", 'value': 0, 'required': False, 'id': "ability", 'label': "Ability",
            'class': "sml-input"
        }
    ))
    num_difficulty_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Difficulty", 'value': 0, 'required': False, 'id': "difficulty",
            'label': "Difficulty", 'class': "sml-input"
        }
    ))
    num_proficiency_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Proficiency", 'value': 0, 'required': False, 'id': "proficiency",
            'label': "Proficiency", 'class': "sml-input"
        }
    ))
    num_challenge_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Challenge", 'value': 0, 'required': False, 'id': "challenge",
            'label': "Challenge", 'class': "sml-input"
        }
    ))
    num_force_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Force", 'value': 0, 'required': False, 'id': "force", 'label': "Force",
            'class': "sml-input"
        }
    ))
    num_numerical_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Numerical", 'value': 0, 'required': False, 'id': "numerical",
            'label': "Numerical", 'class': "sml-input"
        }
    ))
    numerical_dice_sides = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 100, 'min': 0, 'title': "Sides", 'value': 100, 'required': False, 'id': "sides", 'label': "Sides",
            'class': "med-input"
        }
    ))
    additional_triumph = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Triumphs", 'value': 0, 'required': False, 'id': "triumph",
            'label': "Triumphs", 'class': "sml-input"
        }
    ))
    additional_despair = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Despair", 'value': 0, 'required': False, 'id': "despair",
            'label': "Despair", 'class': "sml-input"
        }
    ))
    additional_success = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Success", 'value': 0, 'required': False, 'id': "success",
            'label': "Success", 'class': "sml-input"
        }
    ))
    additional_failure = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Failure", 'value': 0, 'required': False, 'id': "failure",
            'label': "Failure", 'class': "sml-input"
        }
    ))
    additional_advantage = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Advantage", 'value': 0, 'required': False, 'id': "advantage",
            'label': "Advantage", 'class': "sml-input"
        }
    ))
    additional_threat = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Threat", 'value': 0, 'required': False, 'id': "threat",
            'label': "Threat", 'class': "sml-input"
        }
    ))
    additional_light_pips = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Light Pops", 'value': 0, 'required': False, 'id': "lightpip",
            'label': "Light Pips", 'class': "sml-input"
        }
    ))
    additional_dark_pips = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Dark Pips", 'value': 0, 'required': False, 'id': "darkpip",
            'label': "Dark Pips", 'class': "sml-input"
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

