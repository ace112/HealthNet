from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()  # fill in custom user info then save it


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            'insurance',
            'address',
            'phone',
            'hospital',
            'gender',
            'emergency_contact_email',
            'weight',
            'height',
            'birthday'

        )
        #admit = User.admitted

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
          self.fields[myField].widget.attrs['class'] = 'form-control'
          self.fields[myField].required = True

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        for myField in self.fields:
            user.myField = self.cleaned_data[myField]

        if commit:
            user.save()
        return user


class TransferForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['hospital',]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['hospital'].required = True
        self.user = user

    def clean(self):
        clean_data = super(TransferForm, self).clean()
        if self.user.hospital != clean_data.get('hospital'):
            msg = "May only switch to your hospital"
            self.add_error('hospital', msg)

class AdmissionForm(forms.ModelForm):

    reason = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        super(AdmissionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(AdmissionForm,self).save(commit=False)
        #self.Meta.admit = True

        if commit:
            user.save()
        return user


class DismissalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        super(DismissalForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(DismissalForm, self).save(commit=False)
        #self.Meta.admit = False

        if commit:
            user.save()
        return user
