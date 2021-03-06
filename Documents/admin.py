from django.contrib import admin
from Documents.models import Document, User, Department, UserToDoc


class TeachingDocumentModelAdmin(admin.ModelAdmin):
    exclude = ('name', 'extension',)
    list_display = ('name', 'extension', 'dateOfModification', )
    list_filter = ('dateOfModification', 'extension')
    search_fields = ['name', 'extension', ]
    readonly_fields = ['dateOfModification', ]


class TeachingUserModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'departmen', 'access')
    list_filter = ('departmen', )
    search_fields = ['name', 'departmen__name']
    readonly_fields = ['regID',] #'latitude', 'longitude', 'date']


class TeachingDepartmentModelAdmin(admin.ModelAdmin):
    list_display = ('name', "documents_list")
    list_filter = ('name', )
    search_fields = ['name']
    filter_horizontal = ('documents',)

    class Media:
        css = {"all": ("/media/styles.css", )}


admin.site.register(Document, TeachingDocumentModelAdmin)
admin.site.register(User, TeachingUserModelAdmin)
admin.site.register(Department, TeachingDepartmentModelAdmin)
admin.site.register(UserToDoc)


# Admin change logo text
admin.site.site_header = "Directory NNR"
admin.site.site_title = "Directory NNR"

