from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib import admin
from Documents import views
from DocServer.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^documents/$', views.DocumentList.as_view()),
    url(r'^document/$', views.GetDocFromDepartment),
    url(r'^sign_up/$', views.SignUp),
    url(r'^sign_in/$', views.SignIn),
    url(r'^user_status/$', views.StatusDocForUser),
    url(r'^count_doc/$', views.CountStatusDocForUser),
    url(r'^mark_doc/$', views.ChangeStatusDocForUser),
    url(r'^all_department/$', views.DepartmentList.as_view()),
    url(r'^licence/$', views.ShowLicence),
    url(r'^refresh_token/$', views.RefreshTOKEN),
    url(r'^clear_token/$', views.ClearTOKEN),
    url(r'^user_test/$', views.DeleteUserForTESTING),
    url(r'^admin_add/$', views.UploadView.as_view()),
    url(r'^contact/', views.contac),
    url(r'^map/$', views.map),
    url(r'^coordinate/$', views.UpdateCoordinates)
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

