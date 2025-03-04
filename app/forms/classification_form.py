from fastapi import Request, UploadFile


class ClassificationForm:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: list = []
        self.image_id: str = ""
        self.model_id: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.image_id = form.get("image_id")
        self.model_id = form.get("model_id")

    def is_valid(self):
        if not self.image_id or not isinstance(self.image_id, str):
            self.errors.append("A valid image id is required")
        if not self.model_id or not isinstance(self.model_id, str):
            self.errors.append("A valid model id is required")
        if not self.errors:
            return True
        return False


class EditedImageForm:
    """ The EditedImageForm class is used to collect all the parameters submitted
     through the editor_select.html form and pass them to the backend for processing
     and image editing."""

    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: list = []
        self.model_id: str = ""
        self.image_id: str = ""
        self.color_value: int = 0
        self.brightness_value: int = 0
        self.contrast_value: int = 0
        self.sharpness_value: int = 0

    async def load_data(self):
        form = await self.request.form()
        self.model_id = form.get("model_id")
        self.image_id = form.get("image_id")
        self.color_value = int(form.get("color_value", 0))
        self.brightness_value = int(form.get("brightness_value", 0))
        self.contrast_value = int(form.get("contrast_value", 0))
        self.sharpness_value = int(form.get("sharpness_value", 0))

    def is_valid(self):
        if not self.image_id or not isinstance(self.image_id, str):
            self.errors.append("A valid image id is required")
        if not self.model_id or not isinstance(self.model_id, str):
            self.errors.append("A valid model id is required")
        if not self.errors:
            return True
        return False


from fastapi import Request, UploadFile
from typing import Optional


class UploadedImageForm:
    """
    The UploadedImageForm class is used to collect and validate the file, model ID,
    and additional image editing parameters submitted through the form in the
    classification_upload.html and editor_select.html templates.

    This form ensures that a file is uploaded, a valid model ID is provided, and any
    optional image editing parameters are properly handled before proceeding with
    image classification or editing.
    """

    def __init__(self, file: Optional[UploadFile], request: Request) -> None:
        self.request: Request = request
        self.file: Optional[UploadFile] = file
        self.errors: list = []
        self.model_id: str = ""
        self.image_id: str = ""
        self.color_value: int = 0
        self.brightness_value: int = 0
        self.contrast_value: int = 0
        self.sharpness_value: int = 0

    async def load_data(self):
        """Loads form data from the request."""
        form = await self.request.form()

        self.model_id = form.get("model_id", "").strip()
        self.color_value = self.safe_int(form.get("color_value", 0))
        self.brightness_value = self.safe_int(form.get("brightness_value", 0))
        self.contrast_value = self.safe_int(form.get("contrast_value", 0))
        self.sharpness_value = self.safe_int(form.get("sharpness_value", 0))

    def safe_int(self, value, default=0):
        """Safely converts a value to an integer, returning a default if conversion fails."""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def is_valid(self):
        """Validates the form fields."""
        if not self.file:
            self.errors.append("A valid image file is required.")
        if not self.model_id:
            self.errors.append("A valid model ID is required.")

        return not bool(self.errors)  # Returns True if no errors exist
