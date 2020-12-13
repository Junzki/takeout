# -*- coding:utf-8 -*-
import uuid
from django.db import models
from django.conf import settings


def build_identity() -> str:
    return str(uuid.uuid4())


class Identity(models.Model):
    key = models.CharField(max_length=255, null=False, blank=False, default=build_identity,
                           verbose_name='Identity Key')
    alias_name = models.CharField(max_length=255, null=False, blank=True, default='', verbose_name='Alias Name')

    def __str__(self):
        return f'Identity {self.alias_name} - {self.key}'


class Sample(models.Model):
    identity = models.CharField(max_length=255, null=False, blank=False, verbose_name='Identity Key')
    alias_name = models.CharField(max_length=255, null=False, blank=True, default='', verbose_name='Alias Name')
    sample_value = models.BinaryField(null=True, verbose_name='Sample Value')

    sample_file = models.ImageField(upload_to=settings.SAMPLE_UPLOAD_PATH, null=True, default=None,
                                    verbose_name='Sample File')
    sample_hash = models.CharField(max_length=128, null=True, blank=False, default=None,
                                   verbose_name='Sample File HMAC-SHA256')
    primary = models.BooleanField(default=False, null=False, verbose_name='Is Primary Sample')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return f'Sample {self.alias_name} - {self.identity}'
