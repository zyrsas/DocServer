from django.db import models
from django.core.files.storage import FileSystemStorage

#fs = FileSystemStorage(location=STATIC_URL + '/files/')


class Document(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField()
    extension = models.CharField(max_length=10)
    dateOfModification = models.DateTimeField()

    def __str__(self):
        return self.name + "." + self.extension


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    documents = models.ManyToManyField(Document)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name
