# -*- coding: UTF-8 -*-

import requests
import json
import time
import random

def get_Disstid(url):
    headers={
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Referer":"https://y.qq.com/portal/playlist.html",
        "Host":"c.y.qq.com"
    }
# 1访问入口得到音乐列表的disstid
    res = requests.get(url,headers=headers).text
    re=res.strip("getPlaylist()")
    r=json.loads(re)
    for x in r["data"]["list"]:
        # 用得到的dissid进行拼接得到新的url
        sub_url = " https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid={0}&format=jsonp&g_tk=5381&jsonpCallback=playlistinfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0".format(x["dissid"])
# 2访问音乐分类，得到歌单的songmid，songname
        headers["referer"]="https://y.qq.com/n/yqq/playsquare/{0}.html".format(x["dissid"])
        res = requests.get(sub_url, headers=headers).text
        re = res.strip("playlistinfoCallback()")
        r = json.loads(re)
        for x in r["cdlist"][0]["songlist"]:
            songmid = x["songmid"]
            songname = "C400{0}.m4a".format(songmid)
            song = x["songname"]
            key_url = "https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback20480960151150063&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback20480960151150063&uin=0&songmid={0}&filename={1}&guid=9602668140".format(
                songmid, songname)
# 3.访问播放页面，得到每首歌的vkey
            headers["Referer"] = "https://y.qq.com/portal/player.html"
            res = requests.get(key_url, headers=headers).text
            re = res.strip("MusicJsonCallback20480960151150063()")
            r = json.loads(re)
            for x in r["data"]["items"]:
                vkey = x["vkey"]
                song_url = "http://dl.stream.qqmusic.qq.com/{0}?vkey={1}&guid=9602668140&uin=0&fromtag=66".format(
                    songname, vkey)
# 4.访问音乐文件下载
                headers["Host"]="dl.stream.qqmusic.qq.com"
                del headers["Referer"]
                res=requests.get(song_url,headers=headers,stream=True)
                filename = "C:\\Users\\lch\\Desktop\\song\\{0}.m4a".format(song)
                print(song)
                with open(filename,"wb") as f:
                    f.write(res.raw.read())


if __name__ == '__main__':
    sin = 0
    ein = 29
    sum = 5620
    while True:
        url="https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.7709971027608087&g_tk=5381&jsonpCallback=getPlaylist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin={0}&ein={1}".format(sin,ein)
        sub_url_list=get_Disstid(url)
        if ein<5620:
            sub_url_list = get_Disstid(url)
            sin+=30
            ein+=30
        else:
            break
        time.sleep(1)
        span = round(random.random() * 6, 1)
        time.sleep(span)