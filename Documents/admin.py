from django.contrib import admin
from Documents.models import Document, User, Department, UserToDoc


class TeachingClassesAdmin(admin.ModelAdmin):
    exclude = ('name', 'extension',)


admin.site.register(Document, TeachingClassesAdmin)
admin.site.register(User)
admin.site.register(Department)
admin.site.register(UserToDoc)