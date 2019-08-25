#-*- coding:utf-8 -*-
import json
import os
import pandas
import codecs
import glob
import pandas as pd
from jieba import analyse
from snownlp import SnowNLP
from textrank4zh import TextRank4Keyword, TextRank4Sentence
# from pyltp import Segmentor
import jieba.posseg as pseg

import re
import jieba

def get_left_right_dialogue_text(get_Data):

    """
    :param get_Data: 返回音频文本结果，类型是dict
    :return: 左声道语音文本、右声道语音文本、左右声道合成文本
    """
    left_text = []
    right_text = []
    dialogue_text = []

    for i in get_Data['text']:
        dialogue_text.append(i['word'])

        if i['type'] == 'left':
            left_text.append(i['word'])
        elif i['type'] == 'right':
            right_text.append(i['word'])
    return ''.join(left_text), ''.join(right_text), ''.join(dialogue_text)


def clear_stop_word(text):
    '''
    去除文里面的停用词，再合并

    '''
    stopwords = [line.rstrip() for line in
                 open('/Users/mayanli/Work/text_mining/stop_words_defined.txt', 'r', encoding='GBK').readlines()]

    #     使用jieba
    segs = jieba.cut(text, cut_all=False)
    #     使用pyltp
    # LTP_DATA_DIR = '/Users/mayanli/git_dir/pyltp/ltp_data'
    # cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    # segmentor = Segmentor()
    # segmentor.load(cws_model_path)
    # segs = segmentor.segment(text)

    final = ''
    for seg in segs:
        if seg not in stopwords:
            final += seg

    final = re.sub('[。]+', '。', final)  # 处理文本重复符号的表达，如替换多个。！.
    final = re.sub('\n', '', final)
    #     print(final)
    return final


def get_keyword_tfidf(content):
    tfidf = analyse.extract_tags
    keywords = tfidf(content)
    #     # 输出抽取出的关键词
    #     KeyWord =[]
    #     for keyword in keywords:
    #          KeyWord.append(keyword)
    #     return KeyWord

    return '、'.join(keywords)


def get_keyword_tr4k(text):
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

    KeyWord = []
    for item in tr4w.get_keywords(20, word_min_len=2):  # 20个关键词且每个的长度最小为2
        # #         print(item.word, item.weight)
        KeyWord.append(item.word)
    # return '、'.join(KeyWord)
    return KeyWord


def get_keyword_tr4k_3(text):
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

    KeyWord = []
    for item in tr4w.get_keywords(20, word_min_len=3):  # 20个关键词且每个的长度最小为1
        # #         print(item.word, item.weight)
        KeyWord.append(item.word)
    # return '、'.join(KeyWord)
    return KeyWord


def get_keyword_tr4k_4(text):
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

    KeyWord = []
    for item in tr4w.get_keywords(20, word_min_len=4):  # 20个关键词且每个的长度最小为1
        # #         print(item.word, item.weight)
        KeyWord.append(item.word)
    # return '、'.join(KeyWord)
    return KeyWord


def get_left_right_effective_statistical(get_Data, interval=1):

    """

    :param get_Data: 返回json数据,默认大于1秒时常的语言时常记为有效。
    :return: 左声道有效沟通次数、左声道有效沟通时常、右声道有效沟通次数、右声道有效沟通时常
    """

    left_effective_count = 0
    right_effective_count = 0
    left_effective_time = 0
    right_effective_time = 0

    for i in get_Data['text']:

        if i['type'] == 'left':
            left_long = float(i["end"]) - float(i["start"])
            if left_long > interval:
                left_effective_time += left_long
                left_effective_count += 1
        elif i['type'] == 'right':
            right_long = float(i["end"]) - float(i["start"])
            if right_long > interval:
                right_effective_time += right_long
                right_effective_count += 1
    effective_statistical = (left_effective_count, right_effective_count, round(left_effective_time, 2), round(right_effective_time, 2))
    return effective_statistical




def get_flag(text):
    '''
    获得文本的词性标记：n、t
    '''
    words =pseg.cut(text)
    t = []
    n = []
    for w in words:
    #     if w.flag == 'n' or w.flag == 't':
    #         print(w.word,w.flag)
        if w.flag == 't':
    #         print(w.word)
            t.append(w.word)
        if w.flag == 'n':
            n.append(w.word)
    return set(t), set(n)


def involve_grade_subject(text):

    '''
    话题涉及年级、科目
    :param text:
    :return:
    '''
    # text = clear_stop_word(text)#对文本进行清洗
    t, n = get_flag(text)
    grade_list = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级', '七年级', '八年级', '九年级', '初一', '初二', '初三', '高一', '高二', '高三']
    subject_list = ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理']
    grade = list(set(t).intersection(grade_list))
    subject = list(set(n).intersection(subject_list))

    # return '、'.join(grade), '、'.join(subject)
    return grade, subject



