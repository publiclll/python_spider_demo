import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import bidmessage

browser = webdriver.Chrome()
#browser = webdriver.PhantomJS
wait = WebDriverWait(browser,10)
base_url_list = []
base_domain = 'http://www.ccgp-sichuan.gov.cn'

def search():
    try:
        browser.get("http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=search&years=2018&chnlNames=\u4E2D\u6807\u516C\u544A&chnlCodes=8a817eb738e5e70c0138e66e141c0ea1&title=\u6559\u80B2%20\u4E2D\u6807&tenderno=&agentname=&buyername=&startTime=2019-01-01&endTime=2019-07-20&distin_like=510000&province=510000&city=&town=&provinceText=\u56DB\u5DDD\u7701&cityText=\u8BF7\u9009\u62E9&townText=\u8BF7\u9009\u62E9&pageSize=10&searchResultForm=search_result_anhui.ftl")
        total_str = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR ,"body > div:nth-child(35) > div.list-info > div.info > div > div:nth-child(2)"))
        )
        total_num = int(total_str.text.split('/',1)[1])
        nowpage = int(total_str.text.split('/',1)[0].split(':',1)[1])
        getmessagelist()
        return [nowpage,total_num]
    except TimeoutException:
        return search()

def nextpage(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR ,'#targetPage'))
        )
        submit = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR ,'#QuotaList_target'))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        total_str = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "body > div:nth-child(35) > div.list-info > div.info > div > div:nth-child(2)"))
        )
        nowpage = int(total_str.text.split('/', 1)[0].split(':', 1)[1])
        if nowpage == page_number:
            getmessagelist()
    except TimeoutException:
        nextpage(page_number)

def getmessagelist():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR ,'body > div:nth-child(35) > div.list-info > div.info > ul > li'))
    )
    html_content = browser.page_source
    doc = pq(html_content)
    items = doc('body > div:nth-child(35) > div.list-info > div.info > ul > li').items()
    for item in items:
        link_str = item.find('a').attr('href')
        if link_str.startswith('http'):
            base_url_list.append(link_str)
        else:
            base_url_list.append(base_domain + link_str)

def getmessage():
    for url in base_url_list:
        getmessage_content(url)

def getmessage_content(url):
    try:
        browser.get(url)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR ,"#myPrintArea"))
        )
        html_content = browser.page_source
        doc = pq(html_content)
        trs = doc('#myPrintArea > table > tbody').items();
        for tr in trs:
            bidname = tr.find("tr:nth-child(2) > td:nth-child(2)").text()
            bidcompany = tr.find("tr:nth-child(21) > td:nth-child(2)").text()
            bidamount = tr.find("tr:nth-child(19) > td:nth-child(2)").text()
            biddate = tr.find("tr:nth-child(17) > td:nth-child(2)").text()
            purchaser = tr.find("tr:nth-child(9) > td:nth-child(2)").text()
            purchaseraddr = tr.find("tr:nth-child(10) > td:nth-child(2)").text()
            bidurl = url
            bidmessage.savedata(bidcompany, bidamount, biddate, purchaser, purchaseraddr, bidurl, bidname)
            #time.sleep(0.5)
    except Exception:
        print("Exception url : <" + url + ">")
        #getmessage_content(url)


def main():
    #total有两个元素，0是当前页码，1是总页数
    total = search()
    for i in range(2,total[1] + 1):
        nextpage(i)
    getmessage()


if __name__ == '__main__':
    main()
