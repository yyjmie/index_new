# -*- coding: UTF-8 -*-
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def save_table(old_file, new_file, this_month):
    # 新数据与原表合并
    df = pd.read_csv(old_file)

    if this_month not in df.columns:
        df2 = pd.read_csv(new_file)
        result = pd.merge(df ,df2, on='city')
        result.to_csv(old_file, index=False)

def city_name_preprocess(file_name, to_file_name, this_month):
    data = pd.read_csv(file_name)
    data.rename(columns={"城市": "city", "均价": this_month}, inplace=True)

    for i in range(len(data)):
        if data.iat[i,0][-1] == '市':
            data.iat[i,0] = data.iat[i,0][0:-1]

    data.to_csv(to_file_name, index=False)

def sale_calculate(last_month, same_month, this_month):
    # 新数据与原表合并
    df = pd.read_csv('286sale.csv', usecols=['city', same_month, last_month])
    df2 = pd.read_csv('sale.csv')

    result = pd.merge(df ,df2, on='city')

    # 计算同比和环比
    result['y_on_y'] = (result[this_month]-result[same_month]) / result[same_month]
    result['m_on_m'] = (result[this_month]-result[last_month]) / result[last_month]

    # 得到同比和环比上涨数量和涨幅
    result_y_up = result[result.y_on_y>=0]['y_on_y']
    result_m_up = result[result.m_on_m>=0]['m_on_m']
    y_on_y_up_num = len(result_y_up)
    m_on_m_up_num = len(result_m_up)
    y_on_y_up_rate = result_y_up.mean()
    m_on_m_up_rate = result_m_up.mean()
    print("同比上涨数量: " + str(y_on_y_up_num))
    print("环比上涨数量: " + str(m_on_m_up_num))

    print("同比平均涨幅:" + str(y_on_y_up_rate))
    print("环比平均涨幅:" + str(m_on_m_up_rate))


    result_y_down = result[result.y_on_y<0]['y_on_y']
    result_m_down = result[result.m_on_m<0]['m_on_m']
    y_on_y_down_num = len(result_y_down)
    m_on_m_down_num = len(result_m_down)
    y_on_y_down_rate = result_y_down.mean()
    m_on_m_down_rate = result_m_down.mean()
    print("同比下降数量: " + str(y_on_y_down_num))
    print("环比下降数量: " + str(m_on_m_down_num))

    print("同比平均降幅:" + str(y_on_y_down_rate))
    print("环比平均降幅:" + str(m_on_m_down_rate))

    # 保存
    o = pd.read_csv("sale_change.csv")
    if(o.iat[-1, 0]!=this_month):
        s = pd.DataFrame({"日期": this_month,
                        "环比上涨数": m_on_m_up_num,
                        "环比涨幅": m_on_m_up_rate,
                        "同比上涨数": y_on_y_up_num,
                        "同比涨幅": y_on_y_up_rate,
                        "环比下跌": m_on_m_down_num,
                        "环比跌幅": m_on_m_down_rate,
                        "同比下跌": y_on_y_down_num,
                        "同比跌幅": y_on_y_down_rate},
                        index=[0])

        o = o.append(s, ignore_index=True)
        o.to_csv("sale_change.csv", index=False)

# 计算投资收益指数
def index_calculate(last_month, same_month, this_month, last_month_index, same_month_index):
    # 指数表
    df = pd.read_csv("286index.csv", usecols=['city', last_month,same_month])

    # 房价表
    df2 = pd.read_csv("286sale.csv", usecols=['city', last_month, this_month])
    df2.rename(columns={this_month: "sale"+this_month, last_month: "sale"+last_month}, inplace=True)

    # 租金表
    df3 = pd.read_csv("rent.csv")
    df3.rename(columns={this_month: "rent"}, inplace=True)

    # 合并
    merged = pd.merge(df, df2, on='city')
    result = pd.merge(merged, df3, on='city')

    # 计算
    result[this_month] = ((result['sale'+this_month]+result['rent'])/result['sale'+last_month])*result[last_month]

    # 保存
    result.to_csv("index_new.csv", columns=['city', this_month], index=False)

    # 舍弃不需要的列
    result = result.loc[:, ['city', same_month, last_month, this_month]]

    # 计算年投资收益率的前十后十
    result['y_on_y'] = result[this_month]/result[same_month]-1
    sorted = result.loc[:, ['city', 'y_on_y']].sort_values(by='y_on_y', ascending=False)
    top10 = sorted.head(10)
    top10.y_on_y = top10.y_on_y.apply(lambda x: '{:.2%}'.format(x))
    bottom10 = sorted.tail(10)
    bottom10.y_on_y = bottom10.y_on_y.apply(lambda x: '{:.2%}'.format(x))
    print("top 10:")
    print(top10)
    print("bottom 10:")
    print(bottom10)
    top10.to_csv("r_top10.csv", index=False)
    bottom10.sort_values(by='y_on_y', ascending=False).to_csv("r_bottom10.csv", index=False)

    # 一线城市与新一线城市做图
    rate_mean = np.mean(sorted['y_on_y'])

    first_tier = sorted[sorted['city'].isin(['北京', '上海', '广州', '深圳'])]
    print('一线城市:')
    print(first_tier)
    new_first_tier = sorted[sorted['city'].isin(['成都', '杭州', '重庆', '武汉', '苏州', '西安',
                                                 '天津', '南京', '郑州', '长沙', '沈阳', '青岛',
                                                 '宁波', '东莞', '无锡'])]
    print('新一线城市:')
    print(new_first_tier)

    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots()
    ax.bar(new_first_tier['city'].values, new_first_tier['y_on_y'].values)
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax.axhline(rate_mean, ls='--', color='r')
    ax.text(9, rate_mean+0.05, '286城收益率均值')
    ax.set(ylim=[-0.1, 1], xlabel='', ylabel='投资收益率', title='新一线城市投资收益率')
    fig.savefig('new_first_tier.png', transparent=False, dpi=80, bbox_inches="tight")

    fig2, ax2 = plt.subplots()
    ax2.bar(first_tier['city'].values, first_tier['y_on_y'].values)
    labels = ax2.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax2.axhline(rate_mean, ls='--', color='r')
    ax2.text(2, rate_mean + 0.05, '286城收益率均值')
    ax2.set(ylim=[-0.1, 1], xlabel='', ylabel='投资收益率', title='一线城市投资收益率')
    fig2.savefig('first_tier.png', transparent=False, dpi=80, bbox_inches="tight")

   # 计算百城投资收益指数
    rate = (result[this_month]/result[last_month]).mean()
    index = last_month_index*rate
    print("index: ")
    print(index)
    print("m_on_m: ")
    print(index/last_month_index-1)
    print("y_on_y: ")
    print(index/same_month_index-1)

def city_index(this_month):
    df = pd.read_csv('286index.csv')
    sorted = df.sort_values(by=this_month, ascending=false)