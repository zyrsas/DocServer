import collections
from Documents.models import User

def sendNotification(user_id):
    from pyfcm import FCMNotification
    push_service = FCMNotification(api_key="AAAAhMVvqN0:APA91bGmK5ie-OpBUEihpGVMHqqJ3j5dwqfJ8ZEEAy8s5UkK9Vb7Y8r3niQ9xUpUvW3SLLTkCWYcFBcShgbu3XMkYnpF683iYNHHTZMMS8SgoVtYVSHcDWwQnzyYwqcpjMO-EfpK-oQC")
    registration_id = "cK6YpV-fshM:APA91bFPbtxzHnLZzGIx0PRXZGCJLpbA9KmA0eJLjnKOM9Zy4ijG0s-_Kh0tzNgoa-7DkDmXU0qUUgrAKKp9TtkW4ogDcxwN_k8XVB_iVBhzraMf30CrGKlSoifrVAZbWM3-7oP6_LyT"
    message_title = "Uber update"
    message_body = "Hello world!"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                               message_body=message_body)

    user_id = list(set(user_id))
    print(user_id)

    regID_list = []
    for i in user_id:
        user_reg = User.objects.filter(id=i).values("regID")
        user_reg = dict(list(user_reg)[0])
        print(user_reg["regID"])