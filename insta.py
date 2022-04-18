#! /usr/bin/env python
# -*- coding: utf-8 -*-


from get_chrome_driver import GetChromeDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


import time
import random
import csv
import datetime
# import numpy as np

USER_ID = "hirao.program"
USER_PASS = "E74yDq5V"
FOLLOW_NUM = 10
TAG_LISTS = [
    'ポーカー',
    'アミューズメントカジノ',
    'オンラインポーカー',
    'GGポーカー',
]

DOMAIN_BASE = "https://www.instagram.com/"
LOG_NAME = "insta_log.csv"


def get_driver():

    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(options=options)

    # return driver

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)


# twitterログイン


def do_login(driver):
    # ログインURL
    login_url = DOMAIN_BASE + "accounts/login/"
    driver.get(login_url)

    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ

    driver.save_screenshot('login.png')
    # driver.save_screenshot('hoge.png')
    # 電話、メールまたはユーザー名のinput要素が読み込まれるまで待機（最大10秒）
    elem_id = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )

    # driver.save_screenshot('insta.png')
    try:
        # パスワードのinput要素
        elem_password = driver.find_element_by_name("password")

        if elem_id and elem_password:
            # ログインID入力
            elem_id.send_keys(USER_ID)

            # パスワード入力
            elem_password.send_keys(USER_PASS)

            # driver.save_screenshot('insta_.png')

            # ログインボタンクリック
            elem_btn = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="loginForm"]/div/div[3]/button'))
            )

            actions = ActionChains(driver)
            actions.move_to_element(elem_btn)
            actions.click(elem_btn)
            actions.perform()

            # 適当（3秒間待つように対応しています）
            time.sleep(5)

            # 遷移
            # 遷移後のURLでログイン可否をチェック
            perform_url = driver.current_url

            if perform_url.find(login_url) == -1:
                # ログイン成功
                print('成功')
                return True
            else:
                print('失敗１')
                # ログイン失敗
                return False
        else:
            print('失敗２')
            return False
    except:
        print('失敗３')
        return False


def tagselect():

    tag = random.choice(TAG_LISTS)

    return tag


def tagsearch(tag):

    driver.save_screenshot('before_search.png')
    instaurl = 'https://www.instagram.com/explore/tags/'
    driver.get(instaurl + tag + '/')
    # driver.save_screenshot('b.png')
    time.sleep(random.randint(2, 10))
    print('search : ' + tag)
    driver.implicitly_wait(10)


def click_follow_fav():
    # driver.save_screenshot('a.png')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    target = driver.find_elements_by_class_name('_9AhH0')[0]

    actions = ActionChains(driver)
    actions.move_to_element(target)
    actions.perform()
    time.sleep(0.3)

    limit = range(random.randint(200, 300))
    # limit = range(400)
    driver.execute_script("arguments[0].click();", target)

    index = 0

    print("--------")

    for i in limit:
        print(str(i))
        time.sleep(2)

        element = driver.switch_to.active_element

        for j in range(20):
            element.send_keys(Keys.TAB)
            element = driver.switch_to.active_element

            if len(element.find_elements_by_tag_name('svg')) > 0:
                childElement = element.find_element_by_tag_name("svg")
                fav_label = childElement.get_attribute("aria-label")
                if fav_label == 'いいね！':
                    element.send_keys(Keys.ENTER)
                    break
                elif fav_label == '「いいね！」を取り消す':
                    break

        for j in range(20):
            element.send_keys(Keys.SHIFT, Keys.TAB)
            element = driver.switch_to.active_element

            if len(element.find_elements_by_tag_name('svg')) > 0:
                childElement = element.find_element_by_tag_name("svg")
                fav_label = childElement.get_attribute("aria-label")
                if fav_label == '次へ':
                    element.send_keys(Keys.ENTER)
                    break

        index += 1

    print("終了しました")

    return index


def follows():

    # 対象アカウントのInstagramページにアクセス
    driver.get('https://www.instagram.com/' + USER_ID + '/')

    # 3秒スリープ（待機）
    time.sleep(3)

    # 画面上で、フォロワーのリンクをクリック
    follower_button = driver.find_elements_by_css_selector("li.Y8-fY")[2]
    follower_button.click()

    # 3秒スリープ（待機）
    time.sleep(3)

    # フォロワーの一覧は、ポップアップウインドウで表示されます
    dialog = driver.find_element_by_css_selector("div.isgrP")
    for i in range(200):
        index = i / 2
        if index % 1 == 0:
            print('follows ' + str(int(index)) + '/100')
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        time.sleep(random.randint(500, 1000)/1000)

    page_url = driver.page_source
    soup = BeautifulSoup(page_url, "lxml")
    elements = soup.find_all("a", {"class": "FPmhX notranslate _0imsa"})
    follows = []
    # 取得できたフォロワー名を配列にadd
    for value in elements:
        follows.append(value.text)

    # csvに書き出し
    # df = pd.Series(follows)
    # df.to_csv(USER_ID + '_follows_list.csv')

    return follows


