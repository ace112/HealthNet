from django import forms
from .models import Inbox
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime
User = get_user_model()


class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Inbox
        fields = (
            'sender',
            'receiver',
            'message',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['sender'].initial = user.id
        self.fields['sender'].disabled = True
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class ReplyForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Inbox
        fields = (
            'sender',
            'receiver',
            'message',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        receiver = kwargs.pop('receiver', None)
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.fields['sender'].initial = user.id
        self.fields['sender'].disabled = True
        self.fields['receiver'].initial = receiver
        self.fields['receiver'].disabled = True
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class DeleteForm(forms.ModelForm):
    sender = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Inbox
        fields = (
            'sender',
            'receiver',
            'message',
        )

    def __init__(self, *args, **kwargs):
        message = kwargs.pop('message', None)
        receiver = kwargs.pop('receiver', None)
        sender = kwargs.pop('sender', None)
        super(DeleteForm, self).__init__(*args, **kwargs)
        self.fields['sender'].initial = sender.id
        self.fields['sender'].disabled = True
        self.fields['sender'].required = False
        self.fields['message'].initial = message
        self.fields['message'].disabled = True
        self.fields['message'].required = False
        self.fields['receiver'].initial = receiver.id
        self.fields['receiver'].disabled = True
        self.fields['receiver'].required = False
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


