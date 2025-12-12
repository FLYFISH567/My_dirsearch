# My_dirsearch 项目开发指南

## 项目概述
这是一个从零搭建的目录扫描工具（dirsearch），用于学习 Python 多线程和 HTTP 请求处理。项目采用 MVP 迭代开发模式，从单线程逐步演进到多线程实现。

## 核心架构

### 目录结构
- **MVP/** - 生产版本的主要实现
  - `MVP.py` - 单线程基础版本
  - `多线程MVP.py` - 多线程优化版本（推荐使用）
- **多线程学习/** - 多线程技术的学习和实验代码
- **request学习/** - requests 库的学习示例
- **db/** - 数据文件存储
  - `dicc.txt` - 目录扫描字典（主字典）
  - `*_blacklist.txt` - 各种状态码的黑名单
  - `user-agents.txt` - User-Agent 列表

### 项目演进路径
1. **MVP.py** - 单线程版本，顺序扫描 URL
2. **MVP_time.py** - 添加性能计时功能
3. **多线程MVP.py** - 使用 threading + queue 实现并发扫描（当前最佳实践）

## 关键模式和约定

### 1. URL 处理模式
项目使用统一的 URL 拼接函数，防止双斜杠问题：
```python
def join_url(base, word):
    return base.rstrip('/') + '/' + word.lstrip('/')
```
- 所有 URL 拼接必须使用此函数
- 确保基础 URL 和路径词条都正确处理斜杠

### 2. 多线程架构（生产者-消费者模式）
使用 `queue.Queue` + `threading.Thread` 实现线程池：
```python
q = queue.Queue()
num_threads = 60  # 默认 60 个工作线程
```
- **生产者**: 主线程读取字典文件并将任务放入队列
- **消费者**: 工作线程从队列获取任务并执行 HTTP 请求
- **终止信号**: 使用 `None` 作为毒丸（poison pill）优雅退出

### 3. 线程安全计数器
使用锁保护共享状态：
```python
counter_lock = threading.Lock()
with counter_lock:
    counter += 1
```
- 所有全局计数器操作必须加锁
- 每 100 个 URL 输出一次进度信息

### 4. HTTP 请求规范
- **超时**: 所有请求设置 5 秒超时 `timeout=5`
- **User-Agent**: 使用通用浏览器 UA 避免被屏蔽
- **异常处理**: fetch_data 函数捕获所有异常返回 None
- **状态码判断**: 200 表示发现，其他状态打印但不视为成功

### 5. 文件读取模式
字典文件按行读取，自动清理空白：
```python
def read_files(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            clean = line.strip()
            if clean:
                lines.append(clean)
    return lines
```
- 使用 UTF-8 编码
- 过滤空行和空白行
- 相对路径从脚本所在目录计算（如 `../db/dicc.txt`）

## 开发工作流

### 运行主程序
```bash
# 运行多线程版本（推荐）
python MVP/多线程MVP.py

# 运行单线程版本（用于对比测试）
python MVP/MVP.py
```

### 测试学习代码
```bash
# 测试多线程基础功能
python 多线程学习/threading-test.py

# 测试 HTTP 请求
python request学习/Test1.py
```

### Git 工作流
项目包含 [help.md](help.md) 作为 Git 命令快速参考：
- `git add .` - 添加所有文件
- `git commit -m '备注'` - 提交变更
- `git push origin main` - 推送到主分支

## 性能基准
- **单线程**: 顺序扫描，每个请求阻塞
- **多线程 (60 线程)**: 并发扫描，显著提升速度
- 进度报告: 每 100 个 URL 打印一次统计信息

## 注意事项
1. **相对路径**: 所有文件路径使用相对于脚本的 `../db/` 格式
2. **中文支持**: 文件名和注释使用中文，字符串使用 UTF-8 编码
3. **学习项目**: 代码强调可读性和学习价值，不追求生产级别的错误处理
4. **URL 验证**: 当前仅检查状态码 200，未来可扩展黑名单过滤逻辑