def followers():

    # 対象アカウントのInstagramページにアクセス
    driver.get('https://www.instagram.com/' + USER_ID + '/')

    # 3秒スリープ（待機）
    time.sleep(3)

    # 画面上で、フォロワーのリンクをクリック
    follower_button = driver.find_elements_by_css_selector("li.Y8-fY")[1]
    follower_button.click()

    # 3秒スリープ（待機）
    time.sleep(3)

    # フォロワーの一覧は、ポップアップウインドウで表示されます
    dialog = driver.find_element_by_css_selector("div.isgrP")
    for i in range(200):
        index = i / 2
        if index % 1 == 0:
            print('followers ' + str(int(index)) + '/100')
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        time.sleep(random.randint(500, 1000)/1000)

    page_url = driver.page_source
    soup = BeautifulSoup(page_url, "lxml")
    elements = soup.find_all("a", {"class": "FPmhX notranslate _0imsa"})
    followers = []
    # 取得できたフォロワー名を配列にadd
    for value in elements:
        followers.append(value.text)

    # csvに書き出し
    # df = pd.Series(followers)
    # df.to_csv(USER_ID + '_followers_list.csv')

    return followers


def ryoomoi(follows, followers):
    # ryoomoi = [follows in followers]
    # ryoomoi = set(follows) & set(followers)
    ryoomoi = [e for e in followers if e in follows]

    # df = pd.Series(followers)
    # df.to_csv(USER_ID + '_ryoomoi_list.csv')
    return ryoomoi


def kataomoi(follows, followers):
    # kataomoi = np.where(follows not in followers)
    kataomoi = [e for e in follows if e not in followers]

    # df = pd.Series(followers)
    # df.to_csv(USER_ID + '_kataomoi_list.csv')
    return kataomoi


def kataomoware(follows, followers):
    # kataomoware = np.where(followers not in follows)
    kataomoware = [e for e in followers if e not in follows]

    # df = pd.Series(followers)
    # df.to_csv(USER_ID + '_kataomoware_list.csv')
    return kataomoware


def unfollow(lists):
    print('unfollow')
    for list in lists:
        try:
            print('un follow : ' + list)
            # フォローを外すアカウントのInstagramページにアクセス
            driver.get('https://www.instagram.com/' + list + '/')

            # 3秒スリープ（待機）
            time.sleep(3)

            # フォローを外すボタンをクリック
            follower_button = driver.find_element_by_css_selector(
                ".glyphsSpriteFriend_Follow").click()
            time.sleep(1)

            # フォローを外すボタンをクリック
            follower_button = driver.find_element_by_css_selector(
                ".aOOlW.-Cab_").click()

            time.sleep(random.randint(
                random.randint(2, 5), random.randint(10, 15)))
        except:
            print('error')


if __name__ == "__main__":

    dt_now = datetime.datetime.now()

    # Driver
    driver = get_driver()
    # ログイン
    login_flg = do_login(driver)

    #
    # follows = follows()
    # followers = followers()
    # ryoomoi = ryoomoi(follows, followers)
    # kataomoi = kataomoi(follows, followers)
    # kataomoware = kataomoware(follows, followers)
    # print("follows")
    # print(follows)
    # print("followers")
    # print(followers)
    # print("ryoomoi")
    # print(ryoomoi)
    # print("kataomoi")
    # print(kataomoi)
    # print("kataomoware")
    # print(kataomoware)
    # unfollow(kataomoi)

    # for i in range(17):

    # タグの取得
    tag = tagselect()

    print(tag)
    # タグで検索
    tagsearch(tag)

    # # ログに出力
    # csvlist = []
    # csvlist.append(tag)
    # csvlist.append(dt_now)
    # csvlist.append(0)

    # f2 = open(LOG_NAME, 'a', encoding="utf-8", newline='')
    # writer = csv.writer(f2)
    # writer.writerow(csvlist)
    # f2.close()

    # 自動いいねと自動フォロー
    click_follow_fav()

    driver.quit()
