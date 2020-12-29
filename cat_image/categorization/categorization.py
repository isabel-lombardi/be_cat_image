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

    # Transform the input image with values similar to those used during model training.
    @staticmethod
    def transform_input_images(image):
        transform = transforms.Compose([
            transforms.Resize(256),        # Resize to 256×256 pixels
            transforms.CenterCrop(224),    # Crop to 224×224 pixels about the center
            transforms.ToTensor(),         # Convert to PyTorch Tensor data type

            # Normalize with mean and standard deviation
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
        return transform(image)

    def use_template(self):
        result = {}

        for idx, image in enumerate(self.images, 1):
            image_t = Categorization.transform_input_images(image)
            batch_t = torch.unsqueeze(image_t, 0)

            self.resnet.eval()          # network in eval mode
            out = self.resnet(batch_t)  # model inference

            with open('imagenet_classes.txt') as f:
                classes = [line.strip() for line in f.readlines()]

            _, indices = torch.sort(out, descending=True)
            percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

            result[idx] = [(classes[idx], percentage[idx].item()) for idx in indices[0][:1]]

        return result