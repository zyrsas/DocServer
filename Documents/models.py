# -*- coding: utf8 -*-
from django.db import models
import os.path
import os
from django.db.models.signals import post_delete, pre_save, post_init, post_save, pre_delete
from django.dispatch.dispatcher import receiver
from django.dispatch import Signal
from django.utils.safestring import mark_safe
from django.utils import timezone



save_dep = Signal(providing_args=["id_dep"])
global_dep = -1


#BEGIN Documents =====================

class Document(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    file = models.FileField(verbose_name="Документ")
    extension = models.CharField(max_length=10, verbose_name="Расширение")
    dateOfModification = models.DateTimeField(verbose_name="Дата изменение")
    previous_state = None

    class Meta:
        verbose_name_plural = "Документы"
        verbose_name = "Документ"
        ordering = ['-dateOfModification']

    def __str__(self):
        date_to_str = str(self.dateOfModification)
        date_to_str = date_to_str.replace('T', " ").replace("+00:00", "")
        last_ind = date_to_str.rfind(':')
        date_to_str = date_to_str[:last_ind]
        return str(self.name) + "." + str(self.extension)

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')

        print("post_saveCreated = " + str(created))
        print("post_saveinstance = " + str(instance))
        if not created:
            if instance.previous_state != instance.file.path:
                if os.path.isfile(instance.previous_state):
                    os.remove(instance.previous_state)
                    print("Change!!!")

                    # change status false
                    userToDoc = UserToDoc.objects.filter(doc=instance.id)
                    print(list(userToDoc))
                    for i in userToDoc:
                        i.status = False
                        i.save()
                        print("Update")


            else:
                print("Not Change")

    @staticmethod
    def remember_state(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')

        if str(instance) != '.':
            instance.previous_state = instance.file.path


# date of modification set
@receiver(pre_save, sender=Document)
def my_signal_handcler(sender, instance, **kwargs):
    tmp = str(instance.file.name).split('.')
    instance.name = tmp[0]
    instance.extension = tmp[-1]
    # instance.dateOfModification = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    instance.dateOfModification = timezone.now()

# delete after delete row in table
@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


@receiver(pre_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    userToDoc = Document.objects.filter(id=instance.id).values('id')
    print(list(userToDoc))
    for i in list(userToDoc):
        i = dict(i)
        print("doc_id = " + str(i['id']))
        if i['id'] != None:
            if UserToDoc.objects.filter(doc=i['id']).count() != 0:
                UserToDoc.objects.filter(doc=i['id']).delete()
                print("Delete!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


# for signals save for Doc
post_save.connect(Document.post_save, sender=Document)
post_init.connect(Document.remember_state, sender=Document)

# END Documents ========================

# BEGIN Department!!! =================================

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    documents = models.ManyToManyField(Document, verbose_name="Документы")

    class Meta:
        verbose_name_plural = "Отделы"
        verbose_name = "Отдел"


    def __str__(self):
        return self.name

    def documents_list(self):
        to_return = '<ul>'
        i = 0
        max = int(self.documents.count()) - 10
        for doc in self.documents.all():
            to_return += '<li><font size="2" color="#2E768F">{}</li>'.format(doc.name + "." + doc.extension)
            i += 1
            if i == 10:
                to_return += '<li><font size="2" color="#2E768F">...+' + str(max) + '</li></ul>'
                return mark_safe(to_return)
        to_return += '</ul>'
        return mark_safe(to_return)

    documents_list.allow_tags = True
    documents_list.short_description = "Документы"


@receiver(post_save, sender=Department)
def signal_department(sender, instance, **kwargs):
    # print(instance)
    global global_dep
    global_dep = instance.id


@receiver(post_init, sender=Department)
def check_update(sender, instance, **kwargs):
    global global_dep
    if global_dep != -1:
        save_dep.send(sender=None, id_dep=global_dep)
        global_dep = -1


@receiver(pre_delete, sender=Department)
def delte_dep(sender, instance, **kwargs):
    userToDoc = Department.objects.filter(id=instance.id).values('user',
                                                                 'documents__id')
    print(list(userToDoc))
    for i in list(userToDoc):
        i = dict(i)
        print("doc_id = " + str(i['documents__id']))
        print("user_id = " + str(i['user']))
        if ((i['user'] != None) and (i['documents__id'] != None)):
            if UserToDoc.objects.filter(user=i['user'], doc=i['documents__id']).count() == 0:
                UserToDoc.objects.filter(user=i['user'], doc=i['documents__id']).delete()
                print("Delete!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


# END Department!!! =================================

# BEGIN User!!! =================================
class User(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    password = models.CharField(max_length=100, verbose_name="Пароль")
    departmen = models.ForeignKey(Department, verbose_name="Отдел")
    regID = models.CharField(max_length=300, default="")

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователя"

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print("USER CREATE!!!!!!!!!!!!!!")
        print(instance.id)
        user_id = instance.id
        # add to database doc for user
        userToDoc = User.objects.filter(id=user_id).values('departmen__documents__id')
        print(list(userToDoc))
        for i in list(userToDoc):
            i = dict(i)
            if ((i['departmen__documents__id'] != None) and (user_id != None)):
                if not UserToDoc.objects.filter(user=user_id, doc=i['departmen__documents__id']).exists():
                    user_to_doc = UserToDoc(user=user_id, doc=i['departmen__documents__id'], status=True)
                    user_to_doc.save()


@receiver(pre_delete, sender=User)
def document_delete(sender, instance, **kwargs):
    userToDoc = User.objects.filter(id=instance.id).values('id')
    print(list(userToDoc))
    for i in list(userToDoc):
        i = dict(i)
        print("user_id = " + str(i['id']))
        if i['id'] != None:
            if UserToDoc.objects.filter(user=i['id']).count() != 0:
                UserToDoc.objects.filter(user=i['id']).delete()
                print("Delete!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# END User!!! =================================

# BEGIN UserToDoc =======================

class UserToDoc(models.Model):
    user = models.IntegerField()
    doc = models.IntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " " + str(self.doc) + " " + str(self.status)


def dep_save(sender, id_dep, **kwargs):
    userToDoc = Department.objects.filter(id=id_dep).values(
                                                            'documents__id',
                                                            'user',
                                                            )

    doc_id = Department.objects.filter(id=id_dep).values('documents__file')
    for i in list(doc_id):
        if Document.objects.filter(file=i['documents__file']).count() == 0:
            doc = Document(file=i['documents__file'])
            doc.save()

    user_list = []
    print(list(userToDoc))
    for i in list(userToDoc):
        i = dict(i)
        print("doc_id = " + str(i['documents__id']))
        print("user_id = " + str(i['user']))
        if ((i['user'] != None) and (i['documents__id'] != None)):
            if UserToDoc.objects.filter(user=i['user'], doc=i['documents__id']).count() == 0:
                user_to_doc = UserToDoc(user=i['user'], doc=i['documents__id'], status=False)
                user_to_doc.save()
                user_list.append(i['user'])
                print("SAVED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    if user_list:
        from Documents.notifications import sendNotification
        sendNotification(user_id=user_list)


save_dep.connect(dep_save)

# END UserToDoc ===============================