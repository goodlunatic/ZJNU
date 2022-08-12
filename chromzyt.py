#-*- coding: UTF-8 -*- 
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def check(userId, password, name, address):
    # linux需要无头浏览器
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')    
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--disable-gpu')
    driver_path = r'/root/chrome/chromedriver'
    driver =driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
    try:
        driver.get('http://zyt.zjnu.edu.cn/Login/EIPV4/login.aspx')
        time.sleep(0.5)
        # 登录
        driver.find_element(By.NAME, 'UserText').send_keys(userId)
        time.sleep(0.5)
        driver.find_element(By.NAME, 'PasswordText').send_keys(password)
        time.sleep(0.5)
        driver.find_element(By.CLASS_NAME, 'btn-login').click()
        time.sleep(0.5)
        driver.get('http://zyt.zjnu.edu.cn/H5/ZJSFDX/CheckFillIn.aspx')
        html = driver.page_source
        # 检测是否打卡
        if '<div id="check2" style="display:;">' in html:
            driver.quit()
            return "READY"
        else:
            driver.get('http://zyt.zjnu.edu.cn/H5/ZJSFDX/FillIn.aspx')
            time.sleep(0.5)
            # 绿码
            driver.find_element(By.ID, 'DATA_5_1').click()
            time.sleep(0.5)
            # 浙江师范大学本部校区
            driver.find_element(By.ID, 'DATA_13_1').click()
            time.sleep(0.5)
            '''
            # 离校打卡
            driver.find_element(By.ID, 'DATA_13_4').click()
            time.sleep(0.5)
            driver.find_element(By.ID, 'DATA_14').send_keys(address.replace('✰',''))
            time.sleep(0.5)
            '''
            driver.find_element(By.NAME, 'DATA_15').click()
            time.sleep(0.5)
            js = f"document.getElementById('hidDATA_17').value = '{address}'"
            driver.execute_script(js)
            time.sleep(0.5)
            driver.find_element(By.ID, 'btn_save').click()
            time.sleep(0.5)
            driver.quit()
            print(f"[+] {name}提交成功!")
            return f'{name}已打 ({userId}) {address}\n'
    except Exception as e:
        driver.quit()
        return "ERROR"
    finally:
        driver.quit()

def check_arg():
    arglen = len(sys.argv)
    if (arglen == 1):
        all_call()
    else:
        one_call()

def all_call():
    message = "自动打卡"+str(time.strftime('%Y-%m-%d',time.localtime(time.time()))) + "\n"
    accounts = []
    with open("/root/zyt/accounts.txt","r") as f:
        accounts = f.readlines()
    for i in range(len(accounts)):
        s_id = accounts[i].split()[0]
        s_pwd = accounts[i].split()[1]
        s_name = accounts[i].split()[2]
        # s_addr = accounts[i].split()[3] # 自定义地址
        s_addr = '浙江省✰金华市✰婺城区'
        print('[-] 正在进行', f'{s_name}({s_id})', '打卡...')
        ms = check(s_id, s_pwd, s_name, s_addr)
        if ms == 'READY':
            print('[+]', f'{s_name}({s_id})', '已经打卡！')
            ms = f'{s_name}已打 ({s_id}) {s_addr}\n'
        elif ms == 'ERROR':
            print('[!]', f'{s_name}({s_id})', '打卡异常！')
            ms = f'{s_name}异常 ({s_id}) {s_addr}\n'
        message += ms
        time.sleep(1)
    print("\n"+message)
    with open ("/root/zyt/log.txt","a") as f:
        f.write(message)

def one_call():
    message = "手动打卡"+str(time.strftime('%Y-%m-%d',time.localtime(time.time()))) + "\n"
    s_id = sys.argv[1]
    s_pwd = sys.argv[2]
    s_name = sys.argv[3]
    s_addr = '浙江省✰金华市✰婺城区'
    print('[-] 正在进行', f'{s_name}({s_id})', '打卡...')
    ms = check(s_id, s_pwd, s_name, s_addr)
    if ms == 'READY':
        print('[+]', f'{s_name}({s_id})', '已经打卡！')
        ms = f'{s_name}已打 ({s_id}) {s_addr}\n'
    elif ms == 'ERROR':
        print('[!]', f'{s_name}({s_id})', '打卡异常！')
        ms = f'{s_name}异常 ({s_id}) {s_addr}\n'
    message += ms
    print("\n"+message)
    with open ("/root/zyt/log.txt","a") as f:
        f.write(message)

if __name__ == "__main__":
    check_arg()