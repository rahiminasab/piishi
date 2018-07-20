from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    return home(request)


def home(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "index.html")
