# -*- coding: utf8 -*-
from django.db import models
import os.path
import os
from django.db.models.signals import post_delete, pre_save, post_init, post_save
from django.dispatch.dispatcher import receiver
import datetime
from django.dispatch import Signal


save_dep = Signal(providing_args=["id_dep"])
global_dep = -1


class Document(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    file = models.FileField(verbose_name="Документ")
    extension = models.CharField(max_length=10, verbose_name="Расширение")
    dateOfModification = models.DateTimeField(verbose_name="Дата изменение")
    previous_state = None

    class Meta:
        verbose_name_plural = "Документы"

    def __str__(self):
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
    instance.extension = tmp[1]
    instance.dateOfModification = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


# delete after delete row in table
@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


# for signals save for Doc
post_save.connect(Document.post_save, sender=Document)
post_init.connect(Document.remember_state, sender=Document)


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    documents = models.ManyToManyField(Document, verbose_name="Документы")

    class Meta:
        verbose_name_plural = "Департаменты"

    def __str__(self):
        return self.name

    def documents_list(self):
        a = "<br>".join([a.name + "." + a.extension for a in self.documents.all()])
        return '<font size="2" color="#2E768F">' + a + "</p>"

    documents_list.allow_tags = True



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


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    departmen = models.ForeignKey(Department)

    class Meta:
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class UserToDoc(models.Model):
    user = models.IntegerField()
    doc = models.IntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " " + str(self.doc) + " " + str(self.status)


def dep_save(sender, id_dep, **kwargs):
    userToDoc = Department.objects.filter(id=id_dep).values('documents__department__user',
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
                print("SAVED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


save_dep.connect(dep_save)