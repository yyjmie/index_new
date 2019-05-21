import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

this_month = '2019/04'
df1 = pd.read_csv('mid_sale.csv',usecols=['city','num',this_month],na_values='na')
df2 = pd.read_csv('province_city.csv')
df = pd.merge(df1,df2,on='city')

df['total_sale'] = df.num * df[this_month]

df_province = df.groupby('province', as_index=False).sum()
df_province['average'] = df_province['total_sale']/df_province['num']

def map_visualmap() -> Map:
    c = (
        Map()
        .add('住宅价格', df_province.loc[:, ['province','average']].values, "china",is_map_symbol_show=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国房价一览"),
            visualmap_opts=opts.VisualMapOpts(min_=5000,max_=65000,is_piecewise=True,
            	pieces=[{'min':5000, 'max':10000},{'min':10000, 'max':15000},{'min':15000, 'max':20000},
            	{'min':20000, 'max':25000},{'min':25000, 'max':30000},{'min':30000, 'max':35000},{'min':35000}]),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    return c

map = map_visualmap()
make_snapshot(snapshot, map.render(), "map.png")
