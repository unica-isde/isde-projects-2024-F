import os

from app.config import Configuration
from PIL import Image, ImageEnhance

conf = Configuration()


def list_images():
    """Returns the list of available images."""
    img_names = filter(
        lambda x: x.endswith(".JPEG"), os.listdir(conf.image_folder_path)
    )
    return list(img_names)



# Needed to edit images
# Scale value function is used since input values range from -100 to 100
# while PILLOW only manages values between 0 and 2
def scale_values(value: int) -> float:
    return (value + 100) / 100


def edit_image(original_image_path: str,
               color_value: int,
               brightness_value: int,
               contrast_value: int,
               sharpness_value: int,
               edited_image_path : str) -> None:

    original_image = Image.open(original_image_path)
    edited_image = original_image.copy()

    # Scale and apply enhancements
    edited_image = ImageEnhance.Color(edited_image).enhance(scale_values(color_value))
    edited_image = ImageEnhance.Brightness(edited_image).enhance(scale_values(brightness_value))
    edited_image = ImageEnhance.Contrast(edited_image).enhance(scale_values(contrast_value))
    edited_image = ImageEnhance.Sharpness(edited_image).enhance(scale_values(sharpness_value))

    edited_image.save(edited_image_path, format ="JPEG")
