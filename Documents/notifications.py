from Documents.models import User, Department, UserToDoc

API_KEY = "AAAAhMVvqN0:APA91bGmK5ie-OpBUEihpGVMHqqJ3j5dwqfJ8ZEEAy8s5UkK9Vb7Y8r3niQ9xUpUvW3SLLTkCWYcFBcShgbu3XMkYnpF683iYNHHTZMMS8SgoVtYVSHcDWwQnzyYwqcpjMO-EfpK-oQC"

def sendNotification(user_id):
    user_id = list(set(user_id))

    from pyfcm import FCMNotification
    for i in user_id:
        user_reg = User.objects.filter(id=i).values("regID")
        user_reg = dict(list(user_reg)[0])

        push_service = FCMNotification(api_key=API_KEY)
        registration_id = user_reg["regID"]
        message_title = "DirectoryNNR"
        message_body = "Новых документов: " + str(countDocForUserID(i))
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                   message_body=message_body)


def countDocForUserID(id):
    user_id = id
    count = 0
    dep_id = User.objects.filter(id=user_id).values('departmen_id')
    dep_id = dict(list(dep_id)[0])
    dep_id = dep_id['departmen_id']

    tmp = Department.objects.filter(id=dep_id).values('documents__id', )
    for i in tmp:
        userToDoc = UserToDoc.objects.filter(user=user_id, doc=i['documents__id'], status=False).count()
        if userToDoc > 0:
            count += 1
    return count