from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views as registrar_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', registrar_views.SignUpView.as_view(), name='signup'),

    # ****** USER ACTIVATION URLs *******
    re_path(r'^user_activation_pending/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
            registrar_views.UserActivationPendingView.as_view(),
            name='user_activation_pending'),
    re_path(r'^user_activation_done/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            registrar_views.UserActivationDoneView.as_view(),
            name='user_activation_done'),

    # ****** RESET PASS URLs *******
    path('reset_pass_submit/', registrar_views.ResetPassInitView.as_view(), name='reset_pass_submit'),
    re_path(r'^reset_pass_pending/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
            registrar_views.ResetPassPendingView.as_view(),
            name='reset_pass_pending'),
    re_path(r'^reset_pass_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            registrar_views.ResetPassConfirmView.as_view(),
            name='reset_pass_confirm'),
]
