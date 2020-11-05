from selenium import webdriver #selenium の webdriverをインポート
from time import sleep
import urllib
import re
import csv

SQRAPING_URL = 'https://jp.indeed.com' #指定のURLを代入
MAX_NUMBER = 50
search_keyword = input("検索したいキーワードを入力してください。>>> ") #検索キーワードを代入
search_kinmuchi = input("検索したい勤務地を入力してください。>>> ")

###サイトを開く
driver = webdriver.Chrome("chromedriver.exe",False) #chromedriverのパスを引数に指定しchromeを起動 変数driverに代入
driver.implicitly_wait(10)
driver.get(SQRAPING_URL) #指定してURLに移動

###検索窓に文字列を入力
search_box_keyword = driver.find_element_by_id('text-input-what').send_keys(search_keyword) #indeedのサイトの検証から検索窓のhtml idを指定して検索窓検知 
search_box_kinmuchi = driver.find_element_by_id('text-input-where').send_keys(search_kinmuchi) #indeedのサイトの検証から検索窓のhtml idを指定して検索窓検知 

##検索ボタンをクリックする処理
sleep(1)
search_button = driver.find_element_by_class_name('icl-Button.icl-Button--primary.icl-Button--md.icl-WhatWhere-button').click() #class_nameを指定して検索ボタンを検知 

#ここに絞り込み条件を指定する処理
search_dropdpwn_button = driver.find_element_by_id('filter-job-type').click()
sleep(1)
search_dropdpwn_button_24h = driver.find_element_by_xpath('//*[@id="filter-job-type-menu"]/li[1]/a').click()
sleep(1)

count = 0
contents = []
page = 0
while True:
    page = page + 1 
    search_results_td = driver.find_element_by_id('resultsCol')
    search_results = search_results_td.find_elements_by_class_name('jobsearch-SerpJobCard.unifiedRow.row.result.clickcard')
    
    for result in search_results:
        count = count + 1

        company_name = result.find_element_by_class_name("company")
        location = result.find_element_by_class_name("location.accessible-contrast-color-location")
        #salary = result.find_element_by_class_name("salarySnippet")
        title = result.find_element_by_class_name('title')

        content = {
            'company_name': company_name.text,
            'location': location.text,
            #'salary': salary.text,
            'title': title.text,
        }
        contents.append(content)
        #ここにcsv書き込みのコードを記述
        with open('indeed.csv', 'a', encoding='utf-8') as f:
                f.write('\n')
                f.write(str(content))

        sleep(1)
        if count == MAX_NUMBER:
            break
        
    if count == MAX_NUMBER:
        break

    url = urllib.parse.urlparse(driver.current_url) #対象のURLを構成要素に分解する
    #次のページに進む処理
    if page == 1:
        query = url.query + '&start=10'
    else:
        query = re.sub('start=[1-9][0-9]*', 'start=' +str(10*page), url.query)
    print(url.query)

    url = url.scheme + '://' + url.netloc + url.path + '?' + query
    driver.get(url)
    
#print(contents)

driver.close()
driver.quit()

#https://jp.indeed.com/jobs?q=%E9%AB%98%E5%8F%8E%E5%85%A5&l=%E6%9D%B1%E4%BA%AC%E9%83%BD
#https://jp.indeed.com/jobs?q=%E9%AB%98%E5%8F%8E%E5%85%A5&l=%E6%9D%B1%E4%BA%AC%E9%83%BD&start=10
#https://chiebukuro.yahoo.co.jp/search/?p=a&flg=3&class=1&ei=UTF-8&fr=common-navi
#https://chiebukuro.yahoo.co.jp/search?p=a&flg=3&class=1&ei=UTF-8&fr=common-navi&b=11
#ParseResult(scheme='https', netloc='jp.indeed.com', path='/jobs', params='', query='q=%E9%AB%98%E5%8F%8E%E5%85%A5&l=%E6%9D%B1%E4%BA%AC%E9%83%BD', fragment='')

