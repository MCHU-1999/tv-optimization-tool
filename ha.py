import os
import sys
import json
from copy import copy
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import pandas as pd
from datetime import datetime, timezone, timedelta


def timeNow():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    return dt2.strftime("%Y-%m-%d %H-%M-%S")

def dateNow():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    return dt2.strftime("%Y-%m-%d")

def resetBoxes(inputBoxes, iterateBoxNum, iterateLast):
    try:
        # print("RESET...")
        for i, eachNum in enumerate(iterateBoxNum):
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            inputBoxes[eachNum].send_keys(str(iterateLast[i]))
        # print("DONE")
        return True
    except Exception as e:
        print(e)
        return False

def clearBoxes(inputBoxes, iterateBoxNum):
    try:
        # print("CLEAR...")
        for eachNum in iterateBoxNum:
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            inputBoxes[eachNum].send_keys(Keys.BACK_SPACE)
            # print("DONE")
        return True
    except Exception as e:
        print(e)
        return False

def spinnerAppear(driver):
    try:
        spinner = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'tv-spinner.tv-spinner--shown.tv-spinner--size_large')))
        return True
    except Exception as e:
        print(e)
        return False
    
# pseudo code for while loop:
def pseudoLoop(iterateFirst, iterateLast, iterateNow):
    while True:
        if iterateNow >= iterateFirst and iterateNow <= iterateLast:
            iterateNow += 1
        else:
            iterateNow = iterateFirst
            break
        # Do something
        # ...
        # ...

def split_usdt(original_text):
    split_list = original_text.split(' ')
    number_str = ''.join(split_list[0:-1])
    return number_str

def split_sign(original_text):
    if '%' in original_text:
        original_text = original_text.split('%')[0]
    else:
        pass

    if '−' in original_text:
        split_list = original_text.split('−')
        return str(float(split_list[1]) * -1)
    else:
        return original_text


def run(driver, userId, exchange, timeScale, symbol, iterateBoxNum, iterateFirst, iterateLast, iterateNow, folderPath):
    print(symbol+' optimization start...')

    # redirect to tradingview graph
    tradingView = f"https://www.tradingview.com/chart/{userId}/?symbol={exchange}%3A{symbol}USDT.P"    
    driver.get(tradingView)
    # driver.minimize_window()

    # set timescale
    timeScaleBtn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[2]/div[3]/div/div/div[3]/div[1]/div/div/div/div/div[4]/div/div/button[{str(timeScale)}]')))
    timeScaleBtn.click()

    # open setting modal 
    settingBtn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bottom-area"]/div[4]/div/div[1]/div[1]/div[1]/div[2]/button[1]')))
    settingBtn.click()
    settingModal = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@data-dialog-name="HeikinAshi-Oscillator (TORIII)"]')))

    # get input boxes & close button 
    # closeBtn = settingModal.find_element(By.CLASS_NAME, 'close-BZKENkhT')
    inputBoxes = settingModal.find_elements(By.TAG_NAME, 'input')
    resetBoxes(inputBoxes, iterateBoxNum, iterateLast)
    sleep(2)

    # -------------------------------------------------------------------------------------------------------
    # LOOP START
    # -------------------------------------------------------------------------------------------------------
    dataContainer = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[7]/div[2]/div[4]/div/div[2]/div/div[1]')))

    try :
        # Loop Start [0] -----------------------------------------------------------
        while True:
            clearBoxes(inputBoxes, [iterateBoxNum[0]])
            inputBoxes[iterateBoxNum[0]].send_keys(iterateNow[0])

            # Loop Start [1] -----------------------------------------------------------
            while True:
                clearBoxes(inputBoxes, [iterateBoxNum[1]])
                inputBoxes[iterateBoxNum[1]].send_keys(iterateNow[1])

                # Loop Start [2] -----------------------------------------------------------
                while True:
                    clearBoxes(inputBoxes, [iterateBoxNum[2]])
                    inputBoxes[iterateBoxNum[2]].send_keys(iterateNow[2])

                    # Loop Start [3] -----------------------------------------------------------
                    while True:
                        clearBoxes(inputBoxes, [iterateBoxNum[3]])
                        inputBoxes[iterateBoxNum[3]].send_keys(iterateNow[3])

                        # Loop Start [4] -----------------------------------------------------------
                        while True:
                            clearBoxes(inputBoxes, [iterateBoxNum[4]])
                            inputBoxes[iterateBoxNum[4]].send_keys(iterateNow[4])

                            # Loop Start [5] -----------------------------------------------------------
                            while True:
                                clearBoxes(inputBoxes, [iterateBoxNum[5]])
                                inputBoxes[iterateBoxNum[5]].send_keys(iterateNow[5])
                                inputBoxes[iterateBoxNum[5]].send_keys(Keys.ENTER)

                                if spinnerAppear(driver) :      # check if spinner appears
                                    # get data
                                    dataContainer = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[7]/div[2]/div[4]/div/div[2]/div/div[1]')))
                                    secondRow_L = dataContainer.find_elements(By.XPATH, '//*[@class="secondRow-Yvm0jjs7"]/div[1]')
                                    secondRow_R = dataContainer.find_elements(By.XPATH, '//*[@class="secondRow-Yvm0jjs7"]/div[2]')
                                    
                                    profit = split_usdt(secondRow_L[0].text)
                                    mdd = split_usdt(secondRow_L[4].text)
                                    avg_trade = split_usdt(secondRow_L[5].text)

                                    # save data
                                    newline = [[
                                        iterateNow[0],
                                        iterateNow[1],
                                        iterateNow[2],
                                        iterateNow[3],
                                        iterateNow[4],
                                        iterateNow[5],
                                        split_sign(profit),
                                        split_sign(secondRow_R[0].text),
                                        secondRow_L[1].text,
                                        split_sign(secondRow_L[2].text),
                                        split_sign(secondRow_L[3].text),
                                        split_sign(mdd),
                                        split_sign(secondRow_R[4].text),
                                        split_sign(avg_trade),
                                        split_sign(secondRow_R[5].text),
                                        secondRow_L[6].text
                                    ]]
                                    # newline_df = pd.DataFrame(data=newline, columns=output_columns)
                                    newline_df = pd.DataFrame(data=newline)
                                    print(f'Attribute-{iterateNow} -done.', end='\r')
                                else :
                                    print(f'Attribute-{iterateNow} -skipped.', end='\r')
                                
                                # save data to csv
                                newline_df.to_csv(folderPath + symbol +'_Optimization.csv', mode='a', index=False, header=False)
                                # print(iterateFirst, iterateLast)
                                # print('->'+iterateNow)
                            
                                # Looptail------------------------------------------------------------------
                                if iterateNow[5] >= iterateFirst[5] and iterateNow[5] < iterateLast[5]:
                                    iterateNow[5] += 1
                                else:
                                    iterateNow[5] = iterateFirst[5]
                                    break
                                # --------------------------------------------------------------------------
                            # Looptail------------------------------------------------------------------
                            if iterateNow[4] >= iterateFirst[4] and iterateNow[4] < iterateLast[4]:
                                iterateNow[4] += 1
                            else:
                                iterateNow[4] = iterateFirst[4]
                                break
                            # --------------------------------------------------------------------------
                        # Looptail------------------------------------------------------------------
                        if iterateNow[3] >= iterateFirst[3] and iterateNow[3] < iterateLast[3]:
                            iterateNow[3] += 1
                        else:
                            iterateNow[3] = iterateFirst[3]
                            break
                        # --------------------------------------------------------------------------
                    # Looptail------------------------------------------------------------------
                    if iterateNow[2] >= iterateFirst[2] and iterateNow[2] < iterateLast[2]:
                        iterateNow[2] += 1
                    else:
                        iterateNow[2] = iterateFirst[2]
                        break
                    # --------------------------------------------------------------------------
                # Looptail------------------------------------------------------------------
                if iterateNow[1] >= iterateFirst[1] and iterateNow[1] < iterateLast[1]:
                    iterateNow[1] += 1
                else:
                    iterateNow[1] = iterateFirst[1]
                    break
                # --------------------------------------------------------------------------
            # Looptail------------------------------------------------------------------
            if iterateNow[0] >= iterateFirst[0] and iterateNow[0] < iterateLast[0]:
                iterateNow[0] += 1
            else:
                iterateNow[0] = iterateFirst[0]
                break
            # --------------------------------------------------------------------------
        # Loop End -----------------------------------------------------------------
        print('\n')
        return copy(iterateLast)
    except Exception as e :
        print(f'\nerror!\n{e}')
        return copy(iterateNow)


# -------------------------------------------------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------------------------------------------------
USER_ID = "KKx78WKX"
EXCHANGE = "BITGET"
SYMBOLS = ['AXS', 'APT', 'APE', 'ALICE', 'ALGO', 'AAVE', '1INCH', 'AVAX']
# SYMBOLS = ['BTC', 'ZRX', 'XTZ', 'SUSHI', 'TOMO', 'NEAR', 'LQTY', 'JOE', 'IOTA', 'ICP', 'EOS', 'ENJ', 'DYDX', 'DOT', 'CRV', 'CHR', 'AXS', 'APT', 'APE', 'ALICE', 'ALGO', 'AAVE', '1INCH', 'AVAX']
ROOT_PATH = f'./output/{dateNow()}/'

TIME_SCALE = 2          # 1 => 5min, 2 => 15 min, 3 => 1hour, 4 => 2hour, 5 => 4hour.
INPUT_BOX_NUM = [12,13,14,18,20,21]
START = [0, 0, 15, 5, 6, 3]
END = [1, 1, 30, 5, 6, 3]


# -------------------------------------------------------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    now = copy(START)
    print(split_sign('-2233.89%'))

    if not os.path.exists(ROOT_PATH):
        os.makedirs(ROOT_PATH)
        print(f"Create new directory {ROOT_PATH}.")

    for each_symbol in SYMBOLS:
        while True :
            with open('tv-cookie.json') as f:
                cookies = json.load(f)
                f.close()

            driver = webdriver.Chrome('./chromedriver')
            # driver = webdriver.Chrome()
            # driver.maximize_window()
            driver.get('https://www.tradingview.com/')

            for cookie in cookies:
                driver.add_cookie({
                    "name": cookie["name"],
                    "value": cookie["value"]
                })
        
            result = run(driver, USER_ID, EXCHANGE, TIME_SCALE, each_symbol, INPUT_BOX_NUM, START, END, now, ROOT_PATH)
            if result == END:
                now = copy(START)
                print(f'{each_symbol}-done')
                driver.quit()
                break
            else :
                now = result
                print(f'{each_symbol}-error, restarting with last set of parameters: {now}')
                driver.quit()
    print('\nOptimization done, have a nice day:)))')