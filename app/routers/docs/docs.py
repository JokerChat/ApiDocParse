# -*- coding: UTF-8 -*-

from fastapi import APIRouter
from app.routers.docs.docs_schemas import Rap2Body
from common.to_excel import CreateCases
from common.to_yaml import ToYaml
from common.to_jmx import ToJmx
from common.rap2_parse import Rap2Parse
from utils.FILE_PATH import DOWNLOAD_PATH
from utils.config import UrlConfig
from starlette.responses import FileResponse
import os

router = APIRouter()

@router.post('/rap2/export', name='接口文档数据导出')
async def export(body: Rap2Body):
    type = body.type
    project_id = body.projectId
    module_name = body.moduleName
    cookies = body.cookies
    try:
        data, name= Rap2Parse.api_data(project_id, cookies, module_name)
        if type == 1:
            create_excel = CreateCases(name)
            file_name = create_excel.create_file(data)
        elif type == 2:
            file_name = ToYaml.to_yaml(name, data)
        else:
            file_name = ToJmx.to_jmx(name, data)
        url = UrlConfig.DOWNLOAD_URL + file_name
        return dict(code=0, msg='请求成功',data=url)
    except Exception as e:
        return dict(code=500, msg='请求失败',data=str(e))



@router.get("/download/{file_name}",include_in_schema=False)
async def downlaod(file_name: str):
    try:
        file_path = os.path.join(DOWNLOAD_PATH, file_name)  # 文件路径
        return FileResponse(file_path, filename=file_name)
    except Exception as e:
        err = "文件下载报错" + str(e)
        return dict(code=500, msg='请求失败',data=err)