import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
from lxml.html import fromstring
from random import randint, uniform, shuffle, choice
from time import sleep
from password_generator import PasswordGenerator
from selenium_stealth import stealth
from faker import Faker
from fake_headers import Headers
import traceback


def Type_Me(element: WebElement, text: str):
    for character in text:
        element.send_keys(character)
        sleep(uniform(.07, .15))

def Fetch_Proxies():
    url = 'https://sslproxies.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies_list = list()
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies_list.append(proxy)
    shuffle(proxies_list)
    return proxies_list

def Get_Valid_Proxy(proxies_list):
    header = Headers(
        headers=False
    ).generate()
    agent = header['User-Agent']

    headers = {
        'User-Agent': f'{agent}',
    }

    url = 'http://icanhazip.com'
    while(True):
        proxy = choice(proxies_list)
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
        }
        try:
            response = requests.get(url , headers=headers, proxies=proxies, timeout=1)
            if(response.status_code == 200):
                return proxy
        except:
            continue


def Generate_Proxy():
    proxies_list = Fetch_Proxies()
    proxy = Get_Valid_Proxy(proxies_list)
    return proxy


def Prepare_Env(proxy):
    header = Headers(
        browser="chrome",
        os="win",
        headers=False
    ).generate()
    agent = header['User-Agent']

    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-web-security')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f'--user-agent={agent}')
    options.add_argument(f'--proxy-server=http://{proxy}')
    options.add_extension('./nopecha.crx')
    
    driver = uc.Chrome(options=options)

    driver.delete_all_cookies()

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver


def Generate_Account_Details():
    fake = Faker()
    
    pw = PasswordGenerator()
    pw.minlen = 9
    pw.maxlen = 26
    password = pw.generate()

    username = fake.user_name()+'00'+str(randint(1, 1000))
    firstname = fake.first_name()
    lastname = fake.last_name()

    birth_day = str(randint(1, 28))
    birth_month = str(randint(1, 12))
    birth_year = str(randint(1960, 2006))
    
    return password, username, firstname, lastname, birth_day, birth_month, birth_year


def Create_Outlook_Account(driver: uc.Chrome, password, username, firstname, lastname, birth_day, birth_month, birth_year):

    driver.get('https://outlook.live.com/owa/?nlp=1&signup=1')

    field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="MemberName"]')))
    Type_Me(field, username)

    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="iSignupAction"]')))
    button.click()

    field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="PasswordInput"]')))
    Type_Me(field, password)

    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="iOptinEmail"]')))
    button.click()

    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="iSignupAction"]')))
    button.click()

    field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="FirstName"]')))
    Type_Me(field, firstname)

    field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="LastName"]')))
    Type_Me(field, lastname)

    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="iSignupAction"]')))
    button.click()

    country = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Country"]'))))
    country.select_by_value('US')
    sleep(1)

    country = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BirthMonth"]'))))
    country.select_by_value(birth_month)
    sleep(1)

    country = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BirthDay"]'))))
    country.select_by_value(birth_day)
    sleep(1)

    field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BirthYear"]')))
    Type_Me(field, birth_year)

    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="iSignupAction"]')))
    button.click()

    try:
        wait.until(EC.title_contains('Microsoft account'))
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="KmsiCheckboxField"]')))
        button.click()

        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]')))
        button.click()

    except Exception as ex:
        print(ex.msg)
        traceback.print_exc()

    try:
        wait.until(EC.title_contains('Outlook'))
        print('Outlook Account Created Successfully xD!')
        with open('account.txt', 'w') as f:
            f.write(f"Email: {username}@outlook.com\n")
            f.write(f"Password: {password}\n")
            f.close()

    except Exception as ex:
        print(ex.msg)
        traceback.print_exc()
        driver.close()
    

if __name__ == "__main__":

    try:
        proxy = Generate_Proxy()

        driver = Prepare_Env(proxy)

        wait = WebDriverWait(driver, 10)

        password, username, firstname, lastname, day, month, year = Generate_Account_Details()

        Create_Outlook_Account(driver, password, username, firstname, lastname, day, month, year)

        driver.close()

    except Exception as ex:
        print(ex.msg)
        sleep(1000)