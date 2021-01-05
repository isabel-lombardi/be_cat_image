import os

from torchvision import models, transforms
import torch
from PIL import Image


# imagenet_classes file
imagenet_classes_file_path = os.path.join('categorization', 'imagenet_classes.txt')
file_abs_path = os.path.abspath(os.path.dirname(__file__))
imagenet_classes_file_path = os.path.join(file_abs_path, 'imagenet_classes.txt')


class Categorization:

    def __init__(self, images):
        self.images = images

        # pre-trained model
        self.resnet = models.resnet101(pretrained=True)

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
        result_ok = True
        result = {}

        for key, value in self.images.items():
            try:
                image_t = Categorization.transform_input_images(value)
                batch_t = torch.unsqueeze(image_t, 0)

                self.resnet.eval()          # network in eval mode
                out = self.resnet(batch_t)  # model inference

                try:
                    with open(imagenet_classes_file_path) as f:
                        classes = [line.strip() for line in f.readlines()]
                except IOError:
                    result_ok = False
                    return result_ok, result

                _, indices = torch.sort(out, descending=True)
                percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

                result[key] = [(classes[idx], percentage[idx].item()) for idx in indices[0][:1]]

            except:
                result[key] = None

        return result_ok, result

