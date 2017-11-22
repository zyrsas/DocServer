from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from Documents import views
from DocServer.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^documents/$', views.DocumentList.as_view()),
    url(r'^document/$', views.GetDocFromDepartment),
    # url(r'^check/$', views.GetBytesArray),
    # url(r'^create/$', views.createFile),
    url(r'^sign_up/$', views.SignUp),
    url(r'^sign_in/$', views.SignIn),
    url(r'^user_status/$', views.StatusDocForUser),
    #url(r'^file_path/$', views.AbsoluteFileUrl),
    url(r'^all_department/$', views.DepartmentList.as_view()),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)