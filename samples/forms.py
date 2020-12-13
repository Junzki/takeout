# -*- coding:utf-8 -*-
import datetime
from typing import Optional
from django import forms
from django.core.files import File
from .crypto import hash_buf
from .models import Sample


class ImageInputWidget(forms.FileInput):
    template_name = 'samples/file.html'


class SampleForm(forms.ModelForm):
    FIELD_NAME_SAMPLE_FILE = 'sample_file'
    FIELD_NAME_SAMPLE_HASH = 'sample_hash'

    # sample_file = forms.ImageField(widget=ImageInputWidget)
    
    def save(self, commit=True):
        file_: Optional[File] = self.instance.sample_file
        if self.FIELD_NAME_SAMPLE_FILE in self.changed_data and file_:
            name = file_.name
            buf = file_.file.read()
            file_.file.seek(0)

            hash_ = hash_buf(buf)

            if '.' in name:
                _, ext = name.rsplit('.', 1)
                name = f'{hash_}.{ext}'
            else:
                name = hash_

            current = datetime.date.today().strftime('%Y%m%d')
            name = f'{current}_{name}'

            file_.name = name

            self.instance.sample_file = file_
            self.instance.sample_hash = hash_
            self.changed_data.append(self.FIELD_NAME_SAMPLE_HASH)

        return super(SampleForm, self).save(commit)

    class Meta:
        model = Sample
        fields = '__all__'
        # widgets = {
        #     'sample_file': ImageInputWidget(),
        # }
