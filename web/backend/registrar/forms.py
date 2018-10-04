from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput({"placeholder": "first name"}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput({"placeholder": "last name"}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput({"placeholder": "john@gmail.com"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)
        widgets = {
            'username': forms.TextInput({"placeholder": "username"}),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        if not self.is_bound:
            self.fields['password1'].widget = forms.PasswordInput({"placeholder": "password"})
            self.fields['password2'].widget = forms.PasswordInput({"placeholder": "repeat password"})

    def clean_username(self):
        content = self.cleaned_data['username']
        content = content.lower()
        if User.objects.filter(username=content).exists():
            raise forms.ValidationError(_("username already taken"), code="username_taken")

        return content

    def clean_email(self):
        content = self.cleaned_data['email']
        content = content.lower()
        if User.objects.filter(email=content).exists():
            raise forms.ValidationError(_("this email is already associated with an account"), code="email_not_unique")

        return content


class ResetPassInitForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput({"placeholder": "john@gmail.com"}))

    def clean_email(self):
        content = self.cleaned_data.get('email')
        if not User.objects.filter(email=content).exists():
            raise forms.ValidationError(_("Email address is not associated with an account"), code="email_not_found")

        return content


class ResetPassConfirmForm(forms.Form):
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput({"placeholder": "new password"}))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput({"placeholder": "repeat new password"}))

    def clean(self):
        cleaned_data = super(ResetPassConfirmForm, self).clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        if pass1 != pass2:
            raise forms.ValidationError(_("The two provided passwords are not the same!"), code="pass_mismatch")
