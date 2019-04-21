import http
import json
import logging
import random
import re
from datetime import datetime
from urllib.error import URLError
from urllib.parse import urlencode

import xlrd

SMS_SERVER = '106.ihuyi.com'
SMS_URL = '/webservice/sms.php?method=Submit'
SMS_ACCOUNT = 'C91532636'
SMS_PASSWORD = '3c2ff35a24a587022f899e3c3190d3f5'
MSG_TEMPLATE = '您的验证码是：%s。请不要把验证码泄露给其他人。'


def get_order_sn():
    """
    生成随机的订单号
    """
    sn = ''
    s='1234567890qwertyuiopasdfghjklzxcvbnm'
    for i in range(10):
        sn += random.choice(s)
    sn += datetime.now().strftime('%Y%m%d%H%M%S')
    return sn


def get_code(length=4):
    """
    生成随机验证码
    :param length: 长度
    :return: 验证码结果
    """
    string = '0123456789'
    code = ''
    for _ in range(length):
        code += random.choice(string)
    return code


def send_short_message(tel, code):
    """发送短信"""
    params = urlencode({
        'account': SMS_ACCOUNT,
        'password': SMS_PASSWORD,
        'content': MSG_TEMPLATE % code,
        'mobile': tel,
        'format': 'json'
    })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    conn = http.client.HTTPConnection(SMS_SERVER, port=80, timeout=10)
    try:
        conn.request('POST', SMS_URL, params, headers)
        json_str = conn.getresponse().read().decode('utf-8')
        return json.loads(json_str)
    except URLError or KeyError as e:
        logging.error(e)
        return json.dumps({
            'code': 500,
            'msg': '短信服务暂时无法使用'
        })
    finally:
        conn.close()


def check_phone_number(number):
    restring = "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\\d{8}$"
    if re.fullmatch(restring, number):
        return True
    return False


def check_email(mail):
    restring = r'^[0-9a-z][_.0-9a-z-]{0,31}@([0-9a-z][0-9a-z-]{0,30}[0-9a-z]\.){1,4}[a-z]{2,4}$'
    if re.fullmatch(restring, mail):
        return True
    return False


def excel_to_stu(file_path):
    workbook = xlrd.open_workbook(file_path)
    data_sheet = workbook.sheets()[0]
    row_num = data_sheet.nrows
    col_num = data_sheet.ncols

    data = []
    # 拿到所有数据
    for i in range(row_num):
        row_list = []
        for j in range(col_num):
            row_list.append(data_sheet.cell_value(i, j))
        data.append(row_list)
    result_data = []
    for d in data[1:]:
        data_dict = {}
        for i in range(len(data[0])):
            data_dict[re.findall(r'\((.*?)\)', data[0][i])[0]] = d[i]
            # data_dict[data[0][i].split('(')[1].split(')')[0]] = d[i]
        result_data.append(data_dict)
    return result_data


def get_rand_str(length, upper=False, add_str=''):
    string = '1234567890qwertyuiopasdfghjklzxcvbnm' + add_str
    result = ''
    for i in range(length):
        result += random.choice(string)
    if upper:
        return result.upper()
    return result


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|\{\}\[\]\(\)]"  # '/ \ : * ? " < > | { } [ ]'
    new_title = re.sub(rstr, "", title)  # 替换为下划线
    return new_title