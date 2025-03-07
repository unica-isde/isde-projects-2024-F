import json
from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import Configuration
from app.forms.classification_form import EditedImageForm, UploadedImageForm
from app.ml.classification_utils import classify_image, store_uploaded_image
from app.utils import list_images, edit_image

app = FastAPI()
config = Configuration()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/info")
def info() -> dict[str, list[str]]:
    """
    Returns a dictionary containing available models and images.

    This function compiles a list of preconfigured model names and available
    image files, returning them in a structured dictionary format.

    Outputs:
    --------
    - Returns a dictionary named data with:
      - "models": A list of model names.
      - "images": A list of available image.

    """
    list_of_images = list_images()
    list_of_models = Configuration.models
    data = {"models": list_of_models, "images": list_of_images}
    return data


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    The home page of the service.

    This function handles the request to render the home page using a
    predefined HTML template.

    Inputs:
    -------
    request : Request --> The HTTP request containing data about the client's request.


    Outputs:
    --------
    TemplateResponse --> Returns an HTML response generated from the "home.html" template,
    with the request object passed as context.


    """
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/editor")
def editor_get(request: Request):
    """
    The editor_get function handles GET requests to the /editor endpoint and renders
    the editor selection page. It serves an HTML template that provides the user
    interface for selecting images,models, and image editing parameters.
    The template is populated with a list of available images and models
    retrieved from the system configuration.

    Inputs:
    -------
    request : Request --> The HTTP request object.

    Returns:
    --------
    TemplateResponse --> The rendered "editor_select.html" page with available images and models.

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
async def request_edited_classification(request: Request):
    """
    The request_edited_classification function handles POST requests to the /editor endpoint.
    It collects all parameters from the form on the "editor_select.html" page and passes them
    to the edit_image function to generate the edited image. The edited image is then classified,
    and both the edited image and classification results are returned to the client
    via the "editor_output.html" template.

    Inputs:
    -------
    request : Request --> The HTTP request containing form data.

    Output:
    --------
    TemplateResponse --> The rendered "editor_output.html" page with classification results.

    """
    form = EditedImageForm(request)
    await form.load_data()

    if not form.is_valid():
        return {"errors": form.errors}

    original_image_path = f"app/static/imagenet_subset/{form.image_id}"
    edited_image_path = "app/static/imagenet_subset/edited.jpg"

    color_value = form.color_value
    brightness_value = form.brightness_value
    contrast_value = form.contrast_value
    sharpness_value = form.sharpness_value

    edit_image(
        original_image_path,
        color_value,
        brightness_value,
        contrast_value,
        sharpness_value,
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
def upload(request: Request):
    """
    Handles GET requests for the image upload page.

    This function renders the "classification_upload.html" template,
    which allows users to upload an image for classification.

    Inputs:
    -------
    request : Request --> The HTTP request object.

    Output:
    --------
    TemplateResponse --> The rendered "classification_upload.html" page.
    """
    return templates.TemplateResponse(
        "classification_upload.html",
        {
            "request": request,
            "models": Configuration.models
        },
    )


@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    """
    Handles POST requests for uploading and classifying an image.

    This function processes an uploaded image, applies image transformations (color, brightness, contrast, sharpness),
    performs classification using a selected model, and returns the classification results along with the image.

    Inputs:
    -------
    request : Request --> The HTTP request containing form data.
    file : UploadFile --> The image file uploaded by the user.

    Output:
    --------
    TemplateResponse --> The rendered "classification_upload_output.html" page with classification results and image path.
    """
    form = UploadedImageForm(file=file, request=request)
    await form.load_data()

    if not form.is_valid():
        return {"errors": form.errors}

    filename = store_uploaded_image(form.file)

    image_id = filename
    original_image_path = f"app/static/uploads/{image_id}"
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
