from django import forms
from django.contrib.auth import get_user_model
from .models import PolyDicePool

User = get_user_model()


class PolyDicePoolForm(forms.ModelForm):
    num_d4 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 30, 'min': 0, 'title': "D4", 'value': 0, 'required': False, 'id': "d4",
            'label': "D4", 'class': "sml-input"
        }
    ))
    num_d6 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 30, 'min': 0, 'title': "D6", 'value': 0, 'required': False, 'id': "d6",
            'label': "D6", 'class': "sml-input"
        }
    ))
    num_d8 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 30, 'min': 0, 'title': "D8", 'value': 0, 'required': False, 'id': "d8",
            'label': "D8", 'class': "sml-input"
        }
    ))
    num_d10 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 30, 'min': 0, 'title': "D10", 'value': 0, 'required': False, 'id': "d10",
            'label': "d10", 'class': "sml-input"
        }
    ))
    num_d12 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 30, 'min': 0, 'title': "D12", 'value': 0, 'required': False, 'id': "d12",
            'label': "D12", 'class': "sml-input"
        }
    ))
    num_d20 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 30, 'min': 0, 'title': "D20", 'value': 0, 'required': False, 'id': "d20",
            'label': "D20", 'class': "sml-input"
        }
    ))
    num_d100 = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 30, 'min': 0, 'title': "d100", 'value': 0, 'required': False, 'id': "d100",
            'label': "D100", 'class': "sml-input"
        }
    ))
    bonus = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 99, 'min': -99, 'title': "Bonus", 'value': 0, 'required': False, 'id': "bonus",
            'label': "Bonus", 'class': "med-input-b"
        }
    ))
    num_numerical_dice = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 30, 'min': 0, 'title': "Numerical Dice", 'value': 0, 'required': False, 'id': "numerical",
            'label': "Numerical", 'class': "sml-input"
        }
    ))
    numerical_dice_sides = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'max': 999, 'min': 0, 'title': "Sides", 'value': 999, 'required': False, 'id': "sides",
            'label': "Sides", 'class': "med-input"
        }
    ))
    caption = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': "roll-caption", 'placeholder': "Caption",
        }
    ))

    class Meta:
        model = PolyDicePool
        fields = ('num_d4', 'num_d6', 'num_d8', 'num_d10', 'num_d12', 'num_d20', 'num_d100',
                  'bonus', 'num_numerical_dice', 'numerical_dice_sides', 'caption')
