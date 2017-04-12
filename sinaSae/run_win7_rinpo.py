import itchatmp
import random
import requests
import os
from tornado import gen
import time

KEYS = ['241b5a1059b04c898d00d197522a917c', 'ca6acaabfd7a40edb0b42a7bea233dc7', '85c0d048714b43e6bed1b0c966c20cbe']
word_faces = ["✪ω✪", '٩(●̮̮̃●̃)۶ ٩(•̮̮̃•̃)۶ ٩(-̮̮̃-̃)۶ ٩(●̮̮̃•̃)۶ ٩(-̮̮̃•̃)۶ ٩(×̯×)۶ ٩͡[๏̯͡๏]۶', '✷(ꇐ‿ꇐ)✷',
              '┗|｀O′|┛ 嗷~~', '...φ(0￣*)啦啦啦_φ(*￣0￣)′ ', '咳咳＞＜', 'ˋ( ° ▽、° ) ',
              '§(*￣▽￣*)§', '( `０‘)ノ~~~~~~~~~ν ', 'o(′益`)o', '(*￣︿￣) ', '...:.;::..;::: .:.;::….;:￣)…:.;:□￣)(￣□￣*)复活',
              '(=゜ω゜)ノぃょぅ', '(寒￣ii￣)彡…彡…彡 ', '|(*′口`) ', 'こヾ(＾ｏ＾*)ん(ｏ＾^)ｏにｏ(＾０＾ｏ)ち(ｏ＾.＾)ノ" は ヾ(＊＾〇＾＊)ノ" ',
              'ヾ(′▽｀*)ゝ', '3=(-_-メ)', '...(*￣０￣)ノ', '||Φ|(|T|Д|T|)|Φ|| ', '(*￣3￣)╭', 'φ(゜▽゜*)?', '（*＾-＾*）',
              '(o゜▽゜)o☆[好主意!] ', '【】\(·ω·`)o ', 'o(*￣▽￣*)ゞ ', '（￣。。￣）[河马] ', '(_　_)。゜zｚＺ ',
              '[火箭筒，发射！](*￣皿￣)=Σ口＞=Σ口＞=Σ口＞ ',
              '(￣～￣) 嚼！', '(o^^)oo(^^o) ']


# 当前目录
def get_current_dir():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    # print("当前目录：",file_dir)
    return file_dir


# 表情列表
def get_faces_list():
    face_path = os.path.join(get_current_dir(), "faces")
    if os.path.exists(face_path):
        faces_list = os.listdir(face_path)
        # print("表情列表：",faces_list)
        return [os.path.join(face_path, i) for i in faces_list]
    else:
        return


def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': random.choice(KEYS),
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:

        r = requests.post(apiUrl, data=data).json()

        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常

    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return
    if not r['code'] in (100000, 200000, 302000, 308000, 313000, 314000): return
    if r['code'] == 100000:  # 文本类
        return '\n'.join([r['text'].replace('<br>', '\n')])
    elif r['code'] == 200000:  # 链接类
        return '\n'.join([r['text'].replace('<br>', '\n'), r['url']])
    elif r['code'] == 302000:  # 新闻类

        l = [r['text'].replace('<br>', '\n')]
        for n in r['list'][0:10]: l.append('%s - %s' % (n['article'], n['detailurl']))

        return '\n'.join(l)
    elif r['code'] == 308000:  # 菜谱类
        l = [r['text'].replace('<br>', '\n')]
        for n in r['list']: l.append('%s - %s' % (n['name'], n['detailurl']))

        return '\n'.join(l)
    elif r['code'] == 313000:  # 儿歌类
        return '\n'.join([r['text'].replace('<br>', '\n')])
    elif r['code'] == 314000:  # 诗词类
        return '\n'.join([r['text'].replace('<br>', '\n')])


def pictureReply():
    face_word = random.choice(word_faces)
    return face_word


itchatmp.update_config(itchatmp.WechatConfig(
    token='squirrel',
    appId='wx28cd73c327454d59',
    appSecret='f740cea1c5027526c56ead4eb12814db'))


@itchatmp.msg_register(itchatmp.content.INCOME_MSG)
def text_reply(msg):
    # print(msg)
    # 设置延迟回复
    time.sleep(0.2)
    if msg["MsgType"] == "text":
        if msg["Content"] == u'【收到不支持的消息类型，暂无法显示】':
            # 图片回复
            reply = pictureReply()
        else:
            reply = get_response(msg["Content"])
        return reply
    if msg["MsgType"] == "image":
        reply = pictureReply()
        return reply
    if msg["MsgType"] == "event":
        # print("hhh")
        if msg["Event"] == "subscribe":
            # print("关注")
            reply ='''
         welcome to squirrel
功能介绍：
    具备聊天、 笑话、 图片 、天气 、 问答、 百科 、故事 、 新闻、  菜谱 、星座 、 吉凶 、 计算、  快递 、 飞机、  列车、 成语接龙等功能

author：squirrel
weixin: qht131427
            '''
            return reply
        if msg["Event"] == "unsubscribe":
            # print("取消关注")
            return
        else:
            return
    else:
        return


itchatmp.run()
