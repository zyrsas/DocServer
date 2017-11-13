from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from Documents import views
from DocServer.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
#    url(r'^documents/$', views.DocumentList.as_view()),
    url(r'^check/$', views.GetBytesArray),
    url(r'^create/$', views.createFile),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
