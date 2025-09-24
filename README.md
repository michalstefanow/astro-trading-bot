# 🚀 Astro Trading Bot

A modern, AI-powered trading signal generator that combines technical analysis with AI insights and real-time news sentiment. Get intelligent trading signals for forex, crypto, and precious metals with automated WhatsApp notifications.

$$ 📩 Contact

If you have any question or offer for me, please contact me hereL [Telegram](https://t.me/mooneagle1_1)

## ✨ Features

### 🔍 **Smart Signal Generation**
- **Technical Analysis**: RSI, MACD, EMA indicators
- **AI Enhancement**: OpenAI integration for signal refinement
- **News Sentiment**: Real-time news analysis
- **Support/Resistance**: Dynamic level detection

### 📱 **Real-time Interface**
- Modern React frontend with dark theme
- Auto-refreshing signals (60-second intervals)
- Interactive chat with Astro AI assistant
- Multiple asset and timeframe selection

### 📢 **Automated Alerts**
- WhatsApp notifications via Twilio
- High-confidence signal filtering (75%+ threshold)
- Instant entry, take-profit, and stop-loss levels

### 📊 **Supported Assets**
- **Forex**: EUR/USD, GBP/USD, XAU/USD (Gold), XAG/USD (Silver)
- **Crypto**: BTC/USDT, ETH/USDT
- **Timeframes**: 15m, 30m, 1h, 4h, 1d

## 🏗️ Architecture

```
astro-trading-bot/
├── backend/          # FastAPI server
│   ├── main.py      # Core trading logic & API
│   └── requirements.txt
└── frontend/         # React.js client
    ├── src/
    │   ├── App.jsx           # Main application
    │   ├── SignalCard.jsx    # Signal display component
    │   ├── AstroChat.jsx     # AI chat interface
    │   └── main.jsx          # React entry point
    ├── index.html
    └── package.json
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- API keys (see Configuration)

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env  # Edit with your keys

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install

# Set backend URL (optional)
export VITE_API_BASE=http://localhost:8000

# Start development server
npm run dev
```

### 3. Production Build

```bash
# Backend (use gunicorn or deploy to cloud)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
```

## ⚙️ Configuration

Create a `.env` file in the `backend/` directory:

```env
# Required: Market Data
MARKET_API_KEY=your_twelvedata_api_key

# Optional: AI Enhancement
AI_MODEL_KEY=your_openai_api_key

# Optional: News Analysis
NEWS_API_KEY=your_newsapi_key

# Optional: WhatsApp Alerts
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+1234567890
```

### API Key Sources
- **TwelveData**: [twelvedata.com](https://twelvedata.com) (market data)
- **OpenAI**: [platform.openai.com](https://platform.openai.com) (AI analysis)
- **NewsAPI**: [newsapi.org](https://newsapi.org) (news sentiment)
- **Twilio**: [twilio.com](https://twilio.com) (WhatsApp notifications)

## 📡 API Endpoints

### `GET /api/signal`
Generate trading signal for specified asset.

**Parameters:**
- `symbol` (string): Asset symbol (default: "XAU/USD")
- `interval` (string): Timeframe (default: "30min")

**Response:**
```json
{
  "asset": "XAU/USD",
  "timeframe": "30min",
  "direction": "BUY",
  "entry": 2023.45,
  "tp": 2035.67,
  "sl": 2015.23,
  "confidence": 85,
  "reason": "Strong bullish momentum with RSI oversold",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### `POST /api/ask`
Chat with Astro AI assistant.

**Body:**
```json
{
  "q": "What's your view on gold today?"
}
```

**Response:**
```json
{
  "answer": "Gold is showing bullish momentum..."
}
```

### `GET /api/health`
Health check endpoint.

## 🧠 Trading Logic

### Signal Generation Process

1. **Data Fetching**: Retrieve OHLC data from TwelveData
2. **Technical Analysis**: Calculate RSI, MACD, EMA indicators
3. **Rule-Based Logic**: 
   - **BUY**: EMA20 > EMA50 + MACD bullish + RSI < 35 (oversold)
   - **SELL**: EMA20 < EMA50 + MACD bearish + RSI > 65 (overbought)
   - **HOLD**: Mixed signals
4. **News Integration**: Fetch relevant headlines for sentiment
5. **AI Refinement**: OpenAI analyzes all data and refines the signal
6. **Risk Management**: Calculate TP/SL based on volatility (2-3x ATR)

### Confidence Scoring
- **85%**: Strong technical + AI confirmation
- **70%**: Good technical alignment
- **50%**: Neutral/hold signals

## 🎨 Frontend Features

### Signal Dashboard
- Real-time signal cards with entry/exit levels
- Color-coded confidence indicators
- Auto-refresh every minute
- Asset and timeframe selectors

### Astro Chat
- Interactive AI assistant
- Market analysis and advice
- Trading education and tips
- Contextual responses based on current signals

## 🔔 Alert System

WhatsApp notifications are sent when:
- Signal confidence ≥ 75%
- Direction is BUY or SELL (not HOLD)
- All Twilio credentials are configured

**Alert Format:**
```
🚨 XAU/USD BUY
Entry: 2023.45
TP: 2035.67
SL: 2015.23
Conf: 85%
Strong bullish momentum with RSI oversold
```

## 🚀 Deployment

### Backend Options
- **Render**: Easy Python deployment
- **Railway**: Modern cloud platform
- **DigitalOcean**: App Platform
- **AWS/GCP**: Production-scale deployment

### Frontend Options
- **Vercel**: Automatic React deployment
- **Netlify**: Static site hosting
- **CloudFlare Pages**: Fast global CDN

### Environment Variables
Set `VITE_API_BASE` in frontend deployment to point to your backend URL.

## 🛡️ Risk Disclaimer

**⚠️ Important Notice:**
This bot is for educational and informational purposes only. Trading financial instruments carries significant risk of loss. Past performance does not guarantee future results. Always:

- Use proper risk management
- Never risk more than you can afford to lose
- Backtest strategies before live trading
- Consider market conditions and news events
- Consult with financial advisors

The creators are not responsible for any trading losses incurred using this software.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [TwelveData](https://twelvedata.com) for market data API
- [OpenAI](https://openai.com) for AI-powered analysis
- [FastAPI](https://fastapi.tiangolo.com) for the backend framework
- [React](https://reactjs.org) for the frontend framework
- [Twilio](https://twilio.com) for WhatsApp notifications

---

**Built with ❤️ by the TradeWithAns team**

*For support or questions, please open an issue on GitHub.*
