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


class UploadedImageForm:
    """
    The UploadedImageForm class is used to collect and validate the file and model ID
    submitted through the form in the classification_upload.html template.

    This form is designed to handle the input from the user for the image upload process.
    It ensures that a file is uploads and a valid model ID is provided before proceeding
    with image classification.
    """

    def __init__(self, file: UploadFile, model_id: str) -> None:
        self.file = file
        self.model_id = model_id
        self.errors = []

    def is_valid(self):
        if not self.file:
            self.errors.append("An image file is required")
        if not self.model_id:
            self.errors.append("A valid model ID is required")
        return not self.errors