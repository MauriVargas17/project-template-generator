import csv
import datetime
from functools import cache
from io import StringIO
import statistics
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from src.models import Status, Sentiment, Analysis
from src.llm_service import TemplateLLM
from src.sentiment import TemplateSentiment
from src.analysis import TemplateAnalysis
from src.prompts import ProjectParams
from src.parsers import ProjectIdeas
from src.config import get_settings

SETTINGS = get_settings()

app = FastAPI(title=SETTINGS.api_name, version=SETTINGS.api_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=statistics.HTTP_404_NOT_FOUND,
        content={"detail": "Resource not found"},
    )

app.add_exception_handler(HTTPException, not_found_exception_handler)

entries = []
@cache
def get_llm_service():
    return TemplateLLM()
@cache
def get_sentiment_service():
    return TemplateSentiment()
@cache
def get_analysis_service():
    return TemplateAnalysis()


@app.post("/generate")
def generate_project(params: ProjectParams, service: TemplateLLM = Depends(get_llm_service)) -> ProjectIdeas:
    return service.generate(params)

@app.post("/sentiment", description="""
    This endpoint analyzes sentiment of financial text.

    Args:
        text (str): Text to analyze sentiment of in ENGLISH.

    Returns:
        Sentiment: Sentiment of the text, with confidence and how positive or negative it is, plus the time it took to analyze.

    Examples:
        "Stock Prices Soar as Company Beats Earnings Expectations"
        "Global Markets Experience Volatility Amid Economic Uncertainty"
        "Tech Giant Announces Record-Breaking Profits in Q3"
        "Investors React to Central Bank's Decision on Interest Rates"
        "Market Analysts Predict a Bearish Trend in the Coming Weeks"
       
    """)
def sentiment_analysis(text: str = "The market shows a strong uptrend", service:  TemplateSentiment = Depends(get_sentiment_service)) -> Sentiment:
    return service.analyze(text)

@app.post("/analysis", description="""
    This endpoint analyzes financial text.
          
    Args:
        text (str): Text to analyze sentiment of in ENGLISH.
          
    Returns:
        Analysis: Analysis of the text, with POS tagging, NER, embedding and sentiment, plus the time it took to analyze.
    
    Examples:
        "Stock Prices Soar as Company Beats Earnings Expectations"
        "Global Markets Experience Volatility Amid Economic Uncertainty"
        "Tech Giant Announces Record-Breaking Profits in Q3"
        "Investors React to Central Bank's Decision on Interest Rates"
        "Market Analysts Predict a Bearish Trend in the Coming Weeks"  
          """)
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

@app.get('/reports')
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
