from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from fastapi_pagination import Page, add_pagination, paginate
from pydantic import BaseModel, ConfigDict
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from fineai_test.db import get_db
from fineai_test.services.app import get_images_by_job, compare_job_results, \
    get_model_jobs, get_model_lora, get_model_dataset_verify, \
    get_lora_result, get_models, get_model_face_detection, \
    get_model_img2img, get_outputs, get_jobs
from fineai_test.services import mq
from fineai_test import trial

app = FastAPI()
add_pagination(app)
app.include_router(trial.router)
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# class UserModel(BaseModel):
#     id: int = Field(example=100)
#     user_id: int = Field(examples=1)


class JobReq(BaseModel):
    id: str | None = None
    user_model_id: int | None = None
    job_kind: str | None = None
    is_delete: bool | None = None
    status: str | None = None

    size: int | None = 50
    page: int | None = 1


class ModelReq(BaseModel):
    id: int | None = None
    user_id: int | None = None
    model_name: str | None = None
    gender: int | None = None
    status: str | None = None
    pay_status: str | None = None
    order_no: str | None = None
    image_id: int | None = None

    size: int | None = 50
    page: int | None = 1

    model_config = ConfigDict(
        protected_namespaces=()
    )


class OutputReq(BaseModel):
    id: str | None = None
    user_model_id: int | None = None
    image_type: str | None = None
    show_name: str | None = None
    status: str | None = None
    is_delete: bool | None = None

    size: int | None = 50
    page: int | None = 1

class Job(BaseModel):
    job_id: str
    job_kind: str
class MqReq(BaseModel):
    jobs : list[Job]
    type : str | None = None


@app.get("/")
async def root(request: Request):
    data = {"request": request}
    return templates.TemplateResponse("index.html", data)


@app.get("/models")
async def models(request: Request, req: ModelReq = Depends(), db: AsyncSession = Depends(get_db)):
    data = {
        'request': request,
        **await get_models(db, **req.model_dump())
    }
    return templates.TemplateResponse("models.html", data)


@app.get(path="/compare/{job_id1}/vs/{job_id2}", response_class=HTMLResponse)
async def compare_job(request: Request, job_id1, job_id2, db: AsyncSession = Depends(get_db)):
    # deprecated ?
    ret = await compare_job_results(db, job_id1, job_id2)
    data = {"request": request, "job_id1": job_id1, "job_id2": job_id2, **ret}
    return templates.TemplateResponse("vs.html", data)


@app.get(path="/job/{job_id}/images")
async def job_images(job_id, db: AsyncSession = Depends(get_db)):
    '''deprecated
    '''
    return await get_images_by_job(db, job_id)


@app.get(path="/model/{model_id}/jobs")
async def model(request: Request, model_id: int, db: AsyncSession = Depends(get_db)):
    ret = await get_model_jobs(db, model_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_jobs.html", data)


@app.get(path="/model/{model_id}/lora_train/{job_id}")
async def model_lora(request: Request, model_id: int, job_id, db: AsyncSession = Depends(get_db)):
    ret = await get_model_lora(db, model_id, job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_lora.html", data)


@app.get(path="/model/{model_id}/dataset_verify/{job_id}")
async def model_dataset_verify(request: Request, model_id: int, job_id=None, db: AsyncSession = Depends(get_db)):
    ret = await get_model_dataset_verify(db, model_id, job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_dataset_verify.html", data)


@app.get(path="/model/{model_id}/face_detection/{job_id}")
async def model_face_detection(request: Request, model_id: int, job_id=None, db: AsyncSession = Depends(get_db)):
    ret = await get_model_face_detection(db, model_id, job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_face_detection.html", data)


@app.get(path="/lora/{job_id}")
@app.get(path="/lora_train/{job_id}")
async def lora_images(request: Request, job_id: str, db: AsyncSession = Depends(get_db)):
    # deprecated
    ret = await get_lora_result(db, job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("lora.html", data)


@app.get(path="/model/{model_id}/img2img/{job_id}")
async def img2img(request: Request, model_id: int, job_id: str, db: AsyncSession = Depends(get_db)):
    ret = await get_model_img2img(db, model_id, job_id)
    data = {"request": request, **ret}
    return templates.TemplateResponse("model_img2img.html", data)


@app.get(path='/outputs')
async def outputs(request: Request, req: OutputReq = Depends(), db: AsyncSession = Depends(get_db)):

    ret = await get_outputs(db, **req.model_dump())
    data = {"request": request, **ret}
    return templates.TemplateResponse("outputs.html", data)


@app.get(path='/jobs')
async def jobs(request: Request, req: JobReq = Depends(), db: AsyncSession = Depends(get_db)):

    ret = await get_jobs(db, **req.model_dump())
    data = {"request": request, **ret}
    return templates.TemplateResponse("jobs.html", data)


@app.post(path='/mq/consume')
async def consume_mq(req: MqReq):
    kw = req.model_dump()
    if 'type' in kw and kw['type'] in ('force', 'suspend'):
        ret = mq.fail(**kw)
    else:
        ret = mq.consume(**kw)
    return ret
