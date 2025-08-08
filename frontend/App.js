import React, { useEffect, useState } from "react";
import AstroBot from "./AstroBot";

export default function App() {
    const [signal, setSignal] = useState(null);

    useEffect(() => {
        fetch("/signal")
            .then(res => res.json())
            .then(data => setSignal(data));
    }, []);

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold mb-4">AI Trading Signal</h1>
            {signal && (
                <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
                    <p>Pair: {signal.pair}</p>
                    <p>Direction: {signal.direction}</p>
                    <p>Confidence: {signal.confidence}</p>
                    <p>TP: {signal.tp}</p>
                    <p>SL: {signal.sl}</p>
                    <p>Note: {signal.explanation}</p>
                </div>
            )}
            <AstroBot />
        </div>
    );
}