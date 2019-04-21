import datetime
import re
import time

from django.test import TestCase

# Create your tests here.
import xlrd

# workbook = xlrd.open_workbook('D:\\stu_info.xlsx')
# data_sheet = workbook.sheets()[0]
# row_num = data_sheet.nrows
# col_num = data_sheet.ncols
#
# data = []
# # 拿到所有数据
# for i in range(row_num):
#     row_list = []
#     for j in range(col_num):
#         row_list.append(data_sheet.cell_value(i, j))
#     data.append(row_list)
#     print(row_list)
# result_data = []
# for d in data[1:]:
#     data_dict = {}
#     for i in range(len(data[0])):
#         data_dict[re.findall(r'\((.*?)\)', data[0][i])[0]] = d[i]
#         # data_dict[data[0][i].split('(')[1].split(')')[0]] = d[i]
#     result_data.append(data_dict)

print(datetime.timezone.)