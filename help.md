# help for git

# 下载

git clone 项目地址

# 提交

1. 添加至缓存区

  git add . 

  git add help.py 

2. 添加备注

  git commit -m '备注'

3. 提交至仓库

  git push origin main(仓库路径)

# 删除
## 删除某个文件
1. 删除文件 

  git rm help.py

2. 删除文件夹
   git rm -r db

3. 查看缓存(可选)

  git status

4. 提交

  git commit -m '备注'

  git push origin main

# 其他
## 文件状态
运行 git status 可以随时查看文件的状态，帮助你了解哪些文件需要操作。
1. M
M 表示文件已被修改，但尚未提交到 Git 仓库。

2. U
U 表示文件未被 Git 跟踪（即文件是新创建的，尚未添加到暂存区）。

3. A
表示文件已被添加到暂存区，但尚未提交到仓库。

4. D
表示文件已被删除，并且删除操作已添加到暂存区。

5. R
表示文件已被重命名，并且重命名操作已添加到暂存区。

