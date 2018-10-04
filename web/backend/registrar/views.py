from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .forms import SignUpForm, ResetPassInitForm, ResetPassConfirmForm

from .tokens import account_activation_token


class SignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        email = form.cleaned_data.get('email')
        self.send_user_activation_email(user, email)

        return redirect(reverse('user_activation_pending', kwargs={"email": email}))

    def send_user_activation_email(self, user, to_email_address):
        subject = 'Please activate your account at Piishi.com'
        message = render_to_string('registration/activation/user_activation_email.html', {
            'user': user,
            'domain': get_current_site(self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
            'token': account_activation_token.make_token(user),
        })
        EmailMessage(
            subject, message, to=[to_email_address]
        ).send()


# ************ USER ACTIVATION ********************

class UserActivationPendingView(TemplateView):
    template_name = 'registration/activation/user_activation_pending.html'


class UserActivationDoneView(TemplateView):
    template_name = 'registration/activation/user_activation_done.html'

    def get(self, request, *args, **kwargs):
        uidb64 = self.kwargs["uidb64"]
        token = self.kwargs["token"]

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)

            return super(UserActivationDoneView, self).get(request, *args, **kwargs)
        else:
            return HttpResponse('Activation link is invalid!')


# ************ RESET PASSWORD ********************
class ResetPassInitView(FormView):
    template_name = 'registration/reset_pass/reset_pass_init.html'
    form_class = ResetPassInitForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.get(email=email)
        self.send_reset_pass_email(user, email)
        return redirect(reverse('reset_pass_pending', kwargs={"email": email}))

    def send_reset_pass_email(self, user, to_email_address):
        subject = 'Password reset request at piishi.com'
        message = render_to_string('registration/reset_pass/reset_pass_email.html', {
            'email': to_email_address,
            'domain': get_current_site(self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
            'token': account_activation_token.make_token(user),
        })
        EmailMessage(
            subject, message, to=[to_email_address]
        ).send()


class ResetPassPendingView(TemplateView):
    template_name = 'registration/reset_pass/reset_pass_pending.html'


class ResetPassConfirmView(FormView):
    template_name = 'registration/reset_pass/reset_pass_confirm.html'
    form_class = ResetPassConfirmForm

    def get(self, request, *args, **kwargs):
        uidb64 = self.kwargs["uidb64"]
        token = self.kwargs["token"]

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            login(request, user)
            return super(ResetPassConfirmView, self).get(request, *args, **kwargs)
        else:
            return HttpResponse('reset pass link is invalid!')

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data.get('password1'))
        user.save()
        login(self.request, user)

        return render(self.request, 'registration/reset_pass/reset_pass_done.html')
