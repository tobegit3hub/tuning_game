from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r"^v1/competitions/(?P<competition_id>[\w.-]+)$",
        views.v1_competition,
        name="v1_competition"),
    url(r"^v1/participations/(?P<participation_id>[\w.-]+)$",
        views.v1_participation,
        name="v1_participation"),

]
