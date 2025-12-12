# MVP
import requests 
import time

url='https://www.bilibili.com'
header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

path= '../db/dicc.txt'  #文件路径
#按照行读取文件内容返回行的内容
def read_files(file_path):
	lines=[]
	with open(file_path, 'r', encoding='utf-8') as file_line:
		for line in file_line:
			clean_line=line.strip()
			if clean_line:
				lines.append(clean_line)
	return lines

#拼接url
def join_url(url,word):
	url=url.rstrip('/')#去掉结尾的/
	word=word.lstrip('/')#去掉开头的/
	url_all=url+'/'+word
	return url_all

#根据完整的url获取网页内容返回status_code
def fetch_data(url_all):
	response = requests.get(url_all,headers=header,timeout=5)
	return response.status_code

if __name__ == '__main__':
	for i in read_files(path):
		url_all=join_url(url,i)
		status_code=fetch_data(url_all)
		if status_code==200:
			print(f'[+] Found: {url_all} (Status Code: {status_code})')
		else:
			print(f'[-] Not Found: {url_all} (Status Code: {status_code})')

	