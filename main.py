import uvicorn
import os
import io

from PIL import Image
from fastapi import Request, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles

from img2ascii import img_to_ascii


app = FastAPI()

STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=["Home"], status_code=status.HTTP_200_OK)
async def get_root(request: Request) -> dict:
    return JSONResponse(content={"Hello": "world"})


@app.get("/probe", tags=["Home"], status_code=status.HTTP_200_OK)
async def probe():
    return {"message": "I am the Python FastAPI API responding"}

@app.post("/upload", status_code=status.HTTP_200_OK)
async def upload(image_file: UploadFile):
    image_object = await image_file.read()
    image = Image.open(io.BytesIO(image_object))

    result = img_to_ascii.generate_ascii(image)

    return JSONResponse(content={"result": result}, status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run("main:app", port=7001, reload=True)
