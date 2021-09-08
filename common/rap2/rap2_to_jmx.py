# -*- coding: UTF-8 -*-


import uuid
from utils.FILE_PATH import DOWNLOAD_PATH
from common.rap2.rap2_parse import Rap2Parse
from common.to_jmx import CreateJmx

class Rap2ToJmx(object):

    @classmethod
    def to_jmx(cls, id,  cookies=None, module=None):
        rap2_data, name = Rap2Parse.api_data(id, cookies, module)
        jmeter_xml = CreateJmx.conversion(rap2_data, name)
        file_name = f"{name}-{uuid.uuid4().hex}.jmx"
        try:
            jmeter_xml.write(f'{DOWNLOAD_PATH}/{file_name}', pretty_print=True, xml_declaration=True,
                             encoding='utf-8')
        except Exception as e:
            err = "rap2转换jmx失败："+str(e)
            raise Exception(err)
        return file_name

if __name__ == '__main__':
    result = Rap2ToJmx.to_jmx(407)
    print(result)
