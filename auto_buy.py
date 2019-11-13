import requests
import json
import time
from selenium import webdriver
from datetime import timedelta, datetime

gouwuche_url = "https://buy.tmall.com/login/buy.do?from=cart"
time_api_url = "http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp"
confirm_url = "https://buy.tmall.com/order/confirm_order.htm?spm=a1z0d.6639537.0.0.undefined"
cookie_str = "_m_h5_tk=e8734772d14be9ecae36e7d4d2d048c8_1573537603341; hng=CN%7Czh-CN%7CCNY%7C156; dnk=ursaa; uc1=pas=0&cookie21=W5iHLLyFeYZ1WM9hVLhR&existShop=false&cart_m=0&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&lng=zh_CN&cookie15=URm48syIIVrSKA%3D%3D&tag=8&cookie14=UoTbnr35Yx6mzg%3D%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dByuWm2kAbOgooFE4%3D&id2=UUkLXlAPOONllw%3D%3D&nk2=FnhZx5M%3D; tracknick=ursaa; lid=ursaa; uc4=nk4=0%40FE2ZM4vWsrCjUtS%2FpaCpKw%3D%3D&id4=0%40U2uHdu9dpwrmigZScUGNdXvBE1YQ; _l_g_=Ug%3D%3D; unb=2159094188; lgc=ursaa; cookie1=UUwVNUDYPGDJ5ElyrOz8HiHuWyc9oAyvn%2FG2BpXqb00%3D; login=true; cookie17=UUkLXlAPOONllw%3D%3D; cookie2=1a62f4ea9ef578bf8ef7f1cb40d8fb01; _nk_=ursaa; t=df657c2a6ed6f94d54c1d87d6e241e4b; sg=a89; csg=1448e9ea; enc=8ukcJ3vnDsWzsTRBj%2Fn71u%2F%2BsR9BxFN80IxlcXRmzg%2F0%2FGk51lDV6nrdWlC80yCfUI4cfUB6R%2FSj4LQcH1ncwQ%3D%3D; _tb_token_=5b3b34433533b; ubn=p; ucn=center"

cookies = {
    "cna": "eGvLEh0yBjECAXQYQhvaWn0d",
    "_m_h5_tk": "e8734772d14be9ecae36e7d4d2d048c8_1573537603341",
    "_tb_token_": "5b3b34433533b",
    "_m_h5_tk_enc": "4b31fdbf1ab60f4ee18ce4e9f1654dea"
}
common_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    #"Host": "buy.tmall.com"
}

headers = {
    "origin": "https://cart.taobao.com",
    "Referer": "https://cart.taobao.com/cart.htm"
}


def get_cookies():
    cookies = {}
    for kv in cookie_str.split("; "):
        k = kv.split("=")[0]
        v = kv.split("=")[1]
        cookies[k] = v
    return cookies


def check_login():
    cookies = get_cookies()
    print(cookies)
    r = requests.get(gouwuche_url, cookies = cookies, headers=common_headers)
    resp = r.content.decode('utf-8')
    print(resp)
    jdata = json.loads(resp.replace("loginIndicator=", ""))
    is_loggin = jdata['hasLoggedIn']
    return is_loggin


def get_utc13():
    return str(int(time.time()*1000))


def confirm_order():
    post_data = {
        "hex": "n",
        "cartId": "1622730216586",
        "sellerid": "725677994",
        "cart_param": {"items":[{"cartId":"1622730216586","itemId":"20739895092","skuId":"4227830352490","quantity":2,"createTime":1573457259000,"attr":";op:149900;cityCode:440305;itemExtra:{};"}]},
        "unbalance": "",
        "delCartIds": "1622730216586",
        "use_cod": "false",
        "buyer_from": "cart",
        "page_from": "cart",
        "source_time": get_utc13()
    }
    print(post_data)
    r = requests.post(confirm_url, cookies = get_cookies(), data=post_data, headers=headers)
    print(r.text)


def get_time_gap():
    try:
        r = requests.get(time_api_url, timeout=2)
        remote_time = int(json.loads(r.text)['data']['t'])
        local_time = int(time.time()*1000)
        time_gap = remote_time - local_time
    except Exception as e:
        time_gap = 600
    finally:
        return time_gap


def login():
    login_url = "https://login.tmall.com/?spm=875.7931836/B.a2226mz.1.66144265JujCnu&redirectURL=https%3A%2F%2Fwww.tmall.com%2F"
    driver.get(login_url)
    print("开始登陆")
    time.sleep(20)


def keep_login(buy_time):
    dt = datetime.strptime(buy_time, '%Y-%m-%d %H:%M:%S')
    while True:
        if datetime.now() + timedelta(seconds=5) < dt:
            print("当前时间{},继续刷新等待".format(datetime.now()))
            driver.refresh()
            time.sleep(2)
        else:
            break


def buy(buy_time):
    driver.get("https://cart.taobao.com/cart.htm")
    print("当前时间{},开始执行".format(datetime.now()))
    time_gap = get_time_gap()
    print("gap:{}".format(time_gap))
    if driver.find_element_by_id("J_SelectAll1"):
        driver.find_element_by_id("J_SelectAll1").click()
        print("当前时间{},已点击全选".format(datetime.now()))
    while True:
        if time_gap + time.time()*1000 > time.mktime(time.strptime(buy_time, '%Y-%m-%d %H:%M:%S'))*1000:
            print("当前时间{},开始".format(datetime.now()))
            if driver.find_element_by_id("J_Go"):
                driver.find_element_by_id("J_Go").click()
                print("当前时间{},已点击结算".format(datetime.now()))
                #print(driver.page_source)
                if "以下宝贝已不能购买" in driver.page_source:
                    print("当前时间{},重新进入购物车".format(datetime.now()))
                    driver.get("https://cart.taobao.com/cart.htm")
                    if driver.find_element_by_id("J_SelectAll1"):
                        driver.find_element_by_id("J_SelectAll1").click()
                        print("当前时间{},已点击全选".format(datetime.now()))
                        continue

                while True:
                    try:
                        driver.find_element_by_link_text('提交订单').click()
                        print("当前时间{},已点击提交订单".format(datetime.now()))
                        break
                    except Exception as e:
                        print("当前时间{},未找到提交订单按钮".format(datetime.now()))
                        time.sleep(0.01)
                    if time.time()*1000 > time.mktime(time.strptime(buy_time, '%Y-%m-%d %H:%M:%S'))*1000 + 60000:
                        print("当前时间{},执行终止".format(datetime.now()))
                        break
        if time.time()*1000 > time.mktime(time.strptime(buy_time, '%Y-%m-%d %H:%M:%S'))*1000 + 60000:
            print("当前时间{},执行终止".format(datetime.now()))
            break
        print("当前时间{},继续等待".format(datetime.now()))
    driver.close()


driver = webdriver.Chrome()
if __name__ == '__main__':
    buy_time = '2019-11-13 22:00:00'
    login()
    keep_login(buy_time)
    buy(buy_time)
    # gap = get_time_gap()
    # print(gap)
    # print(type(time.time()))
    # timestamp = time.mktime(time.strptime(buy_time, '%Y-%m-%d %H:%M:%S'))
    # print(timestamp)

