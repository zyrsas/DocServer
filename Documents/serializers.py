from rest_framework import serializers
from Documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'file', 'extension', 'dateOfModification')
