import json
import logging
import os
import shutil
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import requests

from config import Configuration


def prepare_images():
    """
    Downloads a subset of the Imagenet Dataset if not already present.

    This function checks if the specified image folder exists. If not, it downloads a ZIP
    file containing a subset of the Imagenet dataset from a given URL. The ZIP file is
    extracted, and the images are stored in the configured image folder.

    """
    img_folder = Configuration().image_folder_path
    if not os.path.exists(img_folder):
        zip_url = (
            "https://github.com/EliSchwartz/"
            "imagenet-sample-images/archive/master.zip"
        )
        with urlopen(zip_url) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(img_folder)
    sub_dir = os.path.join(img_folder, "imagenet-sample-images-master")
    if os.path.exists(sub_dir):
        files = os.listdir(sub_dir)
        for f in files:
            shutil.move(os.path.join(sub_dir, f), img_folder)
        shutil.rmtree(sub_dir)
    logging.info(f"Images downloaded and stored in {img_folder}.")


def prepare_labels():
    """
    Saves a JSON file containing Imagenet labels as a list where
    the index is the label ID of the class.

    This function retrieves a JSON file containing simplified ImageNet labels
    where the index of the list corresponds to the label ID of the class.
    The labels are downloaded from a public URL and saved to the specified
    image folder as "imagenet_labels.json".

    """
    img_folder = Configuration().image_folder_path
    labels_path = os.path.join(img_folder, "imagenet_labels.json")
    imagenet_labels_path = (
        "https://raw.githubusercontent.com/"
        "anishathalye/imagenet-simple-labels/"
        "master/imagenet-simple-labels.json"
    )
    r = requests.get(imagenet_labels_path)
    data = r.json()
    with open(labels_path, "w") as f:
        json.dump(data, f)
    logging.info(f"Labels downloaded and stored in {labels_path}.")


if __name__ == "__main__":
    prepare_images()
    prepare_labels()
