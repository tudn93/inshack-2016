from django.conf.urls import url

from . import views

urlpatterns = [
    # /challenges/
    url(r'^$', views.challenges_list, name='list'),
    # /challenges/score_board/
    url(r'^score_board/$', views.score_board, name='score_board'),
    # /challenges/add_challenge/
    url(r'^add_challenge/$', views.add_challenge, name='add'),
    # /challenges/update/[slug]/
    url(r'^update/(?P<slug>[\w-]+)/$', views.update_challenge, name='update'),
    # /challenges/update/[slug]/
    url(r'^delete/(?P<slug>[\w-]+)/$', views.delete_challenge, name='delete'),
    # /challenges/[slug]/
    url(r'^(?P<slug>[\w-]+)/$', views.challenge_display, name='display'),
]

