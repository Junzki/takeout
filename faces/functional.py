# -*- coding:utf-8 -*-
import copy
import cv2
import math
import numpy as np
import face_recognition
from typing import List, Tuple
from PIL import Image


def load_image(image: Image.Image):
    return np.array(image)


def draw_mark(image, face_locations, face_names):
    copied = copy.deepcopy(image)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(copied, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(copied, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(copied, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return copied


def crop_face(image) -> List[Tuple[np.array, np.array]]:
    results = []
    locs = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image)

    for y1, x2, y2, x1 in locs:
        size = x2 - x1
        point_scale = int(size * 0.26)

        x1a = x1 - point_scale
        x2a = x2 + point_scale
        y1a = y1 - int(math.floor(point_scale * 1.5))
        y2a = y2 + int(math.ceil(point_scale * 0.5))

        cropped = image[y1a:y2a, x1a:x2a]

        results.append(cropped)

    zipped = zip(results, encodings)
    return list(zipped)
