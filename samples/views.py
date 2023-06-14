# -*- coding:utf-8 -*-
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin

from samples.models import ImageInput
from samples.serializers import ImageInputSerializer


class ImageInputViewSet(GenericViewSet,
                        ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = ImageInput.objects.all()
    serializer_class = ImageInputSerializer

    parser_classes = [JSONParser, MultiPartParser]
