"""
This is a simple classification service. It accepts an url of an
image and returns the top-5 classification labels and scores.
"""
import importlib
import json
import logging
import os
import torch
from PIL import Image

from torchvision import transforms
from fastapi import UploadFile

from app.config import Configuration


conf = Configuration()


def fetch_image(image_id):
    """
    Modified function to get the image from the dataset or upload folder

    This function try to get an image using the provided image ID. It first checks if
    the image exists in the upload folder. If exists, it opens and returns the image.
    Otherwise, it attempts to fetch the image from the default image folder.


    Inputs:
    -------
    image_id : str --> The filename or identifier of the image to be found.

    Outputs:
    --------
    Image.Image --> The opened image file as a PIL Image object.

    """
    if os.path.exists(os.path.join(conf.upload_folder_path, image_id)):
        print("debug path exist")
        return Image.open(os.path.join(conf.upload_folder_path, image_id))
    return Image.open(os.path.join(conf.image_folder_path, image_id))


def store_uploaded_image(file: UploadFile) -> str:
    """
    Saves an uploaded image to the designated upload folder and returns its filename.

    This function takes an uploaded image file, saves it to the directory,
    and returns the name of the saved file.

    Inputs:
    -------
    file : UploadFile --> The uploaded file containing the image data.

    Outputs:
    --------
    str --> The filename of the saved image.

    """
    file_path = os.path.join(conf.upload_folder_path, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file.filename

def get_labels():
    """
    Returns the labels of Imagenet dataset as a list, where
    the index of the list corresponds to the output class.

    This function loads the Imagenet class labels from a JSON file and returns them as a list.

    Outputs:
    --------
    list --> A list of ImageNet labels where each index represents a class.

    """
    labels_path = os.path.join(conf.image_folder_path, "imagenet_labels.json")
    with open(labels_path) as f:
        labels = json.load(f)
    return labels


def get_model(model_id):
    """
    Imports a pretrained model from the ones that are specified in
    the configuration file. This is needed as we want to pre-download the
    specified model in order to avoid unnecessary waits for the user

    Inputs:
    -------
    model_id : str --> The identifier of the model to be loaded (must be in `conf.models`).

    Outputs:
    --------
    torch.nn.Module --> The loaded PyTorch model with default pretrained weights.

    """
    if model_id in conf.models:
        try:
            module = importlib.import_module("torchvision.models")
            return module.__getattribute__(model_id)(weights="DEFAULT")
        except ImportError:
            logging.error("Model {} not found".format(model_id))
    else:
        raise ImportError


def classify_image(model_id, img_id):
    """
    Returns the top-5 classification score output from the
    model specified in model_id when it is fed with the
    image corresponding to img_id.

    Inputs:
    -------
    model_id : str --> The identifier of the pretrained model to be used for classification.
    img_id : str --> The identifier (filename) of the image to be classified.

    Outputs:
    --------
    list --> A list of the top-5 classification results, where each item is a tuple:
             (label_name: str, confidence_score: float)

    """
    img = fetch_image(img_id)
    model = get_model(model_id)
    model.eval()
    transform = transforms.Compose(
        (
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        )
    )

    # apply transform from torchvision
    img = img.convert("RGB")
    preprocessed = transform(img).unsqueeze(0)

    # gets the output from the model
    out = model(preprocessed)
    _, indices = torch.sort(out, descending=True)

    # transforms scores as percentages
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

    # gets the labels
    labels = get_labels()

    # takes the top-5 classification output and returns it
    # as a list of tuples (label_name, score)
    output = [[labels[idx], percentage[idx].item()] for idx in indices[0][:5]]

    img.close()
    return output
