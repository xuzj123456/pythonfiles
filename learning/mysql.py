# coding=utf-8
import MySQLdb

# 获取连接
try:
    conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='password',
        db='news',
        port=3306,
        charset='utf8'
    )
    cursor = conn.cursor()

    # 新建表格
    # sql1 = "CREATE TABLE `news`(" \
    #        "  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
    #        " `name` VARCHAR(20) NOT NULL" \
    #        ");"
    # cursor.execute(sql1)

    # 插入数据
    sql2 = "INSERT INTO `news` (`name`) VALUE('张三');"
    cursor.execute(sql2)

    # 获取数据
    sql3 = "SELECT * FROM `news`;"
    cursor.execute(sql3)
    rest = cursor.fetchone()  # 选择第一条
    print(rest[0])

    conn.commit()

    # 关闭连接
    conn.close()

except MySQLdb.Error as e:
    print('Error:%s' % e)
