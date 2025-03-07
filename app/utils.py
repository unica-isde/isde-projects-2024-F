import os

from app.config import Configuration
from PIL import Image, ImageEnhance

conf = Configuration()


def list_images():
    """
    Returns the list of available images.

     Outputs:
    --------
    - Returns a list of image filenames (as strings) with a `.JPEG` extension.

    """
    img_names = filter(
        lambda x: x.endswith(".JPEG"), os.listdir(conf.image_folder_path)
    )
    return list(img_names)


def scale_values(value: int) -> float:
    """This function scales the values obtained from the form on the editor page,
    which range from -100 to 100, to a range of 0 to 2, as the Pillow enhance arguments
    are limited to float values between 0 and 2.

    Arguments:
    - value {int} = it is the integer value to scale from -100÷100 to 0÷2 range.

    Returns:
    - value {float} = the scaled value in float format."""
    return (value + 100) / 100


def edit_image(original_image_path: str,
               color_value: int,
               brightness_value: int,
               contrast_value: int,
               sharpness_value: int,
               edited_image_path: str = "app/static/imagenet_subset/edited.jpg") -> None:
    """edit_image takes as input all the form parameters, including color_value,
      brightness_value, contrast_value, sharpness_value, and original_image_path.
      The original image is first copied to edited_image_path, which should always
      be app/static/imagenet_subset/edited.jpeg to ensure the correct functioning
      of the overall process. The edited.jpeg file is then modified using
      Pillow functions in combination with the scaled parameters obtained from the form.
      Finally, the edited image is saved in its modified format.

      Arguments:
          - original_image_path {str} = the original image path.
          - color_value {int}         = the color value selected from the form on the editor page.
          - brightness_value {int}    = the brightness value selected from the form on the editor page.
          - contrast_value {int}      = the contrast value selected from the form on the editor page.
          - sharpness_value {int}     = the sharpness value selected from the form on the editor page.
          - edited_image_path {str}   = the edited image path."app/static/imagenet_subset/edited.jpg" as default."""

    original_image = Image.open(original_image_path)
    edited_image = original_image.copy()

    # Scale and apply enhancements
    edited_image = ImageEnhance.Color(edited_image).enhance(scale_values(color_value))
    edited_image = ImageEnhance.Brightness(edited_image).enhance(scale_values(brightness_value))
    edited_image = ImageEnhance.Contrast(edited_image).enhance(scale_values(contrast_value))
    edited_image = ImageEnhance.Sharpness(edited_image).enhance(scale_values(sharpness_value))

    edited_image.save(edited_image_path, format="JPEG")
