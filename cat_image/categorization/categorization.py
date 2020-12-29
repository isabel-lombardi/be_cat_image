import os

from torchvision import models, transforms
import torch
from PIL import Image


class Categorization:
    def __init__(self):
        self.images = []
        # pre-trained model
        self.resnet = models.resnet101(pretrained=True)

    def load_input_images(self):
        path = 'user_images'

        for image in os.listdir(path):
            if image != "README.md":
                self.images.append(Image.open(os.path.join(path, image)))