// frontend/src/services/api.ts
const base = import.meta.env.VITE_API_BASE || "http://localhost:8000";
export default {
  get: (path:string) => fetch(base + path).then(r=>r.json()),
  post: (path:string, data:any) => fetch(base + path, {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(data)}).then(r=>r.json()),
};