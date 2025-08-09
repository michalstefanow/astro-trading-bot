import React, { useEffect, useState } from "react";
import axios from "axios";
import SignalCard from "./SignalCard.jsx";
import AstroChat from "./AstroChat.jsx";

// set in Vercel: VITE_API_BASE = https://your-backend.onrender.com
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App(){
  const [symbol, setSymbol] = useState("XAU/USD");
  const [interval, setIntervalVal] = useState("30min");
  const [signal, setSignal] = useState(null);
  const [loading, setLoading] = useState(false);

  const getSignal = async () => {
    setLoading(true);
    try {
      const { data } = await axios.get(`${API_BASE}/api/signal`, { params: { symbol, interval } });
      setSignal(data);
    } catch (e) {
      console.error(e);
      alert("Signal request failed. Check backend URL / env.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getSignal();
    const id = setInterval(getSignal, 60000);
    return () => clearInterval(id);
  }, [symbol, interval]);

  return (
    <div style={{padding:18}}>
      <h1 style={{marginBottom:12}}>TradeWithAns — Signals</h1>
      <div style={{display:"flex",gap:10,flexWrap:"wrap",marginBottom:12}}>
        <select value={symbol} onChange={e=>setSymbol(e.target.value)}>
          <option>XAU/USD</option><option>XAG/USD</option>
          <option>BTC/USDT</option><option>ETH/USDT</option>
          <option>EUR/USD</option><option>GBP/USD</option>
        </select>
        <select value={interval} onChange={e=>setIntervalVal(e.target.value)}>
          <option value="15min">15m</option><option value="30min">30m</option>
          <option value="1h">1h</option><option value="4h">4h</option>
          <option value="1day">1d</option>
        </select>
        <button onClick={getSignal} disabled={loading}>{loading?"...":"Get Signal"}</button>
      </div>
      {signal ? <SignalCard data={signal}/> : <div>Loading signal...</div>}
      <div style={{marginTop:20}}><AstroChat apiBase={API_BASE}/></div>
    </div>
  );
}
