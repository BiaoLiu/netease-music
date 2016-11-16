# coding: utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^test/$', views.test),

    url(r'^bstest/$', views.bs4_test),

    url(r'^music/$', views.get_music)

]
