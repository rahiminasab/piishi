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
        send_user_activation_email(self.request, user, email)

        return redirect(reverse('user_activation_pending', kwargs={"email": email}))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            email = form.cleaned_data.get('email')
            user.save()

            send_user_activation_email(request, user, email)
            return redirect(reverse('user_activation_pending', kwargs={"email": email}))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# ************ USER ACTIVATION ********************

def user_activation_pending(request, email):
    return render(request, 'registration/activation/user_activation_pending.html', {"email": email})


def user_activation_done(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/activation/user_activation_done.html')
    else:
        return HttpResponse('Activation link is invalid!')


def send_user_activation_email(request, user, to_email_address):
    subject = 'Please activate your account at Piishi.com'
    message = render_to_string('registration/activation/user_activation_email.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
        'token': account_activation_token.make_token(user),
    })
    EmailMessage(
        subject, message, to=[to_email_address]
    ).send()


# ************ RESET PASSWORD ********************
def reset_pass_submit(request):
    if request.method == 'POST':
        form = ResetPassInitForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email_input')
            user = User.objects.get(email=email)
            send_reset_pass_email(request, user, email)
            return redirect(reverse('reset_pass_pending', kwargs={"email": email}))
    else:
        form = ResetPassInitForm()
    return render(request, 'registration/reset_pass/reset_pass_init.html', {'form': form})


def reset_pass_pending(request, email):
    return render(request, 'registration/reset_pass/reset_pass_pending.html', {"email": email})


def send_reset_pass_email(request, user, to_email_address):
    subject = 'Password reset request at piishi.com'
    message = render_to_string('registration/reset_pass/reset_pass_email.html', {
        'email': to_email_address,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
        'token': account_activation_token.make_token(user),
    })
    EmailMessage(
        subject, message, to=[to_email_address]
    ).send()


def reset_pass_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        form = ResetPassConfirmForm()
        login(request, user)
        return render(request, 'registration/reset_pass/reset_pass_confirm.html', {"form": form, "user": user})
    else:
        return HttpResponse('reset pass link is invalid!')


@require_POST
def reset_pass_done(request):
    form = ResetPassConfirmForm(request.POST)
    if form.is_valid():
        user = request.user
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        login(request, user)
        return render(request, 'registration/reset_pass/reset_pass_done.html')