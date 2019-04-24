# -*- coding: UTF-8 -*-
import pandas as pd
from matplotlib import rcParams
font_name = 'FZZJ-ZJJYBKTJW'
rcParams['font.sans-serif'] = [font_name]
rcParams['font.family'] = 'sans-serif'
from matplotlib import pyplot as plt

def draw():

    df = pd.read_csv("sale_change.csv")

    df["环比变化幅度"] = (df["环比上涨数"]*df["环比涨幅"]+df["环比下跌"]*df["环比跌幅"])/285
    df["同比变化幅度"] = (df["同比上涨数"]*df["同比涨幅"]+df["同比下跌"]*df["同比跌幅"])/285

    # 两个折线图
    fig, ax = plt.subplots()
    ax.plot(df["日期"].values, df["环比上涨数"].values, label="环比上涨数")
    ax.plot(df["日期"].values, df["同比上涨数"].values, label="同比上涨数")
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax.set(ylim=[50,300], xlabel='', ylabel='城市数', title='近六个月住宅均价上涨城市数')
    ax.legend()
    fig.savefig('r_city_num.png', transparent=False, dpi=80, bbox_inches="tight")


    fig2, ax2 = plt.subplots()
    ax2.plot(df["日期"].values, df["环比变化幅度"].values, label="环比涨幅")
    ax2.plot(df["日期"].values, df["同比变化幅度"].values, label="同比涨幅")
    labels = ax2.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax2.axhline(0, ls='--', color='r', linewidth=1.5)
    ax2.set(ylim=[-0.06, 0.2], xlabel='', ylabel='涨幅', title='近六个月住宅均价涨幅')
    ax2.legend()
    fig2.savefig('r_city_up.png', transparent=False, dpi=80, bbox_inches="tight")

    # 两个饼形图
    labels = "上涨", "下跌"
    sizes = [df.iat[-1, 3], df.iat[-1, 7]]
    explode = (0, 0.1)

    fig3, ax3 = plt.subplots()
    wedges, texts, autotexts = ax3.pie(sizes, labels=labels, autopct='%1.2f%%', explode=explode, shadow=True, startangle=90)
    plt.setp(autotexts, size=20)
    plt.setp(texts, size=16)
    ax3.axis('equal')
    ax3.set_title("19年2月百城住宅环比涨跌对比")
    fig3.savefig('r_pie1.png', transparent=False, dpi=80, bbox_inches="tight")

    sizes = [df.iat[-1, 1],df.iat[-1, 5]]

    fig4, ax4 = plt.subplots()
    wedges2, texts2, autotexts2 = ax4.pie(sizes, labels=labels, autopct='%1.2f%%', explode=explode, shadow=True,
                                       startangle=90)
    plt.setp(autotexts2, size=20)
    plt.setp(texts, size=16)
    ax4.axis('equal')
    ax4.set_title("19年2月百城住宅同比涨跌对比")
    fig4.savefig('r_pie2.png', transparent=False, dpi=80, bbox_inches="tight")




























































