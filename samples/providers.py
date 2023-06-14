# -*- coding:utf-8 -*-
import hashlib
import typing as ty
import io

from django.conf import settings
from PIL import Image
from django.core.files import File

from faces.functional import load_image, crop_face
from samples.models import ImageInput, Sample, build_identity


class FaceSampler(object):

    @staticmethod
    def encode_input(input_: ImageInput) -> ty.List[Sample]:
        fp = input_.image.name
        fp = settings.MEDIA_ROOT / fp
        img = Image.open(fp)
        arr = load_image(img)

        findings = crop_face(arr)

        output = list()
        for sample, encoding in findings:
            buf = io.BytesIO()
            sample_img = Image.fromarray(sample)
            sample_img.save(buf, format='PNG')

            buf.seek(0)
            hasher = hashlib.sha256(buf.read())
            hash_ = hasher.hexdigest()

            buf.seek(0)

            sample = Sample()
            sample.identity = build_identity()
            sample.sample_value = encoding

            sample_file = File(buf)
            sample_file.name = '.'.join((str(input_.pk), hash_[0:8], 'png'))
            sample.sample_file = sample_file
            sample.sample_hash = hash_

            sample.save()
            output.append(sample)

        return output
