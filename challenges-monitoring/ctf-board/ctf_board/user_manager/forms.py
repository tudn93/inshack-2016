from collections import OrderedDict

from django import forms
from django.contrib.auth.models import User

from user_manager.models import TeamProfile
from multiupload.fields import MultiFileField


class TeamProfileForm(forms.ModelForm):
    cvs = MultiFileField(required=False, min_num=0, max_num=8)

    class Meta:
        model = TeamProfile
        fields = ['nb_players', 'avatar', 'on_site', 'level']

    def __init__(self, *args, **kwargs):
        super(TeamProfileForm, self).__init__(*args, **kwargs)
        order = ['nb_players', 'level', 'cvs', 'on_site', 'avatar']
        self.fields['avatar'].label = "Team's avatar"
        self.fields['avatar'].help_text = "A fun picture !"
        self.fields['avatar'].widget = forms.FileInput()
        self.fields['avatar'].widget.attrs.update({
            'placeholder': 'Browse...',
            'class': 'form-control',
            'icon': 'mood'
        })

        self.fields['nb_players'].label = "* Number of players (approximately)"
        self.fields['nb_players'].help_text = "To help the organizers"
        self.fields['nb_players'].widget.attrs.update({
            'class': 'form-control',
            'min': '1',
            'max': '4',
        })

        self.fields['level'].label = "* Your skills"
        self.fields['level'].help_text = "To help the organizers"
        self.fields['level'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['on_site'].label = "Are you playing on site ?"
        self.fields['on_site'].help_text = "To help the organizers"

        if self.instance.avatar.name:
            self.fields['delete_avatar'] = forms.BooleanField(widget=forms.CheckboxInput, required=False)
            self.fields['delete_avatar'].label = 'Delete old avatar ?'
            self.fields['delete_avatar'].help_text = "Do you want to remove your avatar from the website ?"
            order.append('delete_avatar')

        self.fields['cvs'].label = "Team's CVs"
        self.fields['cvs'].help_text = "They will be shared with our sponsors."
        self.fields['cvs'].widget.attrs.update({
            'placeholder': 'Browse...',
            'class': 'form-control',
            'multiple': 'true',
            'accept': 'application/pdf',
            'icon': 'attach_file'
        })
        self.fields = OrderedDict((k, self.fields[k]) for k in order)

    def clean_avatar(self):
        image = self.cleaned_data.get('avatar')
        if image and image.size > 4 * 1024 * 1024:
            raise forms.ValidationError('Please keep avatar size under 4MB.')
        return image

    def clean_cvs(self):
        cvs = self.cleaned_data.get('cvs')
        for cv in cvs:
            if len(cv.name.split('.')) == 1 or cv.name.split('.')[-1].lower() != 'pdf':
                raise forms.ValidationError('File type is not supported, please upload a PDF.')
            str_expected = '%PDF'
            is_pdf = True
            for i in range(4):
                char = cv.read(1)
                if char.decode('utf-8') != str_expected[i]:
                    is_pdf = False
            if not is_pdf:
                raise forms.ValidationError('File type is not supported, please upload a PDF.')
            if cv.size > 4 * 1024 * 1024:
                raise forms.ValidationError('Please keep PDF size under 4MB.')
        return cvs


class UserForm(forms.ModelForm):
    password_validation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '* Team name'
        self.fields['username'].help_text = "You'll be known like this during the CTF."
        self.fields['username'].widget.attrs.update({
            'placeholder': 'InSecurity',
            'class': 'form-control',
            'autofocus': 'true'
        })

        self.fields['email'].label = '* Team referent email'
        self.fields['email'].help_text = "All needed info will be sent here. Please <code>check it</code> " \
                                         "from time to time."
        self.fields['email'].widget = forms.EmailInput()
        self.fields['email'].widget.attrs.update({
            'placeholder': 'contact@insecurity-insa.fr',
            'class': 'form-control',
        })

        self.fields['password'].label = '* Password'
        self.fields['password'].help_text = "You'll need it to validate challenges, so <code>keep it</code> !"
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'placeholder': '1234',
            'class': 'form-control',
        })

        self.fields['password_validation'].label = '* Password verification'
        self.fields['password_validation'].help_text = "Used to check if you know how to repeat a password."
        self.fields['password_validation'].widget = forms.PasswordInput()
        self.fields['password_validation'].widget.attrs.update({
            'placeholder': '1234',
            'class': 'form-control',
        })

        if self.instance.pk is not None:
            self.fields['password_validation'].required = False
            self.fields['password_validation'].label = 'New password verification'
            self.fields['password'].required = False
            self.fields['password'].label = 'New password'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('An email is required')
        elif (self.instance and User.objects.filter(email=email).exclude(id=self.instance.id).count() != 0) or \
                (not self.instance and User.objects.filter(email=email).count() != 0):
            raise forms.ValidationError('An account using this email already exists.')
        return email

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if self.instance.pk is None:
            password = cleaned_data.get("password")
            password_validation = cleaned_data.get("password_validation")

            if password_validation != password:
                raise forms.ValidationError(
                    "Passwords don't match."
                )
        return cleaned_data


class LoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username_or_email'].label = 'Team name or email'
        self.fields['username_or_email'].help_text = "The team name or email used to register."
        self.fields['username_or_email'].widget.attrs.update({
            'placeholder': 'InSecurity',
            'class': 'form-control',
            'autofocus': 'true',
        })

        self.fields['password'].label = 'Password'
        self.fields['password'].widget.attrs.update({
            'placeholder': '1234',
            'class': 'form-control'
        })
