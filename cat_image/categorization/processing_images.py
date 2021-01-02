from base64 import b64decode
from PIL import Image
from io import BytesIO


class ProcessingImages:
    def __init__(self, json):
        self.json = json

    def decoding(self):
        """Returns a tuple result_ok, decoded_images, wrong_files_id:
            result_ok = False if the format of some images is wrong
            decoded_images = the decoded images in a dictionary
            wrong_files_id = the ids of the wrong images in a list

        :return: result_ok, decoded_images, wrong_files_id
        """
        result_ok = True
        decoded_images = {}
        wrong_files_id = []
        for key in self.json:
            try:
                decoded_image = Image.open(BytesIO(b64decode(self.json[key])))
            except:
                result_ok = False
                wrong_files_id.append(key)
                continue
            decoded_images[key] = decoded_image
        return result_ok, decoded_images, wrong_files_id
