import threading
import queue
import requests
import time

url = 'https://www.baidu.com'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
path = '../db/dicc.txt'

def read_files(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            clean = line.strip()
            if clean:
                lines.append(clean)
    return lines

def join_url(base, word):
    return base.rstrip('/') + '/' + word.lstrip('/')

def fetch_data(url_all):
    try:
        response = requests.get(url_all, headers=header, timeout=5)
        return response.status_code
    except:
        return None


# 全局计数器和锁
counter = 0
counter_lock = threading.Lock()
start_time = time.time()


# ------------------------
#   Worker
# ------------------------
def worker(q):
    global counter

    while True:
        word = q.get()
        if word is None:
            break

        url_all = join_url(url, word)
        status_code = fetch_data(url_all)

        # 打印结果
        if status_code == 200:
            print(f"[+] Found: {url_all} (Status: {status_code})")
        else:
            print(f"[-] Not Found: {url_all} (Status: {status_code})")

        # --- 计数部分 ---
        with counter_lock:
            counter += 1
            if counter % 100 == 0:
                spent = time.time() - start_time
                print(f"\n=== 已扫描 {counter} 个 URL，耗时 {spent:.2f} 秒 ===\n")

        q.task_done()


if __name__ == "__main__":
    q = queue.Queue()
    num_threads = 60

    # 启动线程
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(q,))
        t.start()
        threads.append(t)

    # 主线程添加任务
    for word in read_files(path):
        q.put(word)

    q.join()

    # 发结束信号
    for _ in range(num_threads):
        q.put(None)

    for t in threads:
        t.join()

    # 总耗时
    total_time = time.time() - start_time
    print(f"\n✨ 扫描完成，总共扫描 {counter} 个 URL，总耗时 {total_time:.2f} 秒 ✨")
