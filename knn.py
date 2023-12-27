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
    settingModal = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@data-dialog-name="Machine Learning: Lorentzian Classification (TORIII)"]')))

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
        # Loop Start [5] -----------------------------------------------------------
        while True:
            clearBoxes(inputBoxes, [iterateBoxNum[0]])
            inputBoxes[iterateBoxNum[0]].send_keys(iterateNow[0])
            inputBoxes[iterateBoxNum[0]].send_keys(Keys.ENTER)

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
                # save data to csv
                newline_df.to_csv(folderPath + symbol +'_Optimization.csv', mode='a', index=False, header=False)
            else :
                print(f'Attribute-{iterateNow} -skipped.', end='\r')
            
            # Looptail------------------------------------------------------------------
            if iterateNow[0] >= iterateFirst[0] and iterateNow[0] < iterateLast[0]:
                iterateNow[0] += 0.5
            else:
                iterateNow[0] = iterateFirst[0]
                break
            # --------------------------------------------------------------------------
        print('\n')
        return copy(iterateLast)
    except Exception as e :
        print(f'\nerror!\n{e}')
        return copy(iterateNow)


# -------------------------------------------------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------------------------------------------------
USER_ID = "AO9wdyl1"
EXCHANGE = "BITGET"
# SYMBOLS = ["ADA", "APE", "BCH", "BTC", "ETC", "ETH", "FIL", "GMT", "LTC", "LINK", "SOL"]
SYMBOLS = ['AUDIO', 'HIGH', 'OCEAN', 'SAND', 'USDC', 'MAGIC', 'BTC', 'LINK', 'CTSI', 'IMX', 'BAND', 'LOOKS', 'ARB', 'EGLD', 'BSV', 'MANA', 'BNX', 'XMR', 'ENJ', 'MASK', 'AAVE', 'LTC', 'GMX', 'IOTA', 'STG', 'LRC', 'PHB', 'LQTY', 'GTC', 'TON', 'SOL', 'KAVA', 'STX', 'KLAY', 'QTUM', 'ZEC', 'AVAX', 'YFI', 'MINA', 'COMP', 'SUSHI', 'SSV', 'BAT', 'LDO', 'ATOM', 'ICP', 'UNI', 'SNX', 'OMG', 'HOOK', 'SXP', 'FXS', 'BNB', 'API3', 'GFT', 'TOMO', 'SFP', 'RDNT', 'RUNE', 'ETH', 'MKR', 'ZRX', 'UNFI', 'LIT', 'BLUR', 'KNC', 'ENS', 'ETC', 'NEO', 'AR', 'FOOTBALL', 'ALICE', '1INCH', 'KSM', 'DASH', 'APE', 'MATIC', 'HFT', 'ICX', 'BEL', 'OP', 'FLM', 'DYDX', 'EOS', 'DAR', 'DOT', 'XTZ', 'NEAR', 'WAVES', 'INJ', 'STORJ', 'UMA', 'GMT', 'FTM', 'BGHOT10', 'GAL', 'RNDR', 'APT', 'ID', 'CRV', 'TRB', 'CHR', 'ONT', 'BCH', 'ZEN', 'THETA', 'FLOW', 'C98', 'AXS', 'RLC', 'FIL', 'LUNA2', 'FET', 'AGIX', 'METAHOT', 'CELO', 'ALGO', 'MTL', 'JOE']
ROOT_PATH = f'./output/{dateNow()}-knn/'

# 1 => 5min, 2 => 15 min, 3 => 1hour, 4 => 2hour, 5 => 4hour
TIME_SCALE = 5
INPUT_BOX_NUM = [20]
START         = [-5]
END           = [10]


# -------------------------------------------------------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    now = copy(START)

    if not os.path.exists(ROOT_PATH):
        os.makedirs(ROOT_PATH)
        print(f"Create new directory {ROOT_PATH}.")

    for each_symbol in SYMBOLS:
        while True :
            with open('tv-cookie.json') as f:
                cookies = json.load(f)
                f.close()

            driver = webdriver.Chrome('./chromedriver')
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