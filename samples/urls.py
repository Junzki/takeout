# -*- coding:utf-8 -*-
from rest_framework.routers import DefaultRouter

from samples.views import ImageInputViewSet


router = DefaultRouter()
router.register(r'images', ImageInputViewSet, basename='images')


urlpatterns = router.urls
