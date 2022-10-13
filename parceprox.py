from urllib import response
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.request
import socket
import random
import time
socket.setdefaulttimeout(180)


def parce_proxy_list(type):
    if type == 'http':
        ua = UserAgent()
        url = 'https://free-proxy-list.net/'
        responce = requests.get(
            url, headers={'user-agent': f'{ua.random}'})
        result = responce.content

        soup = BeautifulSoup(result, 'lxml')

        table = soup.find('table', class_='table table-striped table-bordered')
        rows = table.find_all('tr')

        proxy_list = []
        for row in rows:
            if row.find('td') != None:
                data = [i.text for i in row.find_all('td')]
                proxy_list.append(data)

        return proxy_list
    elif type == 'socks':
        ua = UserAgent()
        url = 'https://www.socks-proxy.net/'
        responce = requests.get(url, headers={'user-agent': f'{ua.random}'})
        result = responce.content

        soup = BeautifulSoup(result, 'lxml')

        table = soup.find('table', class_='table table-striped table-bordered')
        rows = table.find_all('tr')

        proxy_list = []
        for row in rows:
            if row.find('td') != None:
                data = [i.text for i in row.find_all('td')]
                proxy_list.append(data)

        return proxy_list

    else:
        print('[Input Error]: Enter valid type (http or socks)')


def check_proxy(proxy_list, proxy_num, randomize, type):
    if randomize == 'y':
        random.shuffle(proxy_list)

    count = 0
    for i in range(len(proxy_list)):
        ip = proxy_list[i][0]
        port = proxy_list[i][1]
        proxy = ip + ':' + port
        if int(proxy_num) > count:
            if is_bad_proxy(proxy, type):
                print('Bad proxy checked..\n')
            else:
                print(
                    f'[Good Proxy]: {proxy_list[i][0]} {proxy_list[i][1]} | {proxy_list[i][3]} | {proxy_list[i][4]} | Google: {proxy_list[i][5]} | Https: {proxy_list[i][6]}\n')
                count += 1
        else:
            print('[DONE] Found ' + str(count) + ' proxies')
            break


def is_bad_proxy(proxy, type):
    if type == 'http':
        try:
            proxy_handler = urllib.request.ProxyHandler({'http': proxy})
            opener = urllib.request.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            sock = urllib.request.urlopen('http://www.google.com')
        except urllib.error.HTTPError as e:
            # print('Error code: ', e.code)
            return e.code
        except Exception as detail:
            # print("ERROR:", detail)
            return 1
        return 0

    elif type == 'socks':
        proxy_handler = {f'http': "socks4://{}"}
        try:
            requests.get('http://www.google.com', timeout=3,
                         proxies=dict(http='socks4://user:pass@'+proxy,
                                      https='socks4://user:pass@host:port'+proxy))
        except:
            return 1
        return 0


if __name__ == '__main__':
    type = input('Enter type [http/socks]: ')
    proxy_list = parce_proxy_list(type)
    proxy_num = input('Enter number of proxies to get: ')
    randomize = input('Shuffle proxy list? [y/n]: ')
    print('[INFO] Starting the search...')
    check_proxy(proxy_list, proxy_num, randomize, type)
