import io
import cv2
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, status
import numpy as np
from PIL import Image
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from src.img_service import TemplateImg
from src.llm_service import TemplateLLM
from src.prompts import ProjectParams
from src.parsers import ProjectIdeas
from src.config import get_settings

#FOR LOCAL EXECUTION
# from img_service import TemplateImg
# from llm_service import TemplateLLM
# from prompts import ProjectParams
# from parsers import ProjectIdeas
# from config import get_settings

SETTINGS = get_settings()


app = FastAPI(title=SETTINGS.service_name, version=SETTINGS.k_revision)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PeopleCountResponse(BaseModel):
    people_count: int


def get_llm_service():
    return TemplateLLM()

def get_img_service():
    return TemplateImg()


@app.post("/generate")
def generate_project(params: ProjectParams, service: TemplateLLM = Depends(get_llm_service)) -> ProjectIdeas:
    return service.generate(params)


@app.get("/")
def root():
    return {"status": "OK"}

@app.post("/get_number_of_people")
def get_number_of_people(file: UploadFile = File(...), service: TemplateImg = Depends(get_img_service)) -> PeopleCountResponse:
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Invalid file format")
    
    img_stream = io.BytesIO(file.file.read())
    img_stream.seek(0)
    img_array = np.array(bytearray(img_stream.read()), dtype=np.uint8)

    img = Image.open(img_stream)
    img = np.array(img)
    
    cv2.imwrite('./assets/img.png', img)
    return PeopleCountResponse(
        people_count=service.predict_image(SETTINGS.img_model)
    )
    


#to delete later
# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
