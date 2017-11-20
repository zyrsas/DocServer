# -*- coding: utf8 -*-
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.core.files import File
from Documents.models import Document, User, Department, UserToDoc
from Documents.serializers import DocumentSerializer, DepartmentSerializer
from DocServer.settings import MEDIA_ROOT, MEDIA_URL
from django.forms.models import model_to_dict
from rest_framework import status
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
                    new_user = User(name=request.GET.get('user'), password=request.GET.get('pass'), departmen_id=int(request.GET.get('dep')))
                    new_user.save()

                    data_for_json = User.objects.filter(name=request.GET.get('user')).values('id',
                                                                                             'name',
                                                                                             'departmen_id',
                                                                                             'departmen__name')
                    tmp = list(data_for_json)[0]

                    # id new user
                    user_id = tmp
                    user_id = user_id['id']

                    # add to database doc for user
                    userToDoc = User.objects.filter(id=user_id).values('departmen__documents__id')
                    print(list(userToDoc))
                    for i in list(userToDoc):
                        i = dict(i)
                        if ((i['departmen__documents__id'] != None) and (user_id != None)):
                            if not UserToDoc.objects.filter(user=user_id,
                                                            doc=i['departmen__documents__id']).exists():
                                user_to_doc = UserToDoc(user=user_id,
                                                        doc=i['departmen__documents__id'],
                                                        status=True)
                                user_to_doc.save()

                    return Response(tmp)

                else:
                    return Response({"SignUp": "Department not exist"})
            else:
                return Response({"Null": "Null"})
        except KeyError:
            return Response({"Null": "Null"})
        except ValueError:
            return Response({"Null": "Null"})
        except:
            return Response({"Null": "Null"})


@api_view(['POST', ])
def SignIn(request):
    if request.method == "POST":
        try:
            if User.objects.filter(name=request.GET.get('user'),
                                   password=request.GET.get('pass')).count() == 0:
                return Response({"Null": "Null"}, )
            else:

                data_for_json = User.objects.filter(name=request.GET.get('user')).values('id',
                                                                                         'name',
                                                                                         'departmen_id',
                                                                                         'departmen__name'
                                                                                         )
                tmp = list(data_for_json)[0]

                return Response(tmp)
        except KeyError:
            return Response({"SignIn": "KeyError"})
        except ValueError:
            return Response({"SignIn": "ValueError"})
        except:
            return Response({"SignIn": "Error"})


@api_view(['POST', ])
def GetDocFromDepartment(request):
    if request.method == "POST":
        try:
            user_id = request.GET.get('user_id')

            dep_id = User.objects.filter(id=user_id, ).values('departmen_id')
            dep_id = dict(list(dep_id)[0])
            dep_id = dep_id['departmen_id']
            print("Department = " + str(dep_id))

            tmp = Department.objects.filter(id=dep_id).values(
                                                                'documents__name',
                                                                'documents__extension',
                                                                'documents__id',
                                                                'documents__file',
                                                                'documents__dateOfModification'
                                                                )
            json_list = []
            for i in tmp:
                # url for file
                base_url = "{0}://{1}{2}{3}".format(request.scheme, request.get_host(), MEDIA_URL, i['documents__file'])
                i['documents__file'] = base_url

                # fix date
                date_to_str = str(i['documents__dateOfModification'])
                date_to_str = date_to_str.replace('T', " ").replace("+00:00", '')

                i['documents__dateOfModification'] = date_to_str


                userToDoc = UserToDoc.objects.filter(user=user_id, doc=i['documents__id']).values('status')
                print(userToDoc)
                if userToDoc:
                    userToDoc = dict(list(userToDoc)[0])
                    print(userToDoc['status'])
                    i['status'] = userToDoc['status']
                json_list.append(i)

            return Response(json_list)
        except KeyError:
            return Response({"SignIn": "KeyError"})
        except ValueError:
            return Response({"SignIn": "ValueError"})
        except :
            return Response({"SignIn": "Error"})


@api_view(['POST', ])
def StatusDocForUser(request):
    if request.method == "POST":
        try:
            tmp = UserToDoc.objects.filter(user=int(request.GET.get('user'))).values('doc')

            return Response(list(tmp))
        except KeyError:
            return Response({"SignIn": "KeyError"})
        except ValueError:
            return Response({"SignIn": "ValueError"})
        except:
            return Response({"SignIn": "Error"})


@api_view(['POST', ])
def AbsoluteFileUrl(request):
    if request.method == "POST":
        try:
            tmp = Document.objects.filter(id=request.GET.get('id')).values('file')

            file = dict(list(tmp)[0])
            file = file['file']

            base_url = "{0}://{1}{2}{3}".format(request.scheme, request.get_host(), MEDIA_URL, file)
            print(base_url)
            return Response(list(tmp))
        except KeyError:
            return Response({"SignIn": "KeyError"})
        except ValueError:
            return Response({"SignIn": "ValueError"})
        except:
            return Response({"SignIn": "Error"})