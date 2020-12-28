import os

from base64 import b64decode, b64encode
from PIL import Image
from io import BytesIO


class ProcessingImages:
    decoded_images = []

    def __init__(self, json):
        self.json = json

    def decoding(self):
        for value in self.json.values():
            image = Image.open(BytesIO(b64decode(value)))
            ProcessingImages.decoded_images.append(image)

        return ProcessingImages.decoded_images

    @staticmethod
    def save_image(idx, image):
        folder = "user_images"
        file_type = image.format

        image.save("{}/{}.{}".format(folder, idx, file_type.lower()), '{}'.format(file_type))