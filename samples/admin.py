from django.contrib import admin
from .models import Identity, Sample
from .forms import SampleForm


class IdentityAdmin(admin.ModelAdmin):
    ...


class SampleAdmin(admin.ModelAdmin):
    form = SampleForm
    list_display = ('identity', 'alias_name', 'sample_file', 'updated_at')


admin.site.register(Identity, IdentityAdmin)
admin.site.register(Sample, SampleAdmin)
