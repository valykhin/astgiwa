from __future__ import unicode_literals

from django.db import models
from urlparse import urlparse


# Create your models here.
class OperatingSystem(models.Model):
    name = models.CharField(max_length=64)
    company = models.CharField(max_length=64, blank=True, null=True)
    version = models.CharField(max_length=64)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' '.join([str(self.company), str(self.name), str(self.version)])


class Browser(models.Model):
    name = models.CharField(max_length=64)
    company = models.CharField(max_length=64)
    version = models.CharField(max_length=64)
    support_type = models.CharField(max_length=16, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    operating_system = models.ForeignKey(OperatingSystem)

    def __str__(self):
        return ' '.join([str(self.company), str(self.name), str(self.version), str(self.support_type)])


class Resolution(models.Model):
    height = models.IntegerField()
    width = models.IntegerField()
    aspect_ratio = models.CharField(max_length=8, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.width) + ' x ' + str(self.height) + ' (' + str(self.aspect_ratio) + ')'


class DefectType(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    creation_time = models.DateTimeField(auto_now_add=True)


class TestRequest(models.Model):
    email = models.CharField(max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1)


class TestConfiguration(models.Model):
    test_request = models.ForeignKey(TestRequest)
    resolution = models.ForeignKey(Resolution)
    browser = models.ForeignKey(Browser)


class URL(models.Model):
    protocol = models.CharField(max_length=8)
    host = models.CharField(max_length=128)
    port = models.IntegerField(blank=True, null=True)
    endpoint = models.CharField(max_length=512, blank=True, null=True)
    test_request = models.ForeignKey(TestRequest)

    def __str__(self):
        return self.protocol + '://' + self.host + self.endpoint if self.port is None else \
            self.protocol + '://' + self.host + ':' + str(self.port) + self.endpoint

    def parse(self, url):
        res = urlparse(url)
        self.protocol = res.scheme
        self.host = res.hostname
        self.port = res.port
        self.endpoint = res.path


class Test(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    test_configuration = models.ForeignKey(TestConfiguration)
    url = models.ForeignKey(URL)
    status = models.CharField(max_length=1)
    start_time = models.DateTimeField(blank=True, null=True)
    finish_time = models.DateTimeField(blank=True, null=True)
    test_request = models.ForeignKey(TestRequest)


class Queue(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    test = models.ForeignKey(Test)
    scheduled_time = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(default=0)


class Screenshot(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=256)


class Defect(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    defect_type = models.ForeignKey(DefectType)
    defect_description = models.CharField(max_length=512)
    test = models.ForeignKey(Test)
    full_url = models.CharField(max_length=512)
    screenshot = models.ForeignKey(Screenshot, blank=True, null=True)


class Contact(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=256)
    paypal = models.CharField(max_length=128, blank=True, null=True)
