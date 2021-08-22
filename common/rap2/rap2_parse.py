# -*- coding: utf-8 -*-

import json
import requests
import random
from jsonsearch import JsonSearch
from jsonpath import jsonpath
from aip import AipOcr
from utils.FILE_PATH import DOWNLOAD_PATH
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from utils.config import UrlConfig,Account
import re

class Rap2Data(object):


    @classmethod
    def rap_login(cls):
        config = random.choice(Account.OCR)
        client = AipOcr(config['app_id'],config['api_key'],config['secret_key'])
        options = {}
        options["language_type"] = "ENG"
        options["detect_language"] = "true"
        img_res = requests.get(url = UrlConfig.RAP_CODE_URL)
        img_content = img_res.content
        #下载验证码图片
        with open(f"{DOWNLOAD_PATH}/code.svg", "wb") as f:
            f.write(img_content)
        # svg转jpg
        drawing = svg2rlg(f"{DOWNLOAD_PATH}/code.svg")
        #保存jpg图片
        renderPM.drawToFile(drawing, f"{DOWNLOAD_PATH}/code.jpg", fmt="JPG")
        with open(f"{DOWNLOAD_PATH}/code.jpg", 'rb') as img:
            #调用百度OCR SDK
            code_data = client.basicAccurate(img.read())
            code_list = code_data.get('words_result', [])
            if code_list:
                code_str = code_list[0]['words'].replace(" ", "")
                Account.RAP['captcha'] = code_str
                res = requests.post(url=UrlConfig.RAP_LOGIN_URL, json=Account.RAP, cookies=img_res.cookies)
                res_data = res.json()
                #验证是否登录成功，返回id即成功
                if res_data['data'].get('id', None):
                    cls.cookies = img_res.cookies
                    return True

    @classmethod
    def rap_data(cls, id, cookies = None):
        """
        获取接口文档数据
        :param id: 接口文档id
        :param cookies: 非必填，登录的cookies
        :return: 返回json数据
        """
        params = {"id": id}
        if cookies:
            try:
                cls.cookies = dict([i.split("=", 1) for i in cookies.split("; ")])
            except Exception as e:
                raise Exception('cookies格式不对,请重新输入!')
            try:
                res = requests.get(url=UrlConfig.RAP_PROJRCT_URL, params=params, cookies=cls.cookies).json()
            except Exception as e:
                raise Exception('cookies过期了,请重新输入!')
            return res
        else:
            login_result = False
            #判断是否登录成功
            while not login_result:
                login_result = Rap2Data.rap_login()
            res = requests.get(url=UrlConfig.RAP_PROJRCT_URL, params=params, cookies=cls.cookies).json()
            return res





