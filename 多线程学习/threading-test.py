import threading
import time

def task(name,flag):
    for i in range(5):
        print(f"{name}{flag} is running {i}")
        time.sleep(1)

# 创建两个线程
t1 = threading.Thread(target=task, args=("Thread-1",'aaa'))
t2 = threading.Thread(target=task, args=("Thread-2",'bbb'))

# 启动线程
t1.start()
t2.start()

# 等待线程结束
t1.join()
t2.join()

print("All tasks done")
