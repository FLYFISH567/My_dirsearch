# 简单访问链接后获取状态码
import requests 

def fetch_status_code(url):
	headers = {
		"User-Agent": (
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
			"AppleWebKit/537.36 (KHTML, like Gecko) "
			"Chrome/120 Safari/537.36"
		)
	}
	try:
		response = requests.get(url,headers=headers)
		return response.status_code
	except requests.exceptions.RequestException as e:
		print(f"An error occurred: {e}")
		return None

if __name__ == "__main__":
	url=input("请输入要访问的URL: ")
	status_code = fetch_status_code(url)
	if status_code is not None:
		print(f"{status_code}")