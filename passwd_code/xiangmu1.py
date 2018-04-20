# 1.安装pip pip install redis

# 2.连接mysql

# 3.连接redis
#     import redis
#     redis.Redis()

# 4.获取姓名密码参数
#     python xxx.py argv1 argv2
#     import sys
#     sys.argv[1]

# 5.访问redis，判断输入的姓名和密码和redis中保存的是否匹配

# 6.和redis不匹配，则查询mysql，select操作

# 7.mysql有查询结果的话，则更新到redis中,反之则没有该用户

# -*- coding:utf-8 -*-

import sys
import pymysql
import redis

def con_mysql(sql):
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        db='xiangmu1',
        port=3306,
        charset='utf8')
    cursor=db.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    db.close()
    return data

def con_redis(name,passwd):
    r = redis.Redis(host='120.77.177.113',port=6379,password='123456')
    # r_name = r.hgetall('user')
    r_name = r.hget('user','name')
    r_passwd = r.hget('user','passwd')
    r_name = r_name.decode('utf8')
    r_passwd = r_passwd.decode('utf8')
    if name == r_name and passwd == r_passwd:
        return True, '登录成功'
    else:
        return False, '登录失败'


if __name__ == '__main__':
    #获取传入的姓名和密码参数
    name = sys.argv[1]
    passwd = sys.argv[2]
    #传入redis中，进行校验
    result = con_redis(name,passwd)
    if not result[0]:
        # 查询mysql数据库
        sql = '''select * from people where name="%s" and passwd="%s"''' % (name,passwd)
        data = con_mysql(sql)
        if data:
            r = redis.Redis(host='120.77.177.113', port=6379, password='123456')
            r.hset('user','name',name)
            r.hset('user','passwd',passwd)
            print('刷新redis.登录成功')
        else:
            print('用户名和密码错误')
    else:
        print('redis中数据正确，登录成功')