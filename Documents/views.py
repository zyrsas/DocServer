# -*- coding: utf8 -*-

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.core.files import File
from Documents.models import Document, User, Department
from Documents.serializers import DocumentSerializer, DepartmentSerializer
from DocServer.settings import MEDIA_ROOT, MEDIA_URL
import json
import binascii
import datetime


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


@api_view(['GET'])
def GetBytesArray(request):
    try:
        obj = Document.objects.all()
        file = dict(list(obj.values('file'))[0])
        file = file['file']
        with open(MEDIA_ROOT + "/" + file, "rb") as docFile:
            f = docFile.read()
            b = bytearray(f)

        return Response({"File": binascii.hexlify(b)})
    except ValueError:
        return Response({"File": "Error"})


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


@api_view(['POST', ])
def SignUp(request):
    if request.method == "POST":
        try:
            body = request.read().decode('utf-8')
            json_data = json.loads(body)

            if User.objects.filter(name=json_data['user']).count() == 0:
                if Department.objects.filter(id=json_data['dep']).count() == 1:
                    new_user = User(name=json_data['user'], password=json_data['pass'], departmen_id=json_data['dep'])
                    new_user.save()
                    return Response({"SignUp": "Success"})
                else:
                    return Response({"SignUp": "Department not exist"})
            else:
                return Response({"SignUp": "Wrong! User exist"})
        except KeyError:
            return Response({"SignUp": "KeyError"})
        except ValueError:
            return Response({"SignUp": "ValueError"})
        except:
            return Response({"SignUp": "Error"})


@api_view(['POST', ])
def SignIn(request):
    if request.method == "POST":
        try:
            body = request.read().decode('utf-8')
            json_data = json.loads(body)

            if User.objects.filter(name=json_data['user'],
                                   password=json_data['pass']).count() == 0:
                return Response({"SignIn": "Wrong"})
            else:
                return Response({"SignIn": "Success"})
        except KeyError:
            return Response({"SignIn": "KeyError"})
        except ValueError:
            return Response({"SignIn": "ValueError"})
        except :
            return Response({"SignIn": "Error"})