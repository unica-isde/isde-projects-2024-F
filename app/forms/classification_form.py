from fastapi import Request


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


# classification form for edited images
class EditedImageForm:
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

