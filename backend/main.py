from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signal")
async def get_signal():
    return {
        "pair": "XAU/USD",
        "direction": "Buy",
        "confidence": "82%",
        "tp": "3035",
        "sl": "3002",
        "explanation": "Support zone detected + Bullish MACD crossover"
    }