# -*- coding:utf-8 -*-
import itchat
from itchat.content import *
import requests
import os
import random
import threading
import time
import datetime
import json
import logging
import pytz

tz = pytz.timezone('Asia/Shanghai')

from flask import Flask, make_response


# todo 备注名 进行设置
# todo 固定文件读取
def start_flask():
    flaskApp = Flask('itchat')

    @flaskApp.route('/')
    def return_qr():
        if len(qrSource) < 100:
            return qrSource
        else:
            response = make_response(qrSource)
            response.headers['Content-Type'] = 'image/jpeg'
            return response

    flaskApp.run(host="0.0.0.0")
    # flaskApp.run()


def qrCallback(uuid, status, qrcode):
    if status == '0':
        global qrSource
        qrSource = qrcode
        # print(qrSource)
    elif status == '200':
        qrSource = 'Logged in!'
    elif status == '201':
        qrSource = 'Confirm'

def ec():
    print("机器人退出时间：{}".format(datetime.datetime.now(tz)))
    #todo 退出报警

def start_falsk():
    flaskThread = threading.Thread(target=start_flask)
    flaskThread.setDaemon(True)
    flaskThread.start()


def valid_time():
    exe_date = "2017-06-10 00:00:00"
    exe_time = datetime.datetime.strptime(exe_date, "%Y-%m-%d %H:%M:%S")
    # print(exe_time)
    now_time = datetime.datetime.now(tz)
    if exe_time > now_time:
        print("剩余体验时间 {}天".format((exe_time - now_time).days))
        return True


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


# 配置文件路径
def get_cfg_path():
    current_path = get_current_dir()
    file_path = os.path.join(current_path, "config.json")
    return file_path


# 读取配置
def get_config():
    file_path = get_cfg_path()
    if os.path.exists(file_path):
        with open(file_path, encoding='utf8') as f:
            result = json.loads(f.read())
        return result


# 写入配置
def write_config(data):
    if os.path.exists(get_cfg_path()):
        data = {"safe_friends": data["safe_friends"], "Flag": data["Flag"], "master": data["master"]}
        file_path = get_cfg_path()
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False))
        return True


# 机器人默认配置
chat_config = {
    "safe_groups": [],  # 群白名单
    # "safe_groups": [],  # 群白名单
    "safe_friends": [],  # 好友白名单
    # "safe_friends": ["ht",],  # 好友白名单
    # "safe_friends": ["ht","❇琪琪🌴👙"],  # 好友白名单

    "list_group": [],  # 群列表
    "list_friend": [],  # 好友列表


    "groups_dict": {},  # 群关系字典 name：id  # "nameId":{},"idName":{},"Flag":False
    "friends_dict": {},  # 好友关系字典

    "op_groups_dict": {},  # id：name
    "op_friends_dict": {},
    "master": "",
    "Flag": {},

}
# 2016.12.4
wish_List = ["把酒当歌歌盛世，闻鸡起舞舞新春",
             "金鸡唤出扶桑日，锦犬迎来大地春",
             "金猴留恋丰收年，彩凤欢啼盛世春",
             "鸡鸣喜报丰收果，犬吠欣迎富贵宾",
             "鸡描竹叶三中颂，犬绘梅花五福临",
             "猴奋已教千户乐，鸡鸣又报万家春",
             "鸡报小康随日出，年迎大有伴春来",
             "红日升空辉大道，金鸡报晓促长征",
             "金鸡一唱传佳讯，玉犬三呼报福音",
             "鸡鸣晓日江山丽，犬吠神州岁月新",
             # "鸡年未到，祝福先行。鸡年期盼你：天天开心!",
             "金猴举棒驱走千年旧俗,雄鸡报春迎来一代新风。",
             "猴岁呈祥长空五光十色,鸡年纳福大地万紫千红。",
             "猴岁呈祥，长空五光十色;鸡年纳福，大地万紫千红。",
             "除夕猴在山，重享齐天乐;迎春鸡报晓，高唱东方红。",
             "彩凤高翔恋我中华春不老;金鸡喜唱歌斯盛世乐无穷。",
             "大鹏展翅雄视天下唯我独尊，金鸡独立傲视群英我行我素。",
             "振翅欲冲霄，一唱雄鸡声破晓;迎春思试剑，三擂战鼓气吞虹。",
             "万象喜回春，守信知廉标五德;一元欣复始，司晨报午必三鸣。",
             "九域涌新潮，四海雄鸡争唱晓;三春辉紫气，八方彩凤共朝阳。",
             "鸡鸣早看天，抓住时机求发展;水近先得月，紧跟形势上台阶。",
             "鸡鸣曙日红，万里金光辉瑞霭;柳舞春江绿，千重锦浪映丹霞。",
             "鸡年发大财行大运!身体健康，万事如意!一年伊始，福寿即来。",
             "今年好时辰，群鸡来报喜;春伊花复开，君亦临其景;祝君年年旺，团团又圆圆。",
             "春节捎去我温暖如春的问候，祝您拥有幸福甜美的鸡年。鸡年行好运，万事遂心愿!",
             "古人都扫尘过年，愿你也扫去心中一年的风尘，在新春佳节的时候，祝你一年都开心!",
             "这一刻有我最深的思念。让云捎去满心的祝福，点缀你甜蜜的梦。愿你拥有一个幸福快乐的鸡年!",
             "祝你鸡年财源滚滚，发得像肥猪;身体壮得像狗熊;爱情甜得像蜜蜂;好运多得像牛毛;事业蒸蒸像大鹏。",
             "给你个节日就快乐，给你点阳光就灿烂，给你些问候就温暖，给你顶高帽就发飘。祝鸡年心怡，鸡年大吉!",
             "愿幸福伴你走过每一天;愿快乐随你渡过每一天;愿平安同你穿越每一天;愿祝福和你飞越每一天;祝鸡年快乐!",
             "鸿运滚滚来，四季都发财。鸡年好事多，幸福喜颜开。步步再高升，事事顺着来。老友多联系，莫将我忘怀!",
             "鸡年到了，给你鸡情的祝福。愿你的生活鸡极向上，能把握每个发财的鸡会。把鸡肤保养得青春焕发。事业生鸡勃勃，要记得经常联系哦，不许总关鸡!",
             "吉年好，得鸡宝;出众貌，没得挑;命途好，才气高;合家欢，父母好;祝福到，盼美好，愿您合家多欢乐，平平安安多财宝!",
             "鸡年祝愿天下朋友：工作舒心，薪水合心，被窝暖心，朋友知心，爱人同心，一切都顺心，永远都开心，事事都称心!",
             "祝你鸡年：好事都成双，出门最风光，天下你为王，赛过秦始皇;人人都捧你的场，自己吃肉人喝汤，钞票直往口袋装。",
             "公鸡神采奕奕，带来平安如意;母鸡勤劳美丽，下个金蛋给你;小鸡活泼淘气，挥洒欢乐满地;电话传情达意，祝你鸡年大吉!",
             "鸡年到，喜事到，大喜，小喜都是喜，鸡年到，快乐到，左乐。右乐真是乐。鸡年到，锣鼓敲，鞭炮响。鸡子鸡女一起来报道!",
             '''日给你温暖;
             月给你温馨;
             星给你浪漫;
             雨给你滋润;
             我给你祝福。送一份美丽让你欢笑，送一份开心让你不老，祝你春节快乐!!''',
             "祝你：位高权重责任轻，事少钱多离家近，每天睡到自然醒，别人加班你加薪，领钱数得手抽筋，靓女爱你发神经。鸡年大吉祥!",
             '''鸡年佳节到，向你问个好，身体倍健康，心情特别好;
             好运天天交，口味顿顿妙。最后祝您：鸡年好运挡不住，鸡年财源滚滚来!''',
             "春节到了，送你一个饺子。平安皮儿包着如意馅，用真情煮熟，吃一口快乐两口幸福三口顺利然后喝全家健康汤，回味是温馨，余香是祝福。",
             "鸡年将至，为了地球环境与资源，请减少购买传统纸制贺卡，你可在大面值人民币上用铅笔填上贺词，寄给我!感谢你对环保事业的支持!祝你幸福快乐!",
             "烟花绽放的是灿烂的希望，星光闪烁的是幸福的光芒，对联书写的是心中的梦想，彩虹铺就的是美丽的天堂，短信传递的是鸡年的吉祥。愿你万事如意!",
             " 锣鼓敲，欢声笑，福星照，舞狮闹，祝福速速来报到。新的一年，希望你财富贼多，事业贼火，身体贼棒，家庭贼旺，一切贼顺，鸡年贼牛!",
             "鞭炮声声唱响了春节的喜乐年华，各族人民传统大节的烟花盛开。龙的传人舞狮挥龙庆贺鸡年的到来，秧歌高跷舞出了全国人民心中的喜悦，幸福美满喜笑颜开。祝你鸡年春节万事喜悦开心!",
             "春节送上整个正月的祝福，初一开开心心初二幸幸福福，初三美美满满初四平平安安，初五健健康康，十五甜甜蜜蜜，正月都顺顺当当!给你拜年啦!",

             ]
qrSource = ''
# 2016.12.4 名片信息会变化。无法保持
reply_Card = '<?xmlversion="1.0"?>\n<msgbigheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/a98icYIC0MQEqNutXUJPOkVVRcpibTp8qMWBicSehLv1ib8ERzzyqPseITvO5HaetYuHBA3aq93cOTN1a4pj3jic6tZb81wNiaKbn5hpAk1ELZvHk/0"smallheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/a98icYIC0MQEqNutXUJPOkVVRcpibTp8qMWBicSehLv1ib8ERzzyqPseITvO5HaetYuHBA3aq93cOTN1a4pj3jic6tZb81wNiaKbn5hpAk1ELZvHk/132"username="wxid_ygan7t9qskzd22"nickname="lua"shortpy="JJSW"alias="zxj3459564"imagestatus="3"scene="17"province=""city=""sign=""sex="0"certflag="0"certinfo=""brandIconUrl=""brandHomeUrl=""brandSubscriptConfigUrl=""brandFlags="0"regionCode=""/>\n'
# 2016.12.3
word_faces = ["✪ω✪", '٩(●̮̮̃●̃)۶ ٩(•̮̮̃•̃)۶ ٩(-̮̮̃-̃)۶ ٩(●̮̮̃•̃)۶ ٩(-̮̮̃•̃)۶ ٩(×̯×)۶ ٩͡[๏̯͡๏]۶', '✷(ꇐ‿ꇐ)✷',
              '┗|｀O′|┛ 嗷~~', '...φ(0￣*)啦啦啦_φ(*￣0￣)′ ', '咳咳＞＜', 'ˋ( ° ▽、° ) ',
              '§(*￣▽￣*)§', '( `０‘)ノ~~~~~~~~~ν ', 'o(′益`)o', '(*￣︿￣) ', '...:.;::..;::: .:.;::….;:￣)…:.;:□￣)(￣□￣*)复活',
              '(=゜ω゜)ノぃょぅ', '(寒￣ii￣)彡…彡…彡 ', '|(*′口`) ', 'こヾ(＾ｏ＾*)ん(ｏ＾^)ｏにｏ(＾０＾ｏ)ち(ｏ＾.＾)ノ" は ヾ(＊＾〇＾＊)ノ" ',
              'ヾ(′▽｀*)ゝ', '3=(-_-メ)', '...(*￣０￣)ノ', '||Φ|(|T|Д|T|)|Φ|| ', '(*￣3￣)╭', 'φ(゜▽゜*)?', '（*＾-＾*）',
              '(o゜▽゜)o☆[好主意!] ', '【】\(·ω·`)o ', 'o(*￣▽￣*)ゞ ', '（￣。。￣）[河马] ', '(_　_)。゜zｚＺ ',
              '[火箭筒，发射！](*￣皿￣)=Σ口＞=Σ口＞=Σ口＞ ',
              '(￣～￣) 嚼！', '(o^^)oo(^^o) ']
# logging.basicConfig(format='%(levelname)s:%(message)s', level=print)
KEYS = ['241b5a1059b04c898d00d197522a917c', 'ca6acaabfd7a40edb0b42a7bea233dc7', '85c0d048714b43e6bed1b0c966c20cbe']
# KEYS = ['85c0d048714b43e6bed1b0c966c20cbe']


# *************************二级库*************************#
def groupChatSwitch(msg, groupName):
    '''群聊开关'''
    groupId = chat_config["groups_dict"][groupName]
    if msg['Text'] == "开启":
        chat_config["Flag"][groupName] = True
        # message = '已开启'
        # itchat.send_msg('已开启', groupId)
        # reply = "\"{}\" 的专属新年特别版机器人---{} 正在启动".format(groupName, "小牛皮")
        reply = "\"{}\" 的专属机器人---{} 正在启动".format(groupName, "小牛皮")
        itchat.send_msg(reply, groupId)
    elif msg['Text'] == "关闭":
        chat_config["Flag"][groupName] = False
        # message = '已关闭'
        # itchat.send_msg('已关闭', groupId)
        # reply = "\"{}\" 的专属新年特别版机器人---{} 宕机啦!!!".format(groupName, "小牛皮")
        reply = "\"{}\" 的专属机器人---{} 宕机啦!!!".format(groupName, "小牛皮")
        itchat.send_msg(reply, groupId)


