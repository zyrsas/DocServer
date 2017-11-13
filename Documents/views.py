# -*- coding: utf8 -*-

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.core.files import File
from Documents.models import Document
from Documents.serializers import DocumentSerializer
from DocServer.settings import BASE_DIR
import binascii
import datetime


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


@api_view(['GET'])
def GetBytesArray(request):
    try:
        obj = Document.objects.all()
        file = dict(list(obj.values('file'))[0])
        file = file['file']
        with open(BASE_DIR+'/files/doc/' + file, "rb") as docFile:
            f = docFile.read()
            b = bytearray(f)

        return Response({"File": binascii.hexlify(b)})
    except ValueError:
        return Response({"File": str(b)})


@api_view(['GET'])
def createFile(request):
    obj = Document.objects.all()
    file = dict(list(obj.values('file'))[0])
    file = file['file']
    with open(BASE_DIR + '/files/doc/' + file, "rb") as docFile:
        f = docFile.read()
        b = bytearray(f)

    file2 = open(BASE_DIR + '/files/test.docx', 'wb')
    file2.write(b)

    file2.close()

    path = (BASE_DIR + "/files/test.docx")

    obj = Document(name="test_file",
                   file=File(open(path)),
                   extension="docx",
                   dateOfModification=datetime.datetime.now())
    obj.save()

    return Response({"Ok": "Ok"})


