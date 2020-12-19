import os
from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from .models import Identity, Sample
from .forms import SampleForm


class IdentityAdmin(admin.ModelAdmin):
    ...


class SampleAdmin(admin.ModelAdmin):
    form = SampleForm
    list_display = ('identity', 'alias_name', 'avatar_image', 'updated_at')

    def avatar_image(self, obj: Sample):
        if not obj.sample_file:
            return format_html('<span>Sample not found.</span>')

        path = os.path.join(settings.MEDIA_URL, obj.sample_file.name).replace('//', '/')
        return format_html('<img class="sample-avatar-image" src="{}" alt="{}"/>', path, obj.sample_file.name)

    avatar_image.short_description = 'Avatar Image'

    class Media:
        css = {
            'all': (
                'styles/change-form-samples.css',
            )
        }


admin.site.register(Identity, IdentityAdmin)
admin.site.register(Sample, SampleAdmin)
