from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer Your API Token"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def summarize(request: Request, text: str = Form(...), min_length: int = Form(...), max_length: int = Form(...)):
    output = query({"inputs": text, "parameters": {"min_length": min_length, "max_length": max_length}})
    summary = output[0]["summary_text"] if output else "An error occurred."
    return templates.TemplateResponse("form.html", {"request": request, "text": text, "summary": summary, "min_length": min_length, "max_length": max_length})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
