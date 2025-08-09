import React from "react";
export default function SignalCard({ data }){
  return (
    <div style={{background:"#111",padding:14,borderRadius:8,maxWidth:560}}>
      <h2>{data.asset} — {data.direction}</h2>
      <p><b>Entry:</b> {data.entry}</p>
      <p><b>TP:</b> {data.tp} &nbsp; <b>SL:</b> {data.sl}</p>
      <p><b>Confidence:</b> {data.confidence}%</p>
      <p style={{opacity:.85}}>{data.reason}</p>
      <p style={{fontSize:12,opacity:.6}}>{data.timestamp}</p>
    </div>
  );
}
