# -*- coding: UTF-8 -*-
import pandas as pd

import json_to_csv as j
import data_analyse as d
import draw
import arrow

# 
file_name_sale = "data_2019_04_sale.json"
file_name_rent = "data_2019_04_rent.json"

y_m = arrow.get(file_name_sale, 'YYYY_MM')
this_month = y_m.format('YYYY/MM')
last_month = y_m.shift(months=-1).format('YYYY/MM')
same_month = y_m.shift(years=-1).format('YYYY/MM')


last_month_index = 424.23
same_month_index = 344.82

#
j.json_to_csv(file_name_sale, "mid_sale.csv", this_month)
j.json_to_csv(file_name_rent, "mid_rent.csv", this_month)
j.preprocess("mid_sale.csv", "sale.csv", this_month)
j.preprocess("mid_rent.csv", "rent.csv", this_month)

# 新sale表合并过来并保存
d.save_table("286sale.csv", "sale.csv", this_month)

# 计算286sale同比和环比
d.sale_calculate(last_month, same_month, this_month)

# 计算百城投资收益指数
d.index_calculate(last_month, same_month, this_month, last_month_index, same_month_index)

# 新index表合并过来保存
d.save_table('286index.csv', 'index_new.csv', this_month)

# 绘图
draw.draw()
