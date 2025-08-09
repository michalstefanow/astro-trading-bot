# backend/main.py
import os, math, re
from datetime import datetime
import requests, pandas as pd
from fastapi import FastAPI, Query, HTTPException, Body
from pydantic import BaseModel
from dotenv import load_dotenv
from twilio.rest import Client
import openai

load_dotenv()

app = FastAPI(title="TradeWithAns API")

# env
MARKET_API_KEY = os.getenv("MARKET_API_KEY")
NEWS_API_KEY   = os.getenv("NEWS_API_KEY")
AI_MODEL_KEY   = os.getenv("AI_MODEL_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")  # whatsapp:+14155238886
TWILIO_WHATSAPP_TO   = os.getenv("TWILIO_WHATSAPP_TO")    # whatsapp:+923137072879

openai.api_key = AI_MODEL_KEY
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class SignalResponse(BaseModel):
    asset: str
    timeframe: str
    direction: str
    entry: float
    tp: float
    sl: float
    confidence: float
    reason: str
    timestamp: str

def fetch_timeseries(symbol: str, interval: str, outputsize: int = 200) -> pd.DataFrame:
    url = "https://api.twelvedata.com/time_series"
    r = requests.get(url, params={
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": MARKET_API_KEY
    }, timeout=12)
    data = r.json()
    if "values" not in data:
        raise ValueError(f"TwelveData error: {data}")
    df = pd.DataFrame(data["values"])
    df["close"] = df["close"].astype(float)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)
    return df

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # EMA
    df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()
    # RSI
    delta = df["close"].diff()
    up, down = delta.clip(lower=0), -delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/14, adjust=False).mean()
    ma_down = down.ewm(alpha=1/14, adjust=False).mean()
    rs = ma_up / ma_down
    df["RSI"] = 100 - (100 / (1 + rs))
    # MACD
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
    return df

def support_resistance(df: pd.DataFrame, lookback: int = 100):
    return float(df["close"].rolling(lookback).max().iloc[-1]), float(df["close"].rolling(lookback).min().iloc[-1])

def rule_signal(df: pd.DataFrame, symbol: str):
    latest = df.iloc[-1]
    ema_bull = latest["EMA20"] > latest["EMA50"]
    macd_bull = latest["MACD"] > latest["MACD_SIGNAL"]
    rsi = latest["RSI"]
    direction, confidence = "HOLD", 50
    if ema_bull and macd_bull and rsi < 35:
        direction, confidence = "BUY", 85
    elif (not ema_bull) and (not macd_bull) and rsi > 65:
        direction, confidence = "SELL", 85
    elif ema_bull and macd_bull:
        direction, confidence = "BUY", 70
    elif (not ema_bull) and (not macd_bull):
        direction, confidence = "SELL", 70

    entry = float(latest["close"])
    vol = df["close"].rolling(14).std().iloc[-1]
    vol = 1.0 if (pd.isna(vol) or vol == 0) else vol
    sl = entry - 2*vol if direction == "BUY" else entry + 2*vol
    tp = entry + 3*vol if direction == "BUY" else entry - 3*vol
    reason = f"EMA20 {'>' if ema_bull else '<='} EMA50 | MACD {'>' if macd_bull else '<='} Signal | RSI {rsi:.1f}"
    return direction, entry, tp, sl, confidence, reason

def ask_llm(prompt: str) -> str:
    if not AI_MODEL_KEY: return ""
    try:
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=160,
            temperature=0.1
        )
        return resp.choices[0].text.strip()
    except Exception:
        return ""

@app.get("/api/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.get("/api/signal", response_model=SignalResponse)
def signal(symbol: str = Query("XAU/USD"), interval: str = Query("30min")):
    # 1) data
    df = fetch_timeseries(symbol, interval)
    df = add_indicators(df)
    hi, lo = support_resistance(df)
    # 2) rule
    direction, entry, tp, sl, confidence, reason = rule_signal(df, symbol)
    # 3) news
    headlines = ""
    if NEWS_API_KEY:
        try:
            q = f"{symbol} market"
            j = requests.get("https://newsapi.org/v2/everything",
                             params={"q": q, "apiKey": NEWS_API_KEY, "pageSize": 4, "language": "en", "sortBy": "relevancy"},
                             timeout=8).json()
            headlines = " | ".join([a["title"] for a in j.get("articles", [])])
        except Exception:
            pass
    # 4) LLM refine/explain
    prompt = (
        f"Symbol: {symbol}\n"
        f"Latest price: {entry}\n"
        f"Indicators: RSI {df['RSI'].iloc[-1]:.1f}, MACD {df['MACD'].iloc[-1]:.4f}, "
        f"EMA20 {df['EMA20'].iloc[-1]:.2f}, EMA50 {df['EMA50'].iloc[-1]:.2f}\n"
        f"Support {lo:.2f}, Resistance {hi:.2f}\n"
        f"Headlines: {headlines}\n"
        f"Rule suggests {direction} with TP {tp:.2f} and SL {sl:.2f}. "
        f"Confirm BUY/SELL/HOLD with a short reason and (optional) better TP/SL and confidence %."
    )
    ai = ask_llm(prompt)
    # parse ai a bit
    if ai:
        U = ai.upper()
        if "BUY" in U and "SELL" not in U: direction = "BUY"
        elif "SELL" in U and "BUY" not in U: direction = "SELL"
        elif "HOLD" in U: direction = "HOLD"
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", ai)
        if len(nums) >= 2:
            try:
                tp_c, sl_c = float(nums[0]), float(nums[1])
                if 0 < tp_c < entry*10: tp = tp_c
                if 0 < sl_c < entry*10: sl = sl_c
            except: pass
        m = re.search(r"(\d{1,3})\s*%", U)
        if m:
            try: confidence = max(0, min(100, int(m.group(1))))
            except: pass
        reason = ai.split("\n")[0].strip()

    # 5) alert if strong
    if twilio_client and direction in ("BUY","SELL") and confidence >= 75 and TWILIO_WHATSAPP_FROM and TWILIO_WHATSAPP_TO:
        try:
            body = (f"🚨 {symbol} {direction}\nEntry: {entry:.2f}\nTP: {tp:.2f}\nSL: {sl:.2f}\n"
                    f"Conf: {confidence}%\n{reason}")
            twilio_client.messages.create(
                body=body,
                from_=TWILIO_WHATSAPP_FROM,
                to=TWILIO_WHATSAPP_TO
            )
        except Exception as e:
            print("Twilio error:", e)

    return SignalResponse(
        asset=symbol, timeframe=interval, direction=direction,
        entry=float(entry), tp=float(tp), sl=float(sl),
        confidence=float(confidence), reason=reason,
        timestamp=datetime.utcnow().isoformat()
    )

@app.post("/api/ask")
def ask(q: dict = Body(...)):
    question = q.get("q","").strip()
    if not question: return {"answer":"Ask me anything about the current market or your signal."}
    prompt = f"You are Astro, a friendly pro trading assistant. Be concise.\nQ: {question}\nA:"
    ans = ask_llm(prompt) or "AI is not configured yet."
    return {"answer": ans}
