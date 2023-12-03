import csv
import datetime
from functools import cache
from io import StringIO
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from src.utils.models import Status, Sentiment, Analysis
from src.services.llm_service import TemplateLLM
from src.services.sentiment import TemplateSentiment
from src.services.analysis import TemplateAnalysis
from src.utils.prompts import TextParams
from src.utils.config import get_settings
from src.resources.descriptions import sentiment_description, analysis_description, reports_description

SETTINGS = get_settings()

app = FastAPI(title=SETTINGS.api_name, version=SETTINGS.api_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

entries = []

def create_entry(text: str, analysis: Analysis):
    return {
        "id": len(entries) + 1,
        "text": text,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pos_tagging": analysis.pos_tagging,
        "ner": analysis.ner,
        "sentiment_category": analysis.sentiment.category,
        "sentiment_confidence": analysis.sentiment.confidence,
        "sentiment_value_in_range": analysis.sentiment.value_in_range,
        "sentiment_time_ms": analysis.sentiment.time_ms,
        "time_ms": analysis.total_time_ms,
        "models_used": f"{SETTINGS.models['Analysis']} and {SETTINGS.models['Sentiment']}",

    }

# Obtaining services
@cache
def get_llm_service():
    return TemplateLLM()
@cache
def get_sentiment_service():
    return TemplateSentiment()
@cache
def get_analysis_service():
    return TemplateAnalysis()

# API endpoints
@app.post("/analysis_v2", description=analysis_description)
def generate_project(params: TextParams, service: TemplateLLM = Depends(get_llm_service)) -> Analysis:
    return service.generate(params)

@app.post("/sentiment", description=sentiment_description)
def sentiment_analysis(text: str = "The market shows a strong uptrend", service:  TemplateSentiment = Depends(get_sentiment_service)) -> Sentiment:
    return service.analyze(text)

@app.post("/analysis", description=analysis_description)
def text_analysis(text: str = "The market shows a bad trend as Martin showed in Alaska last week", service: TemplateAnalysis = Depends(get_analysis_service)) -> Analysis:
    analysis = service.analyze(text)
    entries.append(create_entry(text, analysis))
    return analysis

@app.get("/status")
def get_status() -> Status:
    return Status(
        status="OK",
        version=SETTINGS.api_version,
        models_hosted=SETTINGS.models.values(),
    )

@app.get('/reports', description=reports_description)
async def export_csv():
    if not entries:
        raise HTTPException(status_code=404, detail="No data available")

    csv_data = StringIO()
    csv_writer = csv.DictWriter(
        csv_data,
        fieldnames=[
            "id",
            "text",
            "date",
            "pos_tagging",
            "ner",
            "sentiment_category",
            "sentiment_confidence",
            "sentiment_value_in_range",
            "sentiment_time_ms",
            "time_ms",
            "models_used",

        ],
    )
    csv_writer.writeheader()
    csv_writer.writerows(entries)

    response = StreamingResponse(
        iter([csv_data.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=reports.csv",
        },
    )

    return response
