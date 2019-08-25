#-*- coding:utf-8 -*-
import urllib
import json

# values 关键字，输入和输出都是utf8编码
# appId:2001239
#appID和回传地址是绑定的。
#appId:12345  测试appid
# 线上地址：https://asrspcheck.xesv5.com
# 测试地址：10.90.29.60:12009


class SendAudio(object):
    # URL = 'http://asrspcheck.xueersi.com'#大海线上环境
    URL = 'http://asrspcheck.xesv5.com'
    def __init__(self,id,url,appId,keywords):
        self.id = id
        self.url = url
        self.appId = appId
        self.keywords = keywords

    def send_audio(self):

        values = {}
        values['id'] = self.id
        values['url'] = self.url
        values['appId'] = self.appId
        values['keywords'] = self.keywords

        headers = {'Content-Type': 'application/json'}  # 设置请求头 告诉服务器请求携带的是json格式的数据
        request = urllib.request.Request(url=self.URL, headers=headers,
                                         data=json.dumps(values).encode(encoding='UTF8'))  # 需要通过encode设置编码 要不会报错
        response = urllib.request.urlopen(request)  # 发送请求

        logInfo = response.read().decode()  # 读取对象 将返回的二进制数据转成string类型
        # print(logInfo)


        return logInfo

# if __name__ == "__main__":
#     id = "1234"
#     url = "http://47.92.95.216/monitor/bj.ali.12.4/20190730/20190730-204054_N00000022262__917071062572_cc-ali-0-1564490453.4147880.mp3"
#     appId = "12345"
#     keywords = []
#
#     sa = SendAudio(id, url, appId, keywords)
#     sa.send_audio()


# values = {
#     "id":"15644904534147880",
#     "url":"http://47.92.95.216/monitor/bj.ali.12.4/20190730/20190730-204054_N00000022262__917071062572_cc-ali-0-1564490453.4147880.mp3",
#     "appId":"12345",
#     "keywords": [
#         "奥数",
#         "小班",
#         "满分",
#         "都是"
#     ]
# }