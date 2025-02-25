from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from src.llm_service import TemplateLLM
from src.prompts import ProjectParams
from src.parsers import ProjectIdeas


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_llm_service():
    return TemplateLLM()


@app.post("/generate")
def generate_project(params: ProjectParams, service: TemplateLLM = Depends(get_llm_service)) -> ProjectIdeas:
    return service.generate(params)


@app.get("/")
def root():
    return {"status": "OK"}
