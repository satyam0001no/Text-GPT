// frontend/src/components/VoiceControls.tsx
import React from "react";

export function VoiceControls({ onTranscribe }: { onTranscribe: (text:string)=>void }) {
  const startSTT = () => {
    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    if (!SpeechRecognition) return alert("SpeechRecognition not supported");
    const r = new SpeechRecognition();
    r.lang = "en-US";
    r.onresult = (ev:any) => {
      const text = ev.results[0][0].transcript;
      onTranscribe(text);
    };
    r.start();
  };

  const speak = (text:string) => {
    const s = new SpeechSynthesisUtterance(text);
    s.lang = "en-US";
    window.speechSynthesis.speak(s);
  };

  return (
    <div>
      <button onClick={startSTT}>Start Speech-to-Text</button>
      <button onClick={()=>speak("Hello from Text GPT!")}>Test TTS</button>
    </div>
  );
}