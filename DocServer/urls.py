from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from Documents import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^documents/$', views.DocumentList.as_view()),
    url(r'^check/$', views.GetBytesArray),
    url(r'^create/$', views.createFile),
]


urlpatterns = format_suffix_patterns(urlpatterns)