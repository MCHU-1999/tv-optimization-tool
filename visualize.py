from sklearn.manifold import TSNE
from sklearn.datasets import load_iris
import numpy as np
from numpy import reshape
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timezone, timedelta
import time
import os


def timeNow():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    return dt2.strftime("%Y-%m-%d %H-%M-%S")
    
def plot_heatmap(x: pd.DataFrame, y: pd.DataFrame, target: pd.DataFrame, ticker: str, trade_num=[]):
    df = pd.DataFrame()
    trade_num_df = pd.DataFrame()

    for _x, _y, _target, _trade_num in zip(x, y, target, trade_num):
        df.at[f'{_x}', _y] = _target
        trade_num_df.at[f'{_x}', _y] = _trade_num
    df = df.reindex(columns=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])
    trade_num_df = trade_num_df.reindex(columns=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])
    df = df.fillna(0)
    print(trade_num_df)

    np_trade_num = trade_num_df.fillna(0).to_numpy(dtype=int)
    sns.set (rc = {'figure.figsize':(16, 10)})
    sns.heatmap(df, cmap='Spectral').set(title=f"[{ticker}] profit - special condition")

    for i in range(4):
        for j in range(len([15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])):
            text = plt.text(j+0.5, i+0.5, f'{np_trade_num[i, j]}', ha="center", va="center", color="black")

    plt.savefig(f'./{CHART_PATH}/{CSV_FOLDER_NAME}/{ticker}_heatmap.png')
    plt.close()
    return None
    

CSV_FOLDER_NAME = '2023-09-09'
CHART_PATH = './chart_data'
FILES = os.listdir(f'./output/{CSV_FOLDER_NAME}')
# -------------------------------------------------------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    if not (os.path.exists(f'./chart_data/')):
        os.mkdir(f'./chart_data')
    if not (os.path.exists(f'./chart_data/{CSV_FOLDER_NAME}')):
        os.mkdir(f'./chart_data/{CSV_FOLDER_NAME}')
    if not (os.path.exists(f'./output/')):
        os.mkdir(f'./output')

    # print(FILES)
    for each in FILES:
        ticker = each.split('_')[0]

        # read csv
        df = pd.read_csv(f'./output/{CSV_FOLDER_NAME}/{ticker}_Optimization.csv', header=0, names=[
            'param1',
            'param2',
            'param3',
            'param4',
            'param5',
            'param6',
            'Profit (USDT)',
            'Profit (%)',
            'Total Closed Trades',
            'Percent Profitable',
            'Profit Factor',
            'MDD (USDT)',
            'MDD (%)',
            'Avg Trade',
            'Avg Trade (%)',
            'Avg Bars'
            ], dtype={
            'Profit (USDT)': np.float32
            })
        print(ticker)

        # data in different format
        x = df[['param1', 'param2', 'param3', 'param4', 'param5', 'param6']]
        xi = df['param1'] * 2 + df['param2']
        xii = df[['param3', 'param4', 'param5', 'param6']]
        xiii = df[['param3', 'param4', 'param5']]

        param1 = df['param1']
        param2 = df['param2']
        param3 = df['param3']
        param4 = df['param4']
        param5 = df['param5']

        # target data
        profit_percent = df["Profit (%)"]
        profit_usdt = df["Profit (USDT)"]
        profit_factor = df["Profit Factor"]
        mdd_percent = df["MDD (%)"]
        mdd_usdt = df["MDD (USDT)"]
        trades_num = df["Total Closed Trades"]
        # print(min(trades_num))

        plot_heatmap(xi, param3, profit_factor, ticker, trades_num)
        # plot(profit_usdt, mdd_usdt, param1, f'{ticker}', trades_num)