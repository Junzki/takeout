# -*- coding:utf-8 -*-
import typing as ty
import time
import uuid
import hashlib

from django.core.files import File
from rest_framework import serializers
from .models import ImageInput


class ImageInputSerializer(serializers.ModelSerializer):

    image = serializers.ImageField()

    def validate(self, attrs):
        image = attrs['image']

        try:
            _, ext = image.name.rsplit('.', 1)
        except (ValueError, IndexError):
            raise serializers.ValidationError('Invalid file name')

        hasher = hashlib.sha256(image.file.read())
        hash_ = str(hasher.hexdigest())

        prefix = str(int(time.time()))
        suffix = hash_[0:8]

        name_overwrite = '.'.join((prefix, suffix, ext))
        image.file.seek(0)
        image.name = name_overwrite

        attrs['image_hash'] = hash_

        return attrs

    class Meta:
        model = ImageInput
        fields = [
            'image',
            'image_hash',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'image_hash',
            'created_at',
            'updated_at'
        ]