class Rap2Parse(object):

    @classmethod
    def api_data(cls, id, cookies=None, module=None):
        json_obj = Rap2Data.rap_data(id, cookies)
        errMsg = json_obj.get("errMsg")
        #获取报错信息，将其抛出(权限不足、不存在接口文档，接口都会返回errMsg)
        if errMsg:
            errMsg = errMsg + f"请将接口文档授权给{Account.RAP['email']}!"
            raise Exception(errMsg)
        if module is None:
            #模块名不传的话，默认获取所有模块数据
            json_list = json_obj['data']['modules']
        else:
            #模块名传入，获取对应的模块数据
            json_list = jsonpath(json_obj, f"$.data.modules[?(@.name=='{module}')]")
            #校验传入的模块名是否存在
            if not json_list:
                raise Exception(f"{module}模块名不存在")
        # 接口文档标题名，作为后续的文件名
        file_name = json_obj.get('data').get('name')
        #对标题名特殊处理
        special_str = r"[\/\\\:\*\?\"\<\>\|]"
        file_name = re.sub(special_str, "-", file_name)
        data = []
        #遍历模块数据
        for i in json_list:
            modules_data = {}
            #模块名
            modules_data['modules'] = i['name']
            #模块描述
            modules_data['description'] = i['description']
            interfaces = []
            #遍历interfaces接口数据
            for i, dto in enumerate(i['interfaces']):
                cases_data = {}
                #接口id
                cases_data['api_id'] = i + 1
                #接口名
                cases_data['title'] = dto['name']
                #接口描述
                cases_data['description'] = dto['description']
                #接口路径
                cases_data['url'] = dto['url']
                #接口请求方法
                cases_data['method'] = dto['method']
                #获取接口的入参和出参
                properties_list = jsonpath(dto['properties'], f"$.[?(@.scope=='request')]")
                #接口请求头数据
                cases_data['headerData'] = cls.parent_data(properties_list)[2]
                #接口query参数
                cases_data['queryData'] = cls.parent_data(properties_list)[1]
                #接口body参数
                cases_data['data'] = cls.parent_data(properties_list)[0]
                interfaces.append(cases_data)
            modules_data['cases_data'] = interfaces
            data.append(modules_data)
        return data, file_name

    @classmethod
    def parent_data(cls, properties):
        """
        解析接口的入参和出参
        :param properties: 接口的入参和出参数据
        :return: body参数、query参数、header参数
        """
        json_data = {}
        query_data = {}
        header_data = {}
        if not properties:
            return json_data, query_data, header_data
        #获取所有的参数id
        api_id = jsonpath(properties, f"$..id")
        for index,dto in enumerate(properties):
            #body数据
            if dto['pos'] == 3:
                json_data = cls.join_data(json_data, properties, dto['name'], dto['type'], dto['value'], dto['parentId'],api_id)
            #query数据
            elif dto['pos'] == 2:
                query_data = cls.join_data(query_data, properties, dto['name'], dto['type'], dto['value'], dto['parentId'],api_id)
            #header数据
            elif dto['pos'] == 1:
                header_data = cls.join_data(header_data, properties, dto['name'], dto['type'], dto['value'], dto['parentId'],api_id)
            else:
                raise Exception("不支持的数据类型")
        return json_data, query_data, header_data

    @classmethod
    def join_data(cls, json_data, properties, name, type, value, parentId, api_id):
        """
        组装参数
        :param json_data: 字典值(存数据用)
        :param properties: 接口的入参和出参数据
        :param name: 接口名
        :param type: 字段类型
        :param value: 字段值
        :param parentId: 父id
        :param api_id: 所有的参数id
        :return: json_data
        """
        #特殊字符替换
        name = name.replace(".","")
        #没有父id,直接塞进json_data
        if parentId == -1:
            v = cls.change_value(type, value)
            json_data[name] = v
        #有父id且父id在api_id中
        elif parentId != -1 and parentId in api_id:
            #根据父id获取父id的数据
            parent_dto = jsonpath(properties, f"$.[?(@.id=={parentId})]")
            if not parent_dto:
                raise Exception("接口文档维护有误")
            parent_dto = parent_dto[0]
            #如果父的类型为数组
            if parent_dto['type'] == 'Array':
                #找到父的key
                parent_array = cls.search_value(json_data, parent_dto['name'])
                v = cls.change_value(type, value)
                #将子数据挂载在父下面
                parent_array[0][name] = v
            # 如果父的类型为对象
            elif parent_dto['type'] == 'Object':
                # 找到父的key
                parent_object = cls.search_value(json_data, parent_dto['name'])
                v = cls.change_value(type, value)
                # 将子数据挂载在父下面
                parent_object[name] = v
            else:
                raise Exception("父数据类型不支持")
        else:
            pass
            # raise Exception("父数据类型不支持")
        return json_data

    @classmethod
    def search_value(cls, data, key):
        """
        递归找到所在key的数据
        :param data: 数据
        :param key: 需要找的key
        :return:
        """
        key = key.replace(".", "")
        json_data = JsonSearch(object=data)
        path = json_data.search_first_path(key)
        path_str = cls.path_str(path)
        value = jsonpath(data, path_str)[0]
        return value


    @classmethod
    def change_value(cls, type, value):
        """
        根据类型，设置对应的值
        :param type:
        :param value:
        :return:
        """
        if type == 'String':
            v = value
        elif type == 'Number':
            try:
                v = int(value)
            except:
                v = value
        elif type == 'Boolean':
            if value.upper()=="TRUE":
                v = True
            elif value.upper()=="FALSE":
                v = False
            else:
                v = value
        elif type == 'Object':
            v = {}
        elif type == 'Array':
            v = [{}]
        else:
            raise Exception("不支持的类型")
        return v

    @classmethod
    def path_str(cls, path):
        """
        转化为jsonpaht语法
        :param path: 路径数据
        :return:
        """
        path_str = ""
        for i in path:
            if isinstance(i, int):
                path_str += f"[{i}]"
            else:
                path_str += f".{i}"
        return f"${path_str}"



if __name__ == '__main__':
    cookies = "Hm_lvt_ed752fa41bdfde359bfde28ccd27b888=1628211014; koa.sid=kDRbweS1aW_zluRWrvpVbOKpG9GG_IMb; koa.sid.sig=yz2w5nbNYoZi8Ymyv9F13jPqz2s"
    result, file_name = Rap2Parse.api_data(407,cookies)
    print(json.dumps(result,ensure_ascii=False))


