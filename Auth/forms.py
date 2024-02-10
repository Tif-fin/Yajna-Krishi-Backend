from django import forms

class UserDeletionForm(forms.Form):
    mobilenumber = forms.CharField(label='Mobile Number')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
