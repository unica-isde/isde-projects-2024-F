import json
from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import Configuration
from app.forms.classification_form import EditedImageForm, UploadedImageForm
from app.ml.classification_utils import classify_image, store_uploaded_image
from app.utils import list_images, edit_image
import os

app = FastAPI()
config = Configuration()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "app/static")),
    name="static"
)
templates = Jinja2Templates(directory="app/templates")


@app.get("/info")
def info() -> dict[str, list[str]]:
    """
    Retrieves available models and images.

    This function compiles a list of preconfigured model names and available
    image files, returning them in a structured dictionary format.

    Returns
    -------
    dict[str, list[str]]
        A dictionary containing:
        - "models": A list of available model names.
        - "images": A list of available image filenames.
    """
    list_of_images = list_images()
    list_of_models = Configuration.models
    return {"models": list_of_models, "images": list_of_images}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Renders the home page of the service.

    This function handles the request to render the home page using a
    predefined HTML template.

    Parameters
    ----------
    request : Request
        The HTTP request containing data about the client's request.

    Returns
    -------
    TemplateResponse
        The rendered "home.html" page.
    """
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/editor")
def editor_get(request: Request):
    """
    Renders the editor selection page.

    This function handles GET requests to the `/editor` endpoint and
    serves an HTML template that provides the user interface for selecting
    images, models, and image editing parameters.

    Parameters
    ----------
    request : Request
        The HTTP request object.

    Returns
    -------
    TemplateResponse
        The rendered "editor_select.html" page with available images and models.
    """
    return templates.TemplateResponse(
        "editor_select.html",
        {
            "request": request,
            "images": list_images(),
            "models": Configuration.models
        },
    )


@app.post("/editor", response_class=HTMLResponse)
async def editor_post(request: Request):
    """
    Processes edited image classification.

    This function handles POST requests to the `/editor` endpoint.
    It collects parameters from the form on the "editor_select.html" page,
    processes the image using `edit_image()`, and classifies the edited image.

    Parameters
    ----------
    request : Request
        The HTTP request containing form data.

    Returns
    -------
    TemplateResponse
        The rendered "editor_output.html" page with classification results.
    """
    form = EditedImageForm(request)
    await form.load_data()

    if not form.is_valid():
        return {"errors": form.errors}

    original_image_path = f"app/static/imagenet_subset/{form.image_id}"
    edited_image_path = "app/static/imagenet_subset/edited.jpg"

    edit_image(
        original_image_path,
        form.color_value,
        form.brightness_value,
        form.contrast_value,
        form.sharpness_value,
        edited_image_path
    )

    edited_image_id = "edited.jpg"
    classification_scores = classify_image(form.model_id, edited_image_id)

    return templates.TemplateResponse(
        "editor_output.html",
        {
            "request": request,
            "image_id": edited_image_id,
            "classification_scores": json.dumps(classification_scores),
        }
    )


@app.get("/upload")
def upload_get(request: Request):
    """
    Renders the image upload page.

    This function handles GET requests for the `/upload` endpoint and
    serves the "classification_upload.html" template.

    Parameters
    ----------
    request : Request
        The HTTP request object.

    Returns
    -------
    TemplateResponse
        The rendered "classification_upload.html" page.
    """
    return templates.TemplateResponse(
        "classification_upload.html",
        {
            "request": request,
            "models": Configuration.models
        },
    )


@app.post("/upload")
async def upload_post(request: Request, file: UploadFile = File(...)):
    """
    Handles image upload and classification.

    This function processes an uploaded image, applies image transformations
    (color, brightness, contrast, sharpness), classifies the image using a
    selected model, and returns the classification results.

    Parameters
    ----------
    request : Request
        The HTTP request containing form data.
    file : UploadFile
        The image file uploaded by the user.

    Returns
    -------
    TemplateResponse
        The rendered "classification_upload_output.html" page with classification results.
    """
    form = UploadedImageForm(file=file, request=request)
    await form.load_data()

    if not form.is_valid():
        return {"errors": form.errors}

    filename = store_uploaded_image(form.file)

    original_image_path = f"app/static/uploads/{filename}"
    edited_image_path = "app/static/imagenet_subset/edited.jpg"

    edit_image(
        original_image_path,
        form.color_value,
        form.brightness_value,
        form.contrast_value,
        form.sharpness_value,
        edited_image_path
    )

    classification_scores = classify_image(model_id=form.model_id, img_id=filename)

    return templates.TemplateResponse(
        "classification_upload_output.html",
        {
            "request": request,
            "image_id": filename,
            "image_path": f"/static/uploads/{filename}",
            "classification_scores": json.dumps(classification_scores),
        },
    )
