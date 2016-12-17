#!/usr/bin/python3

from argparse import ArgumentParser
import requests, re
import os

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
	parser.add_argument('-u', '--url' , help='URL target')
	parser.add_argument('-w', '--wordlist' , help='Dictionary')
	parser.add_argument('-e', '--extensions' , help='Extension list separated by comma (Example: php,asp)')
	parser.add_argument('-x', '--excludestatus', help='Exclude status code, separated by comma (example: 301,500)')
	return parser.parse_args()

def GetRobots(url):
	print('Get robots.txt')
	req = requests.get('%s/robots.txt' %(url))
	if req.status_code == 200:
		print('Parse robots.txt')
		txt = req.text.replace('Disallow: /', '').replace('Allow: /', '')
		comments = re.findall('#[^\n]+', txt)
		ua = re.findall('User-agent:[^\n]+', txt)
		for item in comments: txt = txt.replace(item, '')
		for item in ua: txt = txt.replace(item, '')
		file = open('robots.lst', 'w')
		file.write(txt)
		file.close()

def Search(url, ext, wordlist, code=''):
	code = str(code)
	if len(code) == 0:
		os.system('sudo dirsearch -r -f -u %s -e %s -w %s' %(url, ext, wordlist))
	else:
		os.system('sudo dirsearch -r -f -u %s -e %s -w %s -x %s' %(url, ext, wordlist, code))

def main():
	args = ParseArgs()
	URL = args.url
	EXT = args.extensions
	WORDLIST = args.wordlist
	CODE = args.excludestatus
	GetRobots(URL)
	if WORDLIST != '':
		os.system('cat %s robots.lst | sort -u > /tmp/wordlist.txt' %(WORDLIST))
		Search(URL, EXT, '/tmp/wordlist.txt', CODE)
	else:
		Search(URL, EXT, 'robots.lst', CODE)

if __name__ == '__main__':
	main()
