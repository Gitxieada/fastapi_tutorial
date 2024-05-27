import sqlite3

connection = sqlite3.connect('test.db')
# 创建游标
cursor = connection.cursor()
# 创建表
cursor.execute('''CREATE TABLE user
       (id INT PRIMARY KEY     NOT NULL,
       username           TEXT    NOT NULL,
       password            TEXT     NOT NULL);''')
# 数据保存
cursor.execute("INSERT INTO user (id,username,password) VALUES (1, 'xiaozhong', '123456')")
cursor.execute("INSERT INTO user (id,username,password) VALUES (2, 'muyu', '123456')")
# 数据查询
cursor = cursor.execute("SELECT id, username, password from user")
for row in cursor:
    print(row)
connection.commit()
# 数据更新
cursor.execute("UPDATE user set username ='xiaoxiao' where id = 1")
connection.commit()
# 数据删除
cursor.execute("DELETE from user where id=1;")
connection.commit()
# 关闭数据库连接
connection.close()
