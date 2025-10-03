# backend/app/image_adapter.py
"""
Pluggable image generation:
- can call AUTOMATIC1111 local WebUI API if installed
- or call remote API
"""
import os, requests

MODE = os.getenv("IMG_MODE", "api")  # api or local_webui

def gen_image_api(prompt: str) -> dict:
    key = os.getenv("STABLE_API_KEY")  # example
    if not key:
        raise RuntimeError("Image API key missing")
    url = "https://api.example-image.com/generate"
    r = requests.post(url, json={"prompt": prompt, "size": "1024x1024"}, headers={"Authorization": f"Bearer {key}"})
    r.raise_for_status()
    return r.json()

def gen_image_local(prompt: str) -> dict:
    # AUTOMATIC1111 API typical endpoint: http://127.0.0.1:7860/sdapi/v1/txt2img
    url = os.getenv("AUTOMATIC1111_URL", "http://127.0.0.1:7860/sdapi/v1/txt2img")
    r = requests.post(url, json={"prompt": prompt, "steps": 20})
    r.raise_for_status()
    return r.json()

def generate_image(prompt: str) -> dict:
    if MODE == "local_webui":
        return gen_image_local(prompt)
    return gen_image_api(prompt)