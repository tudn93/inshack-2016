from django import forms

from challenges.models import Challenge


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['name', 'description', 'category', 'nb_points', 'flag', 'authors', 'is_enabled', 'chall_file']

    def __init__(self, *args, **kwargs):
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Challenge name'
        self.fields['name'].help_text = "Be inventive."
        self.fields['name'].widget.attrs.update({
            'placeholder': 'debugging_madness',
            'class': 'form-control',
            'autofocus': 'true'
        })

        self.fields['description'].label = 'Description'
        self.fields['description'].help_text = "A complete description for the contenders. " \
                                               "Be specific and fun (it can be a story for example)"
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Blabliblou http://insecurity-insa.fr:84/  blablou ... decrypt /password file ...',
            'class': 'form-control',
            'rows': '3'
        })

        self.fields['category'].label = 'Category'
        self.fields['category'].help_text = "If it does not fit, think of adding a category please."
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['nb_points'].label = 'Number of points'
        self.fields['nb_points'].help_text = "Let's say that the easiest challenge will pay 20 points " \
                                             "and the hardest 400."
        self.fields['nb_points'].widget.attrs.update({
            'placeholder': '50',
            'class': 'form-control',
        })

        self.fields['flag'].label = 'Flag'
        self.fields['flag'].help_text = "The challenge's solution, so that contestants can flag."
        self.fields['flag'].widget.attrs.update({
            'placeholder': 'FLAG{lataupedu39}',
            'class': 'form-control',
        })

        self.fields['chall_file'].label = 'Challenge\'s file(s)'
        self.fields['chall_file'].help_text = "Do you want contenders to have access to a file ?"
        self.fields['chall_file'].widget = forms.FileInput()
        self.fields['chall_file'].widget.attrs.update({
            'placeholder': 'Browse...',
            'class': 'form-control',
            'icon': 'attach_file',
        })

        self.fields['authors'].label = 'Authors'
        self.fields['authors'].help_text = "Who are the beautiful people who did this evil challenge ?"
        self.fields['authors'].widget.attrs.update({
            'placeholder': 'Vincent & Raphael',
            'class': 'form-control',
        })

        self.fields['is_enabled'].label = 'Put online now ?'
        self.fields['is_enabled'].help_text = "Is this challenge ready ? If you have to configure something on " \
                                              "the server first, then it's <code>not ready</code>"


class SubmitionForm(forms.Form):
    flag = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SubmitionForm, self).__init__(*args, **kwargs)
        self.fields['flag'].label = 'Flag'
        self.fields['flag'].help_text = "You will find it when you solve the challenge. It looks like this : flag{1234}"
        self.fields['flag'].widget.attrs.update({
            'placeholder': 'FLAG{flying_cow}',
            'class': 'form-control'
        })