def groupChatShow(msg, groupName):
    '''群消息显示'''
    if msg["Type"] == "Text":
        receive = msg["Text"]
        print("群{}:  {}".format(groupName, receive))
        # 群消息开关
        if msg['Text'] in ["开启", "关闭"]:
            print("设置群聊开关")
            groupChatSwitch(msg, groupName)
            # todo 数据固化到file
            write_config(chat_config)
            return True
    elif msg["Type"] == "Picture":
        receive = "接收到群图片"
        print("群{}:  {}".format(groupName, receive))
    elif msg["Type"] == "Sharing":
        receive = msg["Text"]
        print("群{} 分享:  {}".format(groupName, receive))
    elif msg["Type"] == "Card":
        receive = msg['RecommendInfo'].get("NickName")
        print("群{} 名片：{}".format(groupName, receive))


def friendChatShow(msg):
    # 好友消息展示
    # print(chat_config["op_friends_dict"])
    # get_friends()
    # print(msg['FromUserName'])
    User = chat_config["op_friends_dict"].get(msg['FromUserName'])
    if msg["Type"] == "Text":
        print("接收到 {} 的信息：{}".format(User if User else "ht", msg['Text']))
        # 屏蔽好友---好友昵称
        if msg["Text"][:3] in ["add", "del"]:
            print("设置好友屏蔽")
            friendProtect(msg)
            # todo 数据固化到file
            write_config(chat_config)


    elif msg["Type"] == "Picture":
        receive = "发送图片"
        print("接收到 {}: {}".format(User if User else "ht", receive))
    elif msg["Type"] == "Sharing":
        print("接收到 {} 的分享：{}".format(User if User else "ht", msg['Text']))
    elif msg["Type"] == "Card":
        print("接收到 {} 的名片：{}".format(User if User else "ht", msg['RecommendInfo'].get("NickName")))


# 回复信息
def reply_message(msg):
    if msg["Type"] == "Text":
        reply = get_response(msg['Text'])#回复消息！！！！！
        # 2017.1.27 新年特别回复
        # reply = random.choice(wish_List)  # 新年特别版
        return reply
    elif msg["Type"] == "Picture":
        pictureReply(msg)
    elif msg["Type"] == "Sharing":
        reply = get_response(msg['Text'])
        return reply
    elif msg["Type"] == "Card":
        # reply = "收到名片啦"
        itchat.send_raw_msg(msg['MsgType'], msg["Content"], msg['FromUserName'])
        # itchat.send_raw_msg(msg['MsgType'], reply_Card, msg['FromUserName'])


def pictureReply(msg):
    face_list = get_faces_list()
    if face_list:
        face = random.choice(face_list)
        itchat.send('@img@{}'.format(face), msg["FromUserName"])
    else:
        face_word = random.choice(word_faces)
        itchat.send_msg(face_word, msg["FromUserName"])


def friendProtect(msg):
    if msg["Text"].startswith("add"):
        userProtect = msg["Text"][3:]
        chat_config["safe_friends"].append(userProtect)
        if userProtect in chat_config["safe_friends"]:
            print("成功屏蔽 {}".format(userProtect))

    elif msg["Text"].startswith("del"):
        userPublic = msg["Text"][3:]
        chat_config["safe_friends"].remove(userPublic)
        if userPublic in chat_config["safe_friends"]:
            print("成功取消{}的屏蔽".format(userPublic))
    print("当前安全用户列表：", list(set(chat_config["safe_friends"])))  # 去重操作


# safe_friends = ["如影随行","王翔" ]
# safe_groups=["鲁西中学群","TTCCKKYY"]
def choice_pic(list_pic):  # 获取随机数
    return random.choice(list_pic)


def get_path(n=1):
    current_path = os.path.abspath(__file__)
    for i in range(n):
        current_path = os.path.dirname(current_path)
    # print("当前路径：",current_path)
    return current_path


def get_file(path):
    return [i for i in os.listdir(path)]


def get_master():
    host_data = itchat.search_friends()
    # print(host_data)
    return host_data["NickName"]
    # test
    # mps_data=itchat.get_mps()
    # print(mps_data)
    # contact_data=itchat.get_contact()
    # print(contact_data)


