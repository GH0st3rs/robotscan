#!/usr/bin/python3
from argparse import ArgumentParser, REMAINDER
import requests
import re
import os
import json
from urllib.parse import urlparse

HOST = ''
REPORT = ''

if not (os.path.exists('/usr/bin/dirsearch') or os.path.exists('/bin/dirsearch')):
    msg = """dirsearch not found
Use:
    sudo git clone https://github.com/maurosoria/dirsearch.git /usr/share/dirsearch
    sudo ln -s /usr/share/dirsearch/dirsearch.py /usr/bin/dirsearch
    sudo chmod +x /usr/share/dirsearch/dirsearch.py"""
    print(msg)
    exit(0)


def ParseArgs():
    parser = ArgumentParser()
    parser.add_argument('-u', '--url', required=True, help='URL target')
    parser.add_argument('-w', '--wordlist', required=True, help='Dictionary')
    parser.add_argument('-e', '--extensions', required=True, help='Extension list separated by comma (example: php,asp)')
    parser.add_argument('-x', '--excludestatus', type=str, help='Exclude status code, separated by comma (example: 301,500)')
    parser.add_argument('-a', '--args', nargs=REMAINDER,
                        help='Other args for dirsearch. Use quotes for parameters (example: "--timeout=0 -t 20")')
    return parser.parse_args()


def GetRobots(url):
    print('Get robots.txt')
    req = requests.get('%s/robots.txt' % url, verify=False)
    if req.status_code == 200:
        print('Parse robots.txt')
        txt = req.text.replace('Disallow: /', '').replace('Allow: /', '')
        comments = re.findall('#[^\n]+', txt)
        ua = re.findall('User-agent:[^\n]+', txt)
        for item in comments:
            txt = txt.replace(item, '')
        for item in ua:
            txt = txt.replace(item, '')
        file = open('robots.lst', 'w')
        file.write(txt)
        file.close()


def Search(url, ext, wordlist, code='', args=''):
    if len(code) == 0:
        os.system('sudo dirsearch -r -f -u %s -e %s -w %s --json-report=%s %s' % (url, ext, wordlist, REPORT, args))
    else:
        os.system('sudo dirsearch -r -f -u %s -e %s -w %s --json-report=%s -x %s %s' % (url, ext, wordlist, REPORT, code, args))
    report = json.load(open(REPORT))
    fil = filter(lambda x: x['status'] == 301, report[list(report)[0]])
    urls = list(map(lambda x: x['redirect'], fil))
    for item in urls:
        Search(item, ext, wordlist, code, args)


def main():
    global HOST
    global REPORT
    args = ParseArgs()
    URL = args.url
    HOST = urlparse(URL).netloc
    REPORT = os.path.join('/tmp', 'dirsearch_%s' % HOST)
    EXT = args.extensions
    WORDLIST = args.wordlist
    CODE = args.excludestatus
    DIRSEARCH_ARGS = args.args
    GetRobots(URL)
    if WORDLIST != '':
        os.system('cat %s robots.lst | sort -u > /tmp/wordlist.txt' % WORDLIST)
        Search(URL, EXT, '/tmp/wordlist.txt', CODE, DIRSEARCH_ARGS)
    else:
        Search(URL, EXT, 'robots.lst', CODE, DIRSEARCH_ARGS)


if __name__ == '__main__':
    main()
