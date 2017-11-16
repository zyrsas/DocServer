# -*- coding: utf8 -*-
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.core.files import File
from Documents.models import Document, User, Department
from Documents.serializers import DocumentSerializer, DepartmentSerializer
from DocServer.settings import MEDIA_ROOT, MEDIA_URL
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
import binascii
import datetime

from rest_framework import serializers


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
            if User.objects.filter(name=request.GET.get('user')).count() == 0:
                if Department.objects.filter(id=request.GET.get('dep')).count() == 1:
                    new_user = User(name=request.GET.get('user'), password=request.GET.get('pass'), departmen_id=request.GET.get('dep'))
                    new_user.save()
                    return Response(model_to_dict(new_user))
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
            if User.objects.filter(name=request.GET.get('user'),
                                   password=request.GET.get('pass')).count() == 0:
                return Response({"SignIn": "Wrong"})
            else:

                data_for_json = User.objects.filter(name=request.GET.get('user')).values('id',
                                                                                               'name',
                                                                                               'departmen_id',
                                                                                               'departmen__name')
                return JsonResponse(json.dumps(list(data_for_json), indent=2))
        except KeyError:
            return Response({"SignIn": "KeyError"})
        except ValueError:
            return Response({"SignIn": "ValueError"})
        except:
            return Response({"SignIn": "Error"})