from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views as registrar_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', registrar_views.SignUpView.as_view(), name='signup'),

    # ****** USER ACTIVATION URLs *******
    re_path(r'^user_activation_pending/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
            registrar_views.user_activation_pending,
            name='user_activation_pending'),
    re_path(r'^user_activation_done/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            registrar_views.user_activation_done,
            name='user_activation_done'),

    # ****** RESET PASS URLs *******
    path('reset_pass_submit/', registrar_views.reset_pass_submit, name='reset_pass_submit'),
    re_path(r'^reset_pass_pending/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
            registrar_views.reset_pass_pending,
            name='reset_pass_pending'),
    re_path(r'^reset_pass_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            registrar_views.reset_pass_confirm,
            name='reset_pass_confirm'),
    path('reset_pass_done/', registrar_views.reset_pass_done, name='reset_pass_done')
]
