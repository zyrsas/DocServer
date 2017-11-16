from django.contrib import admin
from Documents.models import Document, User, Department, UserToDoc


class TeachingDocumentModelAdmin(admin.ModelAdmin):
    exclude = ('name', 'extension',)
    list_display = ('name', 'extension', 'dateOfModification')
    list_filter = ('dateOfModification', )
    search_fields = ['name', 'extension']
    readonly_fields = ['dateOfModification']


admin.site.register(Document, TeachingDocumentModelAdmin)
admin.site.register(User)
admin.site.register(Department)
admin.site.register(UserToDoc)

# Admin change logo text
admin.site.site_header = "Directory NNR"