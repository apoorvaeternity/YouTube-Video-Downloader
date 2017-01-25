from django.conf.urls import url
from download import views

urlpatterns = [
    url(r'^download/$', views.Download.as_view(),name="index"),
    ]