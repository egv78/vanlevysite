from django import forms
from django.contrib.auth import get_user_model
from swdice.models import SWRoom  #, EnterSWRoom, SWRoomToUser, SWRoomChat, SWDicePool
from accounts.models import Avatar
from .models import MYZDicePool

User = get_user_model()


class MYZDicePoolForm(forms.ModelForm):
    num_base_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Base Dice", 'value': 0, 'required': False, 'id': "base",
            'label': "Base", 'class': "sml-input"
        }
    ))
    num_skill_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': -9, 'title': "Skill Dice", 'value': 0, 'required': False, 'id': "skill",
            'label': "Skill", 'class': "sml-input", 'onchange': "changeSkillImage();",
        }
    ))
    num_gear_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Gear Dice", 'value': 0, 'required': False, 'id': "gear",
            'label': "Gear", 'class': "sml-input"
        }
    ))
    num_d6 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "D6", 'value': 0, 'required': False, 'id': "d6",
            'label': "D6", 'class': "sml-input"
        }
    ))
    num_d66 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "D66", 'value': 0, 'required': False, 'id': "d66",
            'label': "D66", 'class': "sml-input"
        }
    ))
    num_d666 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "D666", 'value': 0, 'required': False, 'id': "d666",
            'label': "D666", 'class': "sml-input"
        }
    ))
    num_numerical_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 9, 'min': 0, 'title': "Numerical Dice", 'value': 0, 'required': False, 'id': "numerical",
            'label': "Numerical", 'class': "sml-input"
        }
    ))
    numerical_dice_sides = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 100, 'min': 0, 'title': "Sides", 'value': 100, 'required': False, 'id': "sides",
            'label': "Sides", 'class': "med-input"
        }
    ))
    additional_trauma = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 20, 'min': 0, 'title': "Trauma", 'value': 0, 'required': False, 'id': "trauma",
            'label': "Trauma", 'class': "sml-input"
        }
    ))
    additional_failure = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 20, 'min': 0, 'title': "Failure", 'value': 0, 'required': False, 'id': "failure",
            'label': "Failure", 'class': "sml-input"
        }
    ))
    additional_damage = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 20, 'min': 0, 'title': "Damage", 'value': 0, 'required': False, 'id': "damage",
            'label': "Damage", 'class': "sml-input"
        }
    ))
    additional_success_base = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 20, 'min': 0, 'title': "Success (Base)", 'value': 0, 'required': False, 'id': "success_base",
            'label': "Success Base", 'class': "sml-input"
        }
    ))
    additional_success_skill = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 20, 'min': 0, 'title': "Success (Skill)", 'value': 0, 'required': False, 'id': "success_skill",
            'label': "Success Skill", 'class': "sml-input"
        }
    ))
    additional_success_gear = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 20, 'min': 0, 'title': "Success (Gear)", 'value': 0, 'required': False, 'id': "success_gear",
            'label': "Success Gear", 'class': "sml-input"
        }
    ))
    is_pushed = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'required': False, 'id': 'is_pushed'
        }
    ))

    caption = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': "roll-caption", 'placeholder': "Caption",
        }
    ))

    class Meta:
        model = MYZDicePool
        fields = ('num_base_dice', 'num_skill_dice', 'num_gear_dice', 'num_d6', 'num_d66', 'num_d666',
                  'num_numerical_dice', 'numerical_dice_sides', 'is_pushed', 'caption',
                  'additional_trauma', 'additional_failure', 'additional_damage',
                  'additional_success_base', 'additional_success_skill', 'additional_success_gear',
                  )

