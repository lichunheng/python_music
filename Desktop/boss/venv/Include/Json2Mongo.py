import json

from pymongo import MongoClient


class Json2Mongo(object):
    def __init__(self):
        self.host = '192.168.75.129'
        self.port = 27017
        # 创建mongodb客户端
        self.client = MongoClient(self.host, self.port)
        # 创建数据库dialog
        self.db = self.client.qq_music
        # 创建集合scene
        self.collection = self.db.qq_music

    # 写入数据库
    def write_database(self):
        with open('C:\\Users\\lch\\Desktop\\json\\music', encoding='utf8') as f:
            i = 0
            while True:
                i += 1
                print(u'正在载入第%s行......' % i)
                try:
                    lines = f.readline()  # 使用逐行读取的方法
                    review_text = json.loads(lines)  # 解析每一行数据

                    print(review_text)
                    data = {
                        "singerName": review_text['singer_name'],
                        "songName": review_text['song_name'],
                        "subtitle": review_text['subtitle'],
                        "albumName": review_text['album_name'],
                        "singerId": review_text['singer_id'],
                        "singerMid": review_text['singer_mid'],
                        "songTimePublic": review_text['song_time_public'],
                        "songType": review_text['song_type'],
                        "language": review_text['language'],
                        "songId": review_text['song_id'],
                        "songMid": review_text['song_mid'],
                        "songUrl": review_text['song_url'],
                        "hotComments": review_text['hot_comments'],
                        "lyric": review_text['lyric']
                    }
                    myquery = {"songId": review_text['song_id']}  # 查询条件
                    self.collection.insert(data)  # 插入mogo数据
                except Exception as e:
                    print(str(e))
                    continue

    # 从数据库读取
    def read_datebase( self ):
        try:
            myquery = {"name": "qq_music"} # 查询条件
            scene_flow = self.collection.find(myquery)
            print(type(scene_flow))
            for x in scene_flow:
                print(type(x))
                print(x)
            print ('读取成功')
        except Exception as e:
            print (e)


if __name__ == '__main__':
    jm = Json2Mongo()
    jm.write_database()
