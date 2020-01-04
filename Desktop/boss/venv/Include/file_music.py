# -*- coding: UTF-8 -*-

import json

import pymysql


# 读取review数据，并写入数据库
# 导入数据库成功，总共4736897条记录
def prem(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)  # 结果表明已经连接成功
    # cursor.execute("DROP TABLE IF EXISTS music")  # 习惯性
    # sql = """CREATE TABLE music (
    #    id INT(11) PRIMARY KEY AUTO_INCREMENT,
    #    singer_name VARCHAR(100),
    #    song_name VARCHAR(100),
    #    subtitle VARCHAR(100),
    #    album_name VARCHAR(100),
    #    singer_id VARCHAR(100) NOT NULL,
    #    singer_mid VARCHAR(100),
    #    song_time_public VARCHAR(30) DEFAULT NULL,
    #    song_type INT(4),
    #    language INT(4),
    #    song_id INT(11) NOT NULL,
    #    song_mid VARCHAR(100),
    #    song_url VARCHAR(300),
    #    hot_comments VARCHAR(10000),
    #    lyric VARCHAR(2000))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
    # cursor.execute(sql)  # 根据需要创建一个表格


def reviewdata_insert(db):
    with open('C:\\Users\\lch\\Desktop\\json\\music', encoding='utf8') as f:
        i = 0
        while True:
            i += 1
            print(u'正在载入第%s行......' % i)
            try:
                lines = f.readline()  # 使用逐行读取的方法
                review_text = json.loads(lines)  # 解析每一行数据
                result = []
                result.append((str(review_text['singer_name']), review_text['song_name'], review_text['subtitle'],
                               review_text['album_name'], str(review_text['singer_id']), str(review_text['singer_mid']),
                               review_text['song_time_public'], review_text['song_type'], review_text['language'],
                               review_text['song_id'], review_text['song_mid'], review_text['song_url'],
                               str(review_text['hot_comments']), review_text['lyric']))

                print(result)
                songId = review_text['song_id']
                # 插入数据库之前先查询数据是否重复

                print("打印song_id数据：", songId)
                select_sql = "select * from music where song_id = %s" %(songId)
                cursor = db.cursor()
                cursor.execute(select_sql)
                res = cursor.fetchone()
                db.commit()
                print("查询数据：", res)
                if res == songId:
                    continue

                # 插入数据
                inesrt_re = "insert into music(singer_name, " \
                            "song_name, " \
                            "subtitle, " \
                            "album_name, " \
                            "singer_id, " \
                            "singer_mid, " \
                            "song_time_public, " \
                            "song_type," \
                            "language, " \
                            "song_id, " \
                            "song_mid, " \
                            "song_url," \
                            "hot_comments," \
                            "lyric)" \
                            " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor = db.cursor()
                cursor.executemany(inesrt_re, result)
                db.commit()
            except Exception as e:
                db.rollback()
                print(str(e))
                continue


if __name__ == "__main__":  # 起到一个初始化或者调用函数的作用
    db = pymysql.connect("192.168.75.129", "root", "123456", "qq_music", charset='utf8mb4')
    cursor = db.cursor()
    prem(db)
    reviewdata_insert(db)
    cursor.close()
