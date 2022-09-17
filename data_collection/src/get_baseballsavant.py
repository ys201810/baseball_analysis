# coding=utf-8
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import subprocess
BASE_DIR = os.path.join(os.getcwd(), '..')
print(BASE_DIR)

player_name_id_dict = {
    'Darvish_Yu': '506433'
}


def run():
    target_player = 'Darvish_Yu'
    if target_player not in player_name_id_dict.keys():
        print('not exist player name')
        exit(1)

    target_player_type = 'pitcher'  # 'pitcher' or 'batter'
    target_year = [2019, 2020, 2021]

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    target_url = 'https://baseballsavant.mlb.com/statcast_search'
    try:
        driver.get(target_url)

        # 条件指定
        # Player Typeの指定
        element = driver.find_element(By.XPATH, '//*[@id="player_type"]')
        select = Select(element)
        select.select_by_value(target_player_type)

        # Seasonの指定
        for year in target_year:
            element = driver.find_element(By.XPATH, '//*[@id="ddlSeason"]/div[1]')
            element.click()
            element = driver.find_element(By.XPATH, '//*[@id="chk_Sea_' + str(year) + '"]')
            element.click()

        # Player nameの指定
        if target_player_type == 'pitcher':
            element = driver.find_element(By.XPATH, '//*[@id="pitchers_lookup"]')
            # terms.click()
            select = Select(element)
            select.select_by_value(player_name_id_dict[target_player])

        # searchボタンの実行
        element = driver.find_element(By.XPATH, '//*[@id="pfx_form"]/div[3]/div/input[1]')
        element.click()

        # データのダウンロード
        element = driver.find_element(By.XPATH, '//*[@id="csv_all_pid_"]')
        element.click()

        # リネームして保存
        out_file = os.path.join(BASE_DIR, 'data', 'baseball_servent', target_player + '.csv')
        subprocess.run(['mv', '/Users/shirai1/Downloads/savant_data.csv', out_file])


    finally:
        driver.quit()


if __name__ == '__main__':
    run()
