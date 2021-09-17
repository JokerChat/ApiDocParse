# -*- coding: UTF-8 -*-


import uuid
from utils.FILE_PATH import DOWNLOAD_PATH
from common.create_jmx import CreateJmx

class ToJmx(object):

    @classmethod
    def to_jmx(cls, name, data):
        jmeter_xml = CreateJmx.conversion(data, name)
        file_name = f"{name}-{uuid.uuid4().hex}.jmx"
        try:
            jmeter_xml.write(f'{DOWNLOAD_PATH}/{file_name}', pretty_print=True, xml_declaration=True,
                             encoding='utf-8')
        except Exception as e:
            err = "rap2转换jmx失败："+str(e)
            raise Exception(err)
        return file_name

if __name__ == '__main__':
    result = ToJmx.to_jmx(407,{})
    print(result)
