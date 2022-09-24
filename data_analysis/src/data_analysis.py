# coding=utf-8
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
BASE_DIR = os.path.join(os.getcwd(), '..', '..')
print(BASE_DIR)
fp = FontProperties(fname=r'/Users/shirai1/.local/share/virtualenvs/baseball_analysis-BxQ8eODn/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/ipaexg.ttf', size=16)

plt.rcParams['figure.subplot.bottom'] = 0.2
plt.rcParams['lines.linewidth'] = 3

def main():
    target_data = os.path.join(BASE_DIR, 'data_collection', 'data', 'baseball_savant', 'Darvish_Yu.csv')  # 'Darvish_Yu.csv'
    player_name = os.path.basename(target_data).replace('.csv', '')
    df = pd.read_csv(target_data)

    # 対象の球種を指定
    # ダルビッシュ用
    df = df[(df['game_date'] >= '2016-01-01') & (df['game_date'] <= '2017-12-31')]
    target_types = ['FF', 'SL', 'SI', 'FC']
    target_type_names = ['4シーム', 'スライダー', '2シーム', 'カッター']
    target_colors = ['red', 'blue', 'green', 'gray']

    # 大谷(ピッチャー)用
    """
    df = df[(df['game_date'] >= '2020-01-01') & (df['game_date'] <= '2021-12-31')]
    target_types = ['FF', 'SL', 'FS', 'FC']
    target_type_names = ['4シーム', 'スライダー', 'ファストボール', 'カッター']
    target_colors = ['red', 'blue', 'green', 'gray']
    """

    print(f'データ範囲:{df["game_date"].min()} ~ {df["game_date"].max()}')

    date_types = df.groupby(['game_date', 'pitch_type'])['release_spin_rate'].mean().index.tolist()
    dates = sorted(df['game_date'].unique().tolist())

    # 対象の球種を全て利用していない日をデータから抜く。
    no_use_dates = []
    for date in dates:
        pitch_types = [val[1] for val in date_types if val[0] == date]
        if len(set(pitch_types) & set(target_types)) != len(target_types):
            no_use_dates.append(date)
    df = df[~df['game_date'].isin(no_use_dates)]
    date_types = df.groupby(['game_date', 'pitch_type'])['release_spin_rate'].mean().index.tolist()
    spins = df.groupby(['game_date', 'pitch_type'])['release_spin_rate'].mean().values.tolist()
    dates = sorted(df['game_date'].unique().tolist())

    for i, target_type in enumerate(target_types):
        tmp_indexes = [n for n, v in enumerate(date_types) if v[1] == target_type]
        tmp_dates = [v[0] for n, v in enumerate(date_types) if v[1] == target_type]
        tmp_spins = [val for i, val in enumerate(spins) if i in tmp_indexes]
        plt.plot(np.array(tmp_dates), np.array(tmp_spins), color=target_colors[i], label=target_type_names[i])

    plt.title(player_name + '_'+ dates[0] + '_' + dates[-1] + 'の投球の回転数の日別推移', fontproperties=fp)
    plt.xticks(rotation=90)
    plt.legend(loc=0, prop=fp)
    # plt.show()
    plt.savefig(os.path.join(BASE_DIR, 'data_analysis', 'data', 'output', player_name + '.png'))
    print(1)

if __name__ == '__main__':
    main()
