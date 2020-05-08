from django.conf.urls import url
from card_scanner import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/CardScanner$', views.card_scanner_list),
    url(r'^api/CardScanner/(?P<pk>[0-9]+)$', views.card_scanner_detail),
    ]