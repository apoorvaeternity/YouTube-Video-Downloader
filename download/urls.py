from django.conf.urls import url
from download import views

urlpatterns = [
    url(r'', views.Download.as_view(), name="index"),
]
