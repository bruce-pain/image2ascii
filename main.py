import uvicorn
import os
import io

from PIL import Image
from fastapi import Request, UploadFile, FastAPI, status, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from img2ascii import img_to_ascii


app = FastAPI()
templates = Jinja2Templates(directory="templates")

STATIC_DIR = "static"
VALID_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


def file_validation(file: UploadFile):
    filename = file.filename
    ext = filename.split(".")[-1]

    if ext.lower() not in VALID_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Supported files include {', '.join(VALID_EXTENSIONS)}",
        )


@app.get("/", tags=["Home"], status_code=status.HTTP_200_OK)
async def get_root(request: Request) -> dict:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/probe", tags=["Home"], status_code=status.HTTP_200_OK)
async def probe():
    return {"message": "I am the Python FastAPI API responding"}


@app.post("/upload", status_code=status.HTTP_200_OK)
async def upload(
    image_file: UploadFile,
    width: int = Query(default=150),
    character_set: str = Query(default="basic"),
    is_colored: bool = Query(default=False),
):
    file_validation(image_file)

    image_object = await image_file.read()
    image = Image.open(io.BytesIO(image_object))

    result = img_to_ascii.generate_ascii(source_image=image, ramp_choice=character_set, colored=is_colored, image_width=width)

    return JSONResponse(content={"result": result}, status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run("main:app", port=7001, reload=True)
