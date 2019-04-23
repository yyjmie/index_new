# -*- coding: UTF-8 -*-
import pandas as pd

import data_analyse as d
import draw

# 设置需要的列
last_month = '2019/1/1'
same_month = '2018/2/1'
this_month = '2019/2/1'
file_name_sale = "data_2019_02_sale.csv"
file_name_rent = "data_2019_02_rent.csv"
last_month_index = 438.16
same_month_index = 340.18

# 处理城市名,去掉"市"字,以与大表按城市名合并
d.city_name_preprocess(file_name_sale, "sale.csv", this_month)
d.city_name_preprocess(file_name_rent, "rent.csv", this_month)

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