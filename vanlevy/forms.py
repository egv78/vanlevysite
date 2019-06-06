from django import forms
from django.contrib.auth import get_user_model
from .models import ContactModel

User = get_user_model()

AREA_CHOICES = [(0, '--select or leave blank--'), (1, 'Accounts'), (2, 'A Dice Roller'), (3, 'Something Else')]
ISSUE_CHOICES = [(0, '--select or leave blank--'), (1, 'Bug Report'), (2, 'Login problems'), (3, 'Something Else')]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ('area_of_concern', 'issue_type', 'message', 'given_email', 'user', 'created_on')

    area_of_concern = forms.ChoiceField(choices=AREA_CHOICES,
                                        widget=forms.Select(
                                           attrs={}
                                        ))
    issue_type = forms.ChoiceField(choices=ISSUE_CHOICES,
                                   widget=forms.Select(
                                      attrs={}
                                   ))
    message = forms.CharField(required=True,
                              widget=forms.Textarea(
                                attrs={
                                    'id': "chat_text", 'rows': 6, 'class': "chat-textbox", 'maxlength': "1023",
                                    'placeholder': "Type your message here."}
                              ))

    given_email = forms.EmailField(required=False,
                                   widget=forms.EmailInput(
                                     attrs={'type': 'email', 'placeholder': 'Email - optional', 'size': '60'}
                                   ))
