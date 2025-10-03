// frontend/src/components/Chat.tsx
import React, { useState, useEffect, useRef } from "react";
import api from "../services/api";

export default function Chat({ chatId }: { chatId: string }) {
  const [messages, setMessages] = useState<{role:string,content:string}[]>([]);
  const [input, setInput] = useState("");
  const [expiresAt, setExpiresAt] = useState<Date | null>(null);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    // fetch chat meta and messages
    async function init() {
      const r = await api.get(`/chat/${chatId}`);
      setExpiresAt(new Date(r.expires_at));
      setMessages(r.messages || []);
    }
    init();
  }, [chatId]);

  useEffect(() => {
    if (!expiresAt) return;
    const interval = setInterval(() => {
      const now = new Date();
      const diff = expiresAt.getTime() - now.getTime();
      if (diff <= 0) {
        alert("Chat expired");
        clearInterval(interval);
      } else if (diff <= 5 * 60 * 1000) {
        // less than 5 minutes left show popup
        // show non-blocking notice
        // one time shown logic omitted
        console.log("Chat will expire in less than 5 minutes");
      }
    }, 1000 * 30);
    return () => clearInterval(interval);
  }, [expiresAt]);

  async function send() {
    if (!input.trim()) return;
    setMessages(m=>[...m, {role:"user",content:input}]);
    setInput("");
    const res = await api.post(`/chat/${chatId}/message`, { role: "user", content: input });
    setMessages(m=>[...m, {role:"assistant", content: res.reply}]);
  }

  return (
    <div className="p-4">
      <div className="messages space-y-3">
        {messages.map((m,i)=> <div key={i} className={m.role==="user"?"text-right":"text-left"}>{m.content}</div>)}
      </div>
      <div className="mt-4 flex">
        <input value={input} onChange={e=>setInput(e.target.value)} className="flex-1 p-2 border" />
        <button onClick={send} className="ml-2 p-2 bg-blue-600 text-white">Send</button>
      </div>
    </div>
  );
}