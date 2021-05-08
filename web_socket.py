# -*-codeing = utf-8 -*-
# @FIle ： web_socket
# @Time : 2021/5/8 11:26
# @Author : 山与河　qq 2900180755
import random
import socket
import time
import requests
import threading
from lxml import etree

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
}


ip_list = []


def ip_verification(list):
    i = -1
    try:
        for ip_dic in list:
            ip = ip_dic['ip']
            link = 'https://2021.ip138.com'
            proxies = {'http': ip,'https': ip}
            result = requests.get(link, headers=headers, proxies=proxies, timeout=3)   # 验证存活
            tree = etree.HTML(result.text)
            title = tree.xpath('/html/body/p[1]/text()')[1]
            title_ls = title.replace('\n', '').replace('\r', '').replace(']', '')
            if result.status_code == 200:
                i +=1
                print('>>>验证有效ip',len(ip_list),ip,title_ls)
            time.sleep(0.1)
    except Exception as a:
        i += 1
        print('>>>删除验证失效ip',ip)
        return i

def ip():
    try:
        ip_json = requests.get(url="http://api.moyo1.cn/api/v1/proxy",headers=headers).json()
        ip = ip_json["data"]['proxy']  # 采集 ip
        link = 'https://2021.ip138.com'
        proxies = {'http': ip,'https': ip}
        result = requests.get(link, headers=headers, proxies=proxies, timeout=3)   # 验证存活
        tree = etree.HTML(result.text)
        title = tree.xpath('/html/body/p[1]/text()')[1]
        title_ls = title.replace('\n', '').replace('\r', '').replace(']', '')
        if result.status_code == 200:
            print('>>>采集有效ip',len(ip_list),ip,title_ls)
            ret = {'ip':ip,'title':title_ls}
            return ret
        time.sleep(0.1)
    except Exception as a:
        return

def IP_start():
    num = 5
    while True:
        if len(ip_list) < num:
            ip_dic = ip()
            if ip_dic != None:
                ip_list.append(ip_dic)

        else:  # 补充ip
            print('>>>ip池已满 正在验证存活......')
            i = ip_verification(ip_list)
            if i != None:
                ip_list.pop(i)


def main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(('localhost',8888))
    sock.listen(5)

    while True:
        if ip_list != []:
            ip_port = random.choice(ip_list)
            conn,addr = sock.accept()
            data = conn.recv(1024)
            print(f'>>>成功返回代理 {ip_port}')
            conn.send(b"HTTP/1.1 200 OK \r\n Content-Type:text/html; charset=utf-8\r\n\r\n")
            conn.send(str(ip_port).encode("gbk"))
            conn.close()


t1 = threading.Thread(target=main)
t2 = threading.Thread(target=IP_start)
t1.start()
t2.start()