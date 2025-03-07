from fastapi import Request, UploadFile


class EditedImageForm:
    """
    The EditedImageForm class is used to collect all the parameters submitted
     through the editor_select.html form and pass them to the backend for processing
     and image editing.

     """

    def __init__(self, request: Request) -> None:
        """
        Initializes a new instance of the class.

        This constructor sets up the initial attributes for handling a classification form request.
        It initializes the request object, an empty list for validation errors, and distinct parameters
        for processing the image.

        Inputs:
        -------
        request : Request --> The HTTP request containing form data.

        """
        self.request: Request = request
        self.errors: list = []
        self.model_id: str = ""
        self.image_id: str = ""
        self.color_value: int = 0
        self.brightness_value: int = 0
        self.contrast_value: int = 0
        self.sharpness_value: int = 0

    async def load_data(self):
        """
        Loads and processes form data from the HTTP request.

        This asynchronous method extracts form values from the request and assigns them to the
        corresponding instance variables. It is responsible for obtaining distinct characteristics such as
        model ID, image ID, color, brightness, contrast, and sharpness.


        """
        form = await self.request.form()
        self.model_id = form.get("model_id")
        self.image_id = form.get("image_id")
        self.color_value = int(form.get("color_value", 0))
        self.brightness_value = int(form.get("brightness_value", 0))
        self.contrast_value = int(form.get("contrast_value", 0))
        self.sharpness_value = int(form.get("sharpness_value", 0))

    def is_valid(self):
        """
        Validates the form data.

        This method checks if the required fields are present and correctly formatted.
        If any of these fields are missing or not of type str, an error message
        is added to the errors list.

        Outputs:
        --------
        bool
            - `True` --> `image_id` and `model_id` are valid.
            - `False` --> errors are stored in `errors` list.
        """
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
        """
        Initializes a new instance of the class.

        This constructor sets up the initial attributes for managing file upload and form data.
        It initializes the request object, the uploaded file (if any), and distinct attributes
        of the image as model ID, image ID, and values for color, brightness, contrast, and sharpness.

        Inputs:
        -------
        file : Optional[UploadFile] --> The uploaded file.
        request : Request --> The HTTP request containing the form data.

        """
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
        """
        Loads and processes form data from the HTTP request.

        This asynchronous method extracts form values from the request and assigns them to the
        corresponding instance variables. It is responsible for obtaining distinct characteristics such as
        model ID, color, brightness, contrast, and sharpness.


        """
        form = await self.request.form()

        self.model_id = form.get("model_id", "").strip()
        self.color_value = self.safe_int(form.get("color_value", 0))
        self.brightness_value = self.safe_int(form.get("brightness_value", 0))
        self.contrast_value = self.safe_int(form.get("contrast_value", 0))
        self.sharpness_value = self.safe_int(form.get("sharpness_value", 0))

    def safe_int(self, value, default=0):

        """
        Tries to convert a given value to an integer, returning a default value if the conversion fails.

        This method safely attempts to convert the provided value to an integer. If the conversion
        fails due to a ValueError or TypeError, it returns a default value instead.

        Inputs:
        -------
        value : Any --> The value to be converted to an integer.
        default : int (optional) --> The value to return if the conversion fails. Default is 0.

        Outputs:
        --------
        int --> The converted integer if successful, or the default value if not successful.

        """
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def is_valid(self):
        """
        Validates the required fields for the image processing form.

        This method checks whether the uploaded file and model ID, are provided.
        If any required field is not provided, it appends an appropriate error message
        to the `errors` list.

        Outputs:
        --------
        bool --> Returns True if the form is valid (no errors found), otherwise False.

        """
        if not self.file:
            self.errors.append("A valid image file is required.")
        if not self.model_id:
            self.errors.append("A valid model ID is required.")

        return not bool(self.errors)
