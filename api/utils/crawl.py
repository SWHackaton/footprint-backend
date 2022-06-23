from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time,os

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#CHROME_FILE = os.path.join(BASE_DIR, 'chromedriver.exe')

#make_options() set Options for Chrome Driver
def make_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.67 Safari/537.36')
    chrome_options.add_argument("--log-level=3") #최소 로그레벨 3(FATAL)로 설정. Critical한거 아니면 로그 안찍힘
    chrome_options.add_argument('--headless') #UI를 띄우지 않고 Background에서 동작
    chrome_options.add_argument('--no-sandbox')
    return chrome_options

#make_driver() returns Webdriver
def make_driver():
    chrome_options = make_options()
#    driver = webdriver.Chrome(CHROME_FILE,options=chrome_options)
#    driver = webdriver.Chrome('C:\\Users\\kms00\\OneDrive\\바탕 화면\\GitHub\\footprint-backend\\api\\utils\\chromedriver.exe',options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# 초기 세팅. 무조건 이부분이 실행되고 나서, crawl_store함수가 실행되어야 한다.
def crawl_init():
    driver = make_driver()
    driver.implicitly_wait(5)
    url = "https://map.kakao.com/"
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_id("dimmedLayer").click()
    time.sleep(1)

    driver.find_element_by_id("search.keyword.query").send_keys('서울시 동작구 흑석동 흑석로 87')
    driver.find_element_by_id("search.keyword.submit").click()
    time.sleep(0.3)
    driver.find_element_by_class_name("tit_coach").click()
    return driver


def crawl_store_img(store_list,dong):
    driver = make_driver()
    driver.implicitly_wait(5)
    url = "https://www.google.com/search?q=aa&sxsrf=ALiCzsbE-gtqyeTMVdsVUecmNpnPibFMWg:1655968979685&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj97auWhcP4AhUB4GEKHVDVDl8Q_AUoAXoECAIQAw&cshid=1655968982818043&biw=1536&bih=754&dpr=1.25"
    driver.get(url)
    time.sleep(1)


    for store in store_list:
        try:
            driver.find_element_by_id("REsRA").clear()
            driver.find_element_by_id("REsRA").send_keys(dong + ' ' + store['store_name'])
            driver.find_element_by_id("BIqFsb").click()
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[1]').click()
            time.sleep(0.7)
            store['img'] = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute("src")
            if(len(store['img'])> 200):
                store['img'] = ''
        except:
            store['img'] = ''
            url = "https://www.google.com/search?q=aa&sxsrf=ALiCzsbE-gtqyeTMVdsVUecmNpnPibFMWg:1655968979685&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj97auWhcP4AhUB4GEKHVDVDl8Q_AUoAXoECAIQAw&cshid=1655968982818043&biw=1536&bih=754&dpr=1.25"
            driver.get(url)
            time.sleep(0.3)

    driver.close()
    return store_list

# driver = crawl_init()
# crwal_store(driver,address)
def crawl_store(driver,address):
    store_list = []
    try:
        driver.find_element_by_id("search.keyword.query").clear()
        driver.find_element_by_id("search.keyword.query").send_keys(address)
        driver.find_element_by_id("search.keyword.submit").click()
        time.sleep(0.3)
        store_cnt = int(driver.find_element_by_id("info.search.place.cnt").text)

        print(store_cnt)
        if(store_cnt > 5):
            driver.find_element_by_id("info.search.place.more").click()
        time.sleep(1)
        elements = driver.find_elements_by_class_name("PlaceItem")
        for element in elements:
            store_name = ' '.join(element.text.split("\n")[2].split(" ")[1:-1])
            store_category = element.text.split("\n")[2].split(" ")[-1]
            store_list.append({"store_name" : store_name,"store_category" : store_category})

    except Exception as e:
        driver.find_element_by_class_name("tit_coach").click()
        print("Crawling Error")
        print(e)

    return store_list


if __name__ == '__main__':
    driver = crawl_init()
    address = "서울시 동작구 흑석동 흑석로 87"
    print(crawl_store(driver,address))
    address = "서울시 동작구 흑석동 흑석로 94"
    print(crawl_store(driver,address))
    address = "서울시 동작구 흑석동 흑석로 75-1"
    print(crawl_store(driver,address))
    address = "서울시 동작구 흑석동 흑석로 79"
    print(crawl_store(driver,address))

