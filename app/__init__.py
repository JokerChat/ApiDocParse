# -*- coding: UTF-8 -*-

from fastapi import FastAPI
from app.routers.docs import docs
from app.routers.root import root
from starlette.middleware.cors import CORSMiddleware

#新建app
app = FastAPI()

#注册路由
app.include_router(docs.router, prefix="/api", tags=["接口文档导出工具"])
app.include_router(root.router)
#注册跨域
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


