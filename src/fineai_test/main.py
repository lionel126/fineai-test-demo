from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fineai_test.services.app import get_images_by_job, compare_job_results, get_images_by_model

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(path="/compare/{job_id1}/vs/{job_id2}", response_class=HTMLResponse)
async def compare_job(request:Request, job_id1, job_id2):
    ret = await compare_job_results(job_id1, job_id2)
    data = {"request": request, "job_id1": job_id1, "job_id2": job_id2, **ret}
    return templates.TemplateResponse("vs.html", data)

@app.get(path="/job/{job_id}/images")
async def job_images(job_id):
    return await get_images_by_job(job_id)

@app.get(path="/model/{model_id}/images")
async def model_images(request:Request, model_id:int):
    ret = await get_images_by_model(model_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_images.html", data)
