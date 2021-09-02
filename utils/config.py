# -*- coding: UTF-8 -*-




class DoMain(object):
    """域名配置"""
    RAP = 'RAP'

class UrlConfig(DoMain):
    """Url配置"""
    RAP_CODE_URL = DoMain.RAP + '/captcha?t=1626914290792'
    RAP_LOGIN_URL = DoMain.RAP + '/account/login'
    RAP_PROJRCT_URL = DoMain.RAP + '/repository/get'


class Account(object):
    RAP = {
    "email": "email",
    "password": "password"
  }
    OCR = [
        {
            "app_id": "app_id",
            "api_key": "api_key",
            "secret_key": "secret_key"
        }
    ]