#


# 获取配置
def getConfig():
    print("致敬         LittleCoder")
    print("__author__   ht")
    # get_master()  # 得到自己的信息
    get_groups()
    get_friends()
    if os.path.exists(get_cfg_path()):
        up_config()
    logging.warn("群flag：", chat_config["Flag"])
    print("已屏蔽好友名单：", chat_config["safe_friends"])


# 更新配置
def up_config():
    current_master = get_master()
    print("当前用户：", current_master)
    fileRcd = get_config()
    master = fileRcd["master"]
    print("记录的用户：", master)
    if master == current_master:
        chat_config["master"] = master
        safe_friends = fileRcd["safe_friends"]
        flags = fileRcd["Flag"]
        if len(safe_friends) > 0:
            chat_config["safe_friends"] = safe_friends
        if len(flags) > 0:
            chat_config["Flag"] = flags
    else:
        chat_config["master"] = current_master
        print("初始化--file记录")
        write_config(chat_config)


def get_groups():
    try:
        list_group = itchat.get_chatrooms(update=False)
        # print("获取群聊：{}".format(len(list_group)))
        # list_group_names = []
        # groups_dict = dict()
        for i in list_group:
            chat_config["groups_dict"][i['NickName']] = i['UserName']
            chat_config["op_groups_dict"][i['UserName']] = i['NickName']
            chat_config["Flag"][i['NickName']] = False

            chat_config["list_group"].append(i['NickName'])
            # print("群列表：{}".format(chat_config["list_group"]))
            # print("群字典：", chat_config["groups_dict"])
    except Exception as e:
        print("error:", e)


def get_friends():
    list_friend = itchat.get_friends(update=True)
    # print(list_friend)
    for j in list_friend:
        chat_config["friends_dict"][j['NickName']] = j['UserName']
        chat_config["op_friends_dict"][j['UserName']] = j['NickName']
        chat_config["list_friend"].append(j['NickName'])
        # print("好友列表:{}".format(chat_config["list_friend"]))

def get_response_xiaoice(msg):
    #微软小冰智能回复 2017.2.20
    ice_reply=itchat.send_msg(msg=msg,toUserName="")#带查阅验证
    return ice_reply

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
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return


@itchat.msg_register([TEXT, PICTURE, SHARING, CARD], isFriendChat=True)
def msg_reply(msg):
    defaultReply = "你在说什么"
    # show信息 ，并设置---好友屏蔽
    friendChatShow(msg)
    # 好友回复权限验证
    if msg['FromUserName'] in [chat_config["friends_dict"][i] for i in chat_config["safe_friends"]]:
        pass
        print("已屏蔽的好友")
    else:
        flag_reply = reply_message(msg)
        if flag_reply: return flag_reply


@itchat.msg_register([TEXT, PICTURE, SHARING, CARD], isGroupChat=True)
def msg_reply(msg):
    # groupId 是群id
    if '@@' in msg["FromUserName"]:
        groupId = msg["FromUserName"]
    else:
        groupId = msg["ToUserName"]
    groupName = chat_config["op_groups_dict"].get(groupId)
    # print("该群名：{}".format(groupName))
    # print("该群的groupId:{}".format(groupId))
    # 展示消息，并设置---群消息开关
    switch_flag = groupChatShow(msg, groupName)  # 开启 只回复一次开启成功；不加flag，会回复两次；
    if not switch_flag:
        # print("群状态开关：{}".format(chat_config["Flag"][groupName]))
        if not chat_config["Flag"][groupName]:
            pass
            # print("已屏蔽的群名")
        else:
            flag_reply = reply_message(msg)
            if flag_reply: return flag_reply


if __name__ == "__main__":
    itchat.auto_login(enableCmdQR=True, hotReload=True)
    # start_falsk()
    # itchat.auto_login(hotReload=True,qrCallback=qrCallback,exitCallback=ec)#2017.1.29  ec是退出的回调函数 尚未编写
    # itchat.auto_login(hotReload=False,qrCallback=qrCallback,exitCallback=ec)
    # itchat.get_chatrooms(update=False)#确保群聊列表 完整；不知道原因
    try:
        if valid_time():
            getConfig()
            itchat.run()
        else:
            print("已超出体验时间")
            time.sleep(15)
    except Exception as e:
        print("error:", e)
        time.sleep(15)

