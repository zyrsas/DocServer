# -*- coding: utf8 -*-
from django.db import models
import os.path
import os, time
from django.db.models.signals import post_delete, pre_save, post_init, post_save
from django.dispatch.dispatcher import receiver
import datetime
from django.http import HttpResponse
from django.core.validators import ValidationError


class Document(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    file = models.FileField(verbose_name="Документ")
    extension = models.CharField(max_length=10, verbose_name="Расширение")
    dateOfModification = models.DateTimeField(verbose_name="Дата изменение")
    previous_state = None


    def __str__(self):
        return str(self.name) + "." + str(self.extension)


    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')
        instance.file.help_text = '<h3><font color="red">This is some text!</font></h3>'

        print("post_saveCreated = " + str(created))
        print("post_saveinstance = " + str(instance))
        if not created:
            if instance.previous_state != instance.file.path:
                if os.path.isfile(instance.previous_state):
                    os.remove(instance.previous_state)

            else:
                print("Not Change")

    @staticmethod
    def remember_state(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')

        if str(instance) != '.':
            instance.previous_state = instance.file.path


post_save.connect(Document.post_save, sender=Document)
post_init.connect(Document.remember_state, sender=Document)


@receiver(pre_save, sender=Document)
def my_signal_handcler(sender, instance, **kwargs):
    tmp = str(instance.file.name).split('.')
    instance.name = tmp[0]
    instance.extension = tmp[1]
    instance.dateOfModification = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


class Department(models.Model):
    name = models.CharField(max_length=100)
    documents = models.ManyToManyField(Document)

    def __str__(self):
        return self.name

    def documents_list(self):
        a = "\n".join([a.name for a in self.documents.all()])
        return a


#post_save.connect(signal_department, sender=Department)
#post_init.connect(Department.remember_state, sender=Department)


@receiver(post_save, sender=Department)
def signal_department(sender, instance, **kwargs):
    print(instance.id)
    userToDoc = Department.objects.filter(id=instance.id).values('documents__department__user',
                                                                 'documents__id')
    print(list(userToDoc))
    for i in list(userToDoc):
        i = dict(i)
        print("doc_id = " + str(i['documents__id']))
        print("user_id = " + str(i['documents__department__user']))
        if ((i['documents__department__user'] != None) and (i['documents__id'] != None)):
            if UserToDoc.objects.filter(user=i['documents__department__user'], doc=i['documents__id']).count() == 0:
                user_to_doc = UserToDoc(user=i['documents__department__user'], doc=i['documents__id'])
                user_to_doc.save()


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    departmen = models.ForeignKey(Department)

    def __str__(self):
        return self.name


""""@receiver(post_save, sender=User)
def signal_user(sender, instance, **kwargs):
    print(instance.id)
    userToDoc = User.objects.filter(id=instance.id).values('departmen__documents__id')
    print(list(userToDoc))
    for i in list(userToDoc):
        print("lost")
        i = dict(i)
        print("departmen__documents__id = " + str(i['departmen__documents__id']))
        print("user_id = " + str(instance.id))
        if ((i['departmen__documents__id'] != None) and (instance.id != None)):
            if not UserToDoc.objects.filter(user=instance.id, doc=i['departmen__documents__id']).exists():
                user_to_doc = UserToDoc(user=i['departmen__documents__id'], doc=instance.id, status=True)
                user_to_doc.save()
                print("Save")"""


class UserToDoc(models.Model):
    user = models.IntegerField()
    doc = models.IntegerField()
    status = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user) + " " + str(self.doc) + " " + str(self.status)




