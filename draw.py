# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
# zhongwenziti
from matplotlib import rcParams
font_name = 'FZXiHeiI-Z08S'
rcParams['font.sans-serif'] = [font_name]
rcParams['font.family'] = 'sans-serif'
from matplotlib import pyplot as plt
# pyechart
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


plt.style.use('fivethirtyeight')

def map_visualmap(df_province) -> Map:
    c = (
        Map()
        .add('住宅价格', df_province.values, "china",is_map_symbol_show=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国房价一览"),
            visualmap_opts=opts.VisualMapOpts(min_=5000,max_=65000,is_piecewise=True,
                pieces=[{'min':5000, 'max':10000},{'min':10000, 'max':15000},{'min':15000, 'max':20000},
                {'min':20000, 'max':25000},{'min':25000, 'max':30000},{'min':30000, 'max':35000},{'min':35000}]),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    return c


def pie(this_month):

    df = pd.read_csv("sale_change.csv")

    labels = "上涨", "下跌"
    sizes = [df.iat[-1, 3], df.iat[-1, 7]]
    explode = (0, 0.1)

    fig3, ax3 = plt.subplots()
    wedges, texts, autotexts = ax3.pie(sizes, labels=labels, autopct='%1.2f%%', explode=explode, shadow=True, startangle=90)
    plt.setp(autotexts, size=20)
    plt.setp(texts, size=16)
    ax3.axis('equal')
    ax3.set_title(this_month+"百城住宅环比涨跌对比")
    fig3.savefig('r_pie1.png', transparent=False, dpi=80, bbox_inches="tight")

    sizes = [df.iat[-1, 1],df.iat[-1, 5]]

    fig4, ax4 = plt.subplots()
    wedges2, texts2, autotexts2 = ax4.pie(sizes, labels=labels, autopct='%1.2f%%', explode=explode, shadow=True,
                                       startangle=90)
    plt.setp(autotexts2, size=20)
    plt.setp(texts, size=16)
    ax4.axis('equal')
    ax4.set_title(this_month+"百城住宅同比涨跌对比")
    fig4.savefig('r_pie2.png', transparent=False, dpi=80, bbox_inches="tight")


def line():

    df = pd.read_csv("sale_change.csv")

    df["环比变化幅度"] = (df["环比上涨数"]*df["环比涨幅"]+df["环比下跌"]*df["环比跌幅"])/285
    df["同比变化幅度"] = (df["同比上涨数"]*df["同比涨幅"]+df["同比下跌"]*df["同比跌幅"])/285

    fig, ax = plt.subplots()
    ax.plot(df["日期"].values[-6:], df["环比上涨数"].values[-6:], label="环比上涨数")
    ax.plot(df["日期"].values[-6:], df["同比上涨数"].values[-6:], label="同比上涨数")
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax.set(ylim=[50,300], xlabel='', ylabel='城市数', title='近半年住宅均价上涨城市数')
    ax.legend()
    fig.savefig('r_city_num.png', transparent=False, dpi=80, bbox_inches="tight")


    fig2, ax2 = plt.subplots()
    ax2.plot(df["日期"].values[-6:], df["环比变化幅度"].values[-6:], label="环比涨幅")
    ax2.plot(df["日期"].values[-6:], df["同比变化幅度"].values[-6:], label="同比涨幅")
    labels = ax2.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax2.axhline(0, ls='--', color='r', linewidth=1.5)
    ax2.set(ylim=[-0.06, 0.2], xlabel='', ylabel='涨幅', title='近半年住宅均价涨幅')
    ax2.legend()
    fig2.savefig('r_city_up.png', transparent=False, dpi=80, bbox_inches="tight")

def bar():
    
    df = pd.read_csv("rate_new.csv")

    rate_mean = np.mean(df['y_on_y'])

    first_tier = df[df['city'].isin(['北京', '上海', '广州', '深圳'])]
    new_first_tier = df[df['city'].isin(['成都', '杭州', '重庆', '武汉', '苏州', '西安',
                                                 '天津', '南京', '郑州', '长沙', '沈阳', '青岛',
                                                 '宁波', '东莞', '无锡'])]

    fig, ax = plt.subplots()
    ax.bar(new_first_tier['city'].values, new_first_tier['y_on_y'].values)
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax.axhline(rate_mean, ls='--', color='r')
    ax.text(9, rate_mean+0.05, '285城收益率均值')
    ax.set(ylim=[-0.1, 1], xlabel='', ylabel='投资收益率', title='新一线城市投资收益率')
    fig.savefig('new_first_tier.png', transparent=False, dpi=80, bbox_inches="tight")

    fig2, ax2 = plt.subplots()
    ax2.bar(first_tier['city'].values, first_tier['y_on_y'].values)
    labels = ax2.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax2.axhline(rate_mean, ls='--', color='r')
    ax2.text(2, rate_mean + 0.05, '285城收益率均值')
    ax2.set(ylim=[-0.1, 1], xlabel='', ylabel='投资收益率', title='一线城市投资收益率')
    fig2.savefig('first_tier.png', transparent=False, dpi=80, bbox_inches="tight")

def map(this_month):

    this_month = '2019/04'
    df1 = pd.read_csv('mid_sale.csv',usecols=['city','num',this_month],na_values='na')
    df2 = pd.read_csv('province_city.csv')
    df = pd.merge(df1,df2,on='city')

    df['total_sale'] = df.num * df[this_month]

    df_province = df.groupby('province', as_index=False).sum()
    df_province['average'] = df_province['total_sale']/df_province['num']
    df_province = df_province.loc[:, ['province','average']]

    map = map_visualmap(df_province)
    make_snapshot(snapshot, map.render(), "map.png")





















































