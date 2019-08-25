#-*- coding:utf-8 -*-
from flask import Flask, request
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
import time
import sys
sys.path.append('../')
from utils.parse import *
app = Flask(__name__)

# 只接受POST方法访问
@app.route("/speechtext_11", methods=["POST"])
def check():
    # 默认返回内容
    # return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    return_dict = {"stat": 1, "message": "success"}
    # 判断入参是否为空
    if request.get_data() is None:
        return_dict['stat'] = '0'
        return_dict['message'] = 'download error'
        # return_dict['message'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data, encoding='utf-8')

    # 将结果保存到es
    save_result_to_es(get_Data)

    # 将结果存入本地
    path = "../speechtext_11/post_result.json"
    with open(path, 'a', encoding='utf-8') as json_file:
        json.dump(get_Data, json_file, ensure_ascii=False)

    # #获得请求失败的音频id，重新发送
    # if get_Data['stat'] == 0:
    #     id_list = []
    #     id_list.append(get_Data['id'])

    return json.dumps(return_dict, ensure_ascii=False)


def save_result_to_es(get_Data):
    """
    :param dict: 将返回json数据，解析出文本，关键字提取
    :return: 存入ES
    """
    es = Elasticsearch(['127.0.0.1'], port=9200)

    es = Elasticsearch(
        ['es-cn-0pp165u620001xs3r.elasticsearch.aliyuncs.com'],
        http_auth=('elastic', 'Z6NTRPAjYZlrGCW1'),
        port=9200
    )

    if get_Data["stat"] == 1:

        #解析文本
        left_text, right_text, dialogue_text = get_left_right_dialogue_text(get_Data)

        #清洗解析文本

        left_text_clear = clear_stop_word(left_text)
        right_text_clear = clear_stop_word(right_text)
        dialogue_text_clear = clear_stop_word(dialogue_text)

        #提取关键字
        left_keyword = get_keyword_tr4k(left_text_clear)
        right_keyword = get_keyword_tr4k(right_text_clear)
        dialogue_keyword = get_keyword_tr4k(dialogue_text_clear)




        #涉及学科年级
        left_text_grade, left_text_subject = involve_grade_subject(left_text_clear)
        right_text_grade, right_text_subject = involve_grade_subject(right_text_clear)
        dialogue_text_grade, dialogue_text_subject = involve_grade_subject(dialogue_text_clear)

        #统计左右声道有效沟通次数、沟通时间
        left_effective_count, right_effective_count,left_effective_time,right_effective_time = \
            get_left_right_effective_statistical(get_Data)

        result = {
            "original_return_text": get_Data,
            "parses_text":
                {
                    "parses_left_channel_text": left_text,
                    "parses_right_channel_text": right_text,
                    "parses_left_right_channel_text": dialogue_text
                },

            "keyword":
                {
                    "left_channel_keyword": left_keyword,
                    "right_channel_keyword": right_keyword,
                    "right_left_channel_keywords": dialogue_keyword
                },
            "involve":
                {
                    "left_channel_involve_grade": left_text_grade,
                    "left_channel_involve_subject": left_text_subject,
                    "right_channel_involve_grade": right_text_grade,
                    "right_channel_involve_subject ": right_text_subject,
                    "dialogue_involve_grade": dialogue_text_grade,
                    "dialogue_involve_subject": dialogue_text_subject
                },
            "effective_statistical ":
                {
                    "left_channel_effective_count": left_effective_count,
                    "left_channel_effective_time": left_effective_time,
                    "right_channel_effective_count": right_effective_count,
                    "right_channel_effective_time": right_effective_time
                },

            "dt": time.strftime("%Y%m%d")
        }

        es.index(index="speech_text", doc_type="doc", id=get_Data['id'], body=result)
    else:
        result = {}
        result["original_return_text"] = get_Data

        es.index(index="speech_text", doc_type="doc", id=get_Data['id'], body=result)




if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='10.29.48.92', port=5000)#本地
    #http://10.29.48.92:5000/speechtex
    # app.run(host='0.0.0.0', port=5000)#测试环境
