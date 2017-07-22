from django.conf.urls import url

from . import views

urlpatterns = [
    # /team/
    url(r'^$', views.profile_redirect, name="profile"),
    # /team/register/
    url(r'^register/$', views.register, name="register"),
    # /team/login/
    url(r'^login/$', views.login_user, name="login"),
    # /team/logout/
    url(r'^logout/$', views.logout_user, name="logout"),
    # /team/get_all_mails/
    url(r'^get_all_mails/$', views.mails, name="get_all_mails"),
    # /team/delete/[user_to_delete]/
    url(r'^delete/(?P<user_to_delete>[\w\.@\+\-_]+)/$', views.delete, name="delete"),
    # /team/[user_to_show]/
    url(r'^(?P<user_to_show>[\w\.@\+\-_]+)/$', views.profile, name="profile_other_user"),
    # /team/email_verification/[user_to_show]/sd6sv8sd5FGr89ds...
    url(r'^email_verification/(?P<username>[\w\.@\+\-_]+)/(?P<verification_key>[a-zA-Z0-9]{35})/$', views.validate_email, name="validate_email"),
    # /team/resend_mail/[user_to_show]/
    url(r'^resend_mail/(?P<username>[\w\.@\+\-_]+)/$', views.regenerate_verification_key, name="resend_mail"),
]
