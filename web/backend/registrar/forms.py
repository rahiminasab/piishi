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
    email_input = forms.EmailField(max_length=100, required=True)

    class Meta:
        fields = ('email_input',)

    def clean(self):
        cleaned_data = super(ResetPassInitForm, self).clean()
        email = cleaned_data.get('email_input')
        try:
            User.objects.get(email=email)
            return cleaned_data
        except User.DoesNotExist:
            raise forms.ValidationError(u'User with this Email address is not found!')


class ResetPassConfirmForm(forms.Form):
    password = forms.CharField(max_length=30, required=True)
    password_repeat = forms.CharField(max_length=30, required=True)

    class Meta:
        fields = ('password', 'password_repeat')

    def clean(self):
        cleaned_data = super(ResetPassConfirmForm, self).clean()
        pass1 = cleaned_data.get('password')
        pass2 = cleaned_data.get('password_repeat')
        if pass1 != pass2:
            raise forms.ValidationError(u'The two provided passwords are not the same!')
