# -*- coding: UTF-8 -*-

from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="static")

@router.get('/',include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})
