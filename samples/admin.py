from django.contrib import admin
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Identity, Sample
from .forms import SampleForm
from .crypto import hash_buf


class IdentityAdmin(admin.ModelAdmin):
    ...


class SampleAdmin(admin.ModelAdmin):
    form = SampleForm


admin.site.register(Identity, IdentityAdmin)
admin.site.register(Sample, SampleAdmin)
