from django.conf.urls import url

from . import views

app_name = 'charts'
urlpatterns = [
    url(r'^exportjson/$', views.export_json),
    url(r'^exportcsv/$', views.export_csv),
    url(r'^exportxls/$', views.export_xls),
    url(r'^draw/$', views.draw, name='draw'),
    url(r'^upload/$', views.simple_upload),
    url(r'^uploadform/$', views.ManualUpload.as_view()),
    url(r'^savegraph/$', views.savegraph),
    url(r'^savegraphs/$', views.savedgraphs),
    url(r'^drawsaved/(?P<graph_id>[0-9]+)/$', views.drawsaved),
]
