#-*- coding:utf-8 -*-
import pymysql
import time
import pandas as pd
from utils.send_audio import SendAudio
from utils.logger import Logger

filename ='/home/mayanli/speechtext_11/log/run.log'
# filename = './speechtext_11/log/run.log'

log = Logger(filename, level='debug', when='D')

def get_clue_call_record(sql=None):
    """
    获得昨天所有的电话录音mp3
    具体信息见SQl语句
    测试限制十条信息
    :return:
    """

    # 打开数据库连接
    dbname = 'k12_cc'
    connect = pymysql.connect(host='10.100.8.240',  # 本机主机A的IP（必须是这个）
                              port=3306,
                              user='bigdata',
                              passwd='Zw6GOIkCUXWnZXbY4Eo57mqfR8wOWWnD',
                              db=dbname)  # 需要连接的数据库的名称

    # sql = """
    # select id, province,district,follow_author,`begin`,`end`,(`end`-`begin`) as time_skip,CONCAT(file_server,'/',record_file) as `address`
    # from k12_cc.clue_call_record
    # where state = 'dealing' and DATEDIFF(`begin`,NOW())=-1 -- 昨天
    # -- state = 'dealing' and SUBSTR(`begin`,1,10)>DATE_SUB(CURDATE(),INTERVAL 1 day)
    # -- state = 'dealing' and DATEDIFF(`begin`,NOW())=0 -- 今天
    # limit 10 """

    sql = """
    select id, province,district,follow_author,`begin`,`end`,(`end`-`begin`) as time_skip,CONCAT(file_server,'/',record_file) as `address`
    from k12_cc.clue_call_record
    where state = 'dealing' and DATEDIFF(`begin`,NOW())=-1 -- 昨天
    -- state = 'dealing' and SUBSTR(`begin`,1,10)>DATE_SUB(CURDATE(),INTERVAL 1 day)
    -- state = 'dealing' and DATEDIFF(`begin`,NOW())=0 -- 今天
    """

    df_call_record = pd.read_sql(sql, con=connect)

    connect.close()
    return df_call_record
    # 关闭数据库连接


def batch_send():

    """
    读取数据上发送MP3音频
    :return:
    """
    df_call_record = get_clue_call_record()
    id = df_call_record["id"].to_list()
    url = df_call_record["address"].to_list()
    dict = zip(id, url)
    # appId = "1001619"线上环境的appId
    appId = "12345"#测试环境的appId
    keywords = []

    for id, url in dict:

        time.sleep(1) #测试环境设置一下时间

        sa = SendAudio(id, url, appId, keywords)
        send_message = sa.__dict__
        log.logger.error(send_message)
        sa.send_audio()
        log.logger.error(sa.send_audio())