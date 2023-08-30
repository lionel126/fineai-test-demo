from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from fastapi_pagination import Page, add_pagination, paginate
from pydantic import BaseModel, Field

from fineai_test.services.app import get_images_by_job, compare_job_results, \
    get_model_jobs, get_model_lora, get_model_dataset_verify, \
    get_lora_result, get_models, get_model_face_detection, \
    get_model_img2img

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class UserModel(BaseModel):
    id: int = Field(example=100)
    user_id: int = Field(examples=1)


@app.get("/", response_model=UserModel)
async def root(request: Request):
    # s, stmt = await get_models_pagination()
    # return paginate(s, stmt)
    size = int(request.query_params.get('size', 200))
    page = int(request.query_params.get('page', 1))
    data = {
        'request': request,
        **await get_models(size, page)
    }
    return templates.TemplateResponse("index.html", data)


@app.get(path="/compare/{job_id1}/vs/{job_id2}", response_class=HTMLResponse)
async def compare_job(request: Request, job_id1, job_id2):
    # ?
    ret = await compare_job_results(job_id1, job_id2)
    data = {"request": request, "job_id1": job_id1, "job_id2": job_id2, **ret}
    return templates.TemplateResponse("vs.html", data)


@app.get(path="/job/{job_id}/images")
async def job_images(job_id):
    '''deprecated
    '''
    return await get_images_by_job(job_id)


@app.get(path="/model/{model_id}/jobs")
async def model(request: Request, model_id: int):
    ret = await get_model_jobs(model_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_jobs.html", data)


@app.get(path="/model/{model_id}/lora_train/{job_id}")
async def model_lora(request: Request, model_id: int, job_id):
    ret = await get_model_lora(model_id, job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_lora.html", data)


@app.get(path="/model/{model_id}/dataset_verify/{job_id}")
async def model_dataset_verify(request: Request, model_id: int, job_id=None):
    ret = await get_model_dataset_verify(model_id, job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_dataset_verify.html", data)


@app.get(path="/model/{model_id}/face_detection/{job_id}")
async def model_face_detection(request: Request, model_id: int, job_id=None):
    ret = await get_model_face_detection(model_id, job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_face_detection.html", data)


@app.get(path="/lora/{job_id}")
@app.get(path="/lora_train/{job_id}")
async def lora_images(request: Request, job_id: str):
    # deprecated
    ret = await get_lora_result(job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("lora.html", data)


@app.get(path="/model/{model_id}/img2img/{job_id}")
async def img2img(request: Request, model_id: int, job_id: str):
    ret = await get_model_img2img(model_id, job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_img2img.html", data)
