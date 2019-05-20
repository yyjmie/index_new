import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def save_table(old_file, new_file, this_month):
    
    df = pd.read_csv(old_file)

    if this_month not in df.columns:
        df2 = pd.read_csv(new_file)
        result = pd.merge(df ,df2, on='city')
        result.to_csv(old_file, index=False)


def sale_calculate(last_month, same_month, this_month):
    
    df = pd.read_csv('286sale.csv', usecols=['city', same_month, last_month, this_month])

    # 计算同比和环比
    df['y_on_y'] = (df[this_month]-df[same_month]) / df[same_month]
    df['m_on_m'] = (df[this_month]-df[last_month]) / df[last_month]

    # 得到同比和环比上涨数量和涨幅
    y_up = df[df.y_on_y>=0]['y_on_y']
    m_up = df[df.m_on_m>=0]['m_on_m']
    y_on_y_up_num = len(y_up)
    m_on_m_up_num = len(m_up)
    y_on_y_up_rate = y_up.mean()
    m_on_m_up_rate = m_up.mean()

    y_down = df[df.y_on_y<0]['y_on_y']
    m_down = df[df.m_on_m<0]['m_on_m']
    y_on_y_down_num = len(y_down)
    m_on_m_down_num = len(m_down)
    y_on_y_down_rate = y_down.mean()
    m_on_m_down_rate = m_down.mean()

    # 保存
    o = pd.read_csv("sale_change.csv", index_col=['日期'])
    o.loc[this_month] = [m_on_m_up_num, '%.4f'%m_on_m_up_rate, y_on_y_up_num, '%.4f'%y_on_y_up_rate, 
                         m_on_m_down_num, '%.4f'%m_on_m_down_rate, y_on_y_down_num, '%.4f'%y_on_y_down_rate]
    o.to_csv("sale_change.csv")


def index_calculate(last_month, same_month, this_month):
    
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
    
    # save
    sorted.to_csv("rate_new.csv", index=False)
    top10.to_csv("r_top10.csv", index=False)
    bottom10.sort_values(by='y_on_y', ascending=False).to_csv("r_bottom10.csv", index=False)

   # 计算百城投资收益指数
    df_index = pd.read_csv('index_change.csv',index_col=['date'])
    last_month_index = df_index.at[last_month,'index']
    same_month_index = df_index.at[same_month,'index']

    rate = (result[this_month]/result[last_month]).mean()
    index = last_month_index*rate

    df_index.loc[this_month] = '%.2f'%index
    df_index.to_csv('index_change.csv')

    print("index: ")
    print(index)
    print("m_on_m: ")
    print(index/last_month_index-1)
    print("y_on_y: ")
    print(index/same_month_index-1)

