# -*- coding: utf8 -*-

from django.db import models
import os.path
import os
from django.db.models.signals import post_delete, pre_save, post_init, post_save
from django.dispatch.dispatcher import receiver


class Document(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(verbose_name="Документ")
    extension = models.CharField(max_length=10)
    dateOfModification = models.DateTimeField(verbose_name="Дата изменение")
    previous_state = None

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


post_save.connect(Document.post_save, sender=Document)
post_init.connect(Document.remember_state, sender=Document)

@receiver(pre_save, sender=Document)
def my_signal_handcler(sender, instance, **kwargs):
    tmp = str(instance.file.name).split('.')
    instance.name = tmp[0]
    instance.extension = tmp[1]


@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


class Department(models.Model):
    name = models.CharField(max_length=100)
    documents = models.ManyToManyField(Document)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    departmen = models.ForeignKey(Department)

    def __str__(self):
        return self.name


class UserToDoc(models.Model):
    user = models.ForeignKey(User)
    doc = models.ManyToManyField(Document)
    status = models.BooleanField(default=False)




