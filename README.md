# Tai-database-merge
这是一个能够合并[Tai👻在Windows上统计软件使用时长的软件](https://github.com/Planshit/Tai)的数据库的脚本。
## 使用方法
1. 将两个`data.db`文件**的副本**改为不同名字后放入.py脚本同目录下
2. 更改脚本第2-4行：
```py
OLDDB = 'data3.db'  # 此处为更老的数据库名
NEWDB = 'data2.db'  # 此处为更新的数据库名
outdb = 'data.db'  # 导出的数据库名字
```
* 实际上，`OLDDB` 与 `NEWDB`混用并不影响数据库记录的正确性。
3. 当前目录下执行脚本
## 运行环境
python3
## 注意事项
* 数据无价，请使用数据库副本进行合并
* 脚本不包含 `分类` 数据的合并
* 理论上支持 1.0.0.2 <= `data.db.version` <= 1.0.* 的数据库的合并。如需合并更新的数据库，请在Issues中反馈。
