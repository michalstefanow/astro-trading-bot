import React, { useState } from "react";
import axios from "axios";

export default function AstroChat({ apiBase }){
  const [msgs, setMsgs] = useState([{from:"astro",text:"yo, I'm Astro. Ask me about markets or your signal."}]);
  const [inp, setInp] = useState("");

  const send = async ()=>{
    if(!inp) return;
    setMsgs(m=>[...m,{from:"you",text:inp}]);
    try{
      const {data} = await axios.post(`${apiBase}/api/ask`, { q: inp });
      setMsgs(m=>[...m,{from:"astro",text:data.answer||"..." }]);
    }catch{
      setMsgs(m=>[...m,{from:"astro",text:"can't reach the server rn"}]);
    }finally{
      setInp("");
    }
  };

  return(
    <div style={{maxWidth:560}}>
      <div style={{background:"#0e0e0e",padding:10,borderRadius:8,minHeight:140}}>
        {msgs.map((m,i)=>(
          <div key={i} style={{textAlign:m.from==="you"?"right":"left",margin:"6px 0"}}>
            <span style={{display:"inline-block",background:m.from==="you"?"#a3d3ff":"#222",color:m.from==="you"?"#000":"#fff",padding:"8px 10px",borderRadius:6}}>
              {m.text}
            </span>
          </div>
        ))}
      </div>
      <div style={{display:"flex",gap:6,marginTop:8}}>
        <input value={inp} onChange={e=>setInp(e.target.value)} placeholder="Ask Astro..." style={{flex:1,padding:8}}/>
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}
