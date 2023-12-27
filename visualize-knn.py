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

def label(data):
    float_data = float(data)
    if float_data >= 0 and float_data < 25:
        return 5
    elif float_data >= 25 and float_data < 50:
        return 6
    elif float_data >= 50 and float_data < 75:
        return 7
    elif float_data >= 75 and float_data < 100:
        return 8
    elif float_data >= 100:
        return 9
    elif float_data <= 0 and float_data > -25:
        return 0
    elif float_data <= -25 and float_data > -50:
        return 1
    elif float_data <= -50 and float_data > -75:
        return 2
    elif float_data <= -75 and float_data > -100:
        return 3
    elif float_data < -100:
        return 4
    
    
def tsne_plot(x, y, ticker, filename):
    tsne = TSNE(n_components=2, verbose=1, random_state=123)
    z = tsne.fit_transform(x)

    df = pd.DataFrame()
    df["y"] = y
    df["comp-1"] = z[:,0]
    df["comp-2"] = z[:,1]

    sns.scatterplot(x="comp-1", y="comp-2", hue=df.y.tolist(),
                    palette=sns.color_palette("Spectral", as_cmap=True),
                    data=df).set(title=f"{ticker} {filename}_projection")
    plt.savefig(f'{filename}.png')
    plt.close()
    return None

def plot_3D(x, y, z, target, ticker, filename, trailing_stop):
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection='3d')

    # Add x, y gridlines
    ax.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.3,
            alpha = 0.2)
    
    # Creating color map
    # my_cmap = plt.get_cmap('Spectral')
    
    # Creating plot
    sctt = ax.scatter3D(x, y, z,
                        alpha = 0.6,
                        c = target,
                        cmap = plt.get_cmap('Spectral'))
    
    plt.title(f"{ticker}, trailing stop = {trailing_stop}")
    ax.set_xlabel('param-3', fontweight ='bold')
    ax.set_ylabel('param-4', fontweight ='bold')
    ax.set_zlabel('param-5', fontweight ='bold')
    ax.view_init(30, 120)
    fig.colorbar(sctt, ax = ax, shrink = 0.5, aspect = 5)

    plt.savefig(f'./chart_data/{ticker}/{filename}.png')
    plt.close()
    return None

def plot(x, y, target, ticker, trade_num=[]):
    # x = x.to_numpy()
    df = pd.DataFrame()
    df["y"] = target
    df["profit"] = x
    df["mdd"] = y

    sns.scatterplot(x="profit", y="mdd", hue=df.y.tolist(), alpha=0.5,
                    palette=sns.color_palette("flare", as_cmap=True), s=400,
                    data=df).set(title=f"{ticker} profit - special condition")
    for i, (tar, num) in enumerate(zip(target, trade_num)):
        if num > 30 and x[i] > y[i]*1.2 and tar >= 2.0 and tar <= 3.0:
            plt.text(x[i]-0.2, y[i]-0.2, f"{num}, {tar}")
        else:
            plt.text(x[i]-0.2, y[i]-0.2, "")

    plt.savefig(f'./chart_data/{ticker}_knn.png')
    plt.close()
    return None

def plot_heatmap(x: pd.DataFrame, y: pd.DataFrame, target: pd.DataFrame, ticker: str):
    df = pd.DataFrame()

    for _x, _y, _target in zip(x, y, target):
        df.at[f'{_x}', _y] = _target
    df = df.reindex(columns=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])
    print(df)

    sns.heatmap(df, cmap='Spectral').set(title=f"[{ticker}] profit - special condition")
    plt.savefig(f'./chart_data/{ticker}_heatmap.png')
    plt.close()
    return None
    

# TICKER = 'SOL'
CSV_PATH = './output/2023-06-25-knn'
FROM_PATH = './chart_data'
FILES = os.listdir(FROM_PATH)
# -------------------------------------------------------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    if not (os.path.exists(f'./chart_data/')):
        os.mkdir(f'./chart_data')

    # print(FILES)
    for each in FILES:
        ticker = each.split('_')[0]
        if "DS" in ticker or "bad" in ticker:
            continue 

        # read csv
        df = pd.read_csv(f'{CSV_PATH}/{ticker}_Optimization.csv', header=0, names=[
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
        # x = df[['param1', 'param2', 'param3', 'param4', 'param5', 'param6']]
        # xi = df['param1'] * 2 + df['param2']
        # xii = df[['param3', 'param4', 'param5', 'param6']]
        # xiii = df[['param3', 'param4', 'param5']]

        param1 = df['param1']
        # param2 = df['param2']
        # param3 = df['param3']
        # param4 = df['param4']
        # param5 = df['param5']

        # target data
        profit_percent = df["Profit (%)"]
        profit_usdt = df["Profit (USDT)"]
        mdd_percent = df["MDD (%)"]
        mdd_usdt = df["MDD (USDT)"]
        trades_num = df["Total Closed Trades"]
        # print(min(trades_num))

        # plot_heatmap(xi, param3, profit_usdt, ticker)
        plot(profit_usdt, mdd_usdt, param1, f'{ticker}', trades_num)