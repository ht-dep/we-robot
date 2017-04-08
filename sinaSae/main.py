# coding=utf8
import itchatmp
import random,os,time
from itchatmp.content import (
    TEXT, MUSIC, IMAGE, VOICE,
    VIDEO, THUMB, NEWS, CARD,
    SAFE)
from tuling import get_response

itchatmp.update_config(itchatmp.WechatConfig(
    token='squirrel',
    appId='wx28cd173c32454d59',
    appSecret='f740cea1c5027526c56ead4eb12814db'),

)

word_faces =[u"✪ω✪", u'✷(ꇐ‿ꇐ)✷', u"｡◕‿◕｡", u"(๑￫ܫ￩)", u"(-人-) [拜佛] ", u"(。﹏。*)", u"(*/ω＼*)",
              u" ( *^-^)ρ(^0^* )", u"(●'◡'●)ﾉ♥", u"( ◔ ڼ ◔ )", u"( ´◔ ‸◔`)", u"(・ω< )★", u"(♥◠‿◠)ﾉ",
              u'（*＾-＾*）', u"(☍﹏⁰)", u"(｡◕ˇ∀ˇ◕）", u"✪ω✪", u"~Ⴚ(●ტ●)Ⴢ~", u"(,,Ծ‸Ծ,,)", u"(๑◕ܫ￩๑)b",
              u"v( ^-^(ё_ёゝ", u"(๑￫ܫ￩)", u"(˘❥˘)", u"(╬▔＾▔)凸", u"(✿◡‿◡)", u"o(￣▽￣)ｄ", u"(；′⌒`)",
              u"(ˉ▽￣～) 切~~", u"╰(*°▽°*)╯",
              u" ( ｡ớ ₃ờ)ھ", u"◔ ‸◔？", u"╮(๑•́ ₃•̀๑)╭", u"٩(๑´0`๑)۶", u"（//▽//）", u"(๑•́ ₃ •̀),",
              u"( ´◔ ‸◔`) ", u"(..•˘_˘•..)", u"๑乛◡乛๑ ", u"（๑￫‿ฺ￩๑）", u"♥(｡￫v￩｡)♥", u"(๑＞ڡ＜)☆",
              u"(╯’ – ‘)╯︵ ┻━┻", u"(•‾̑⌣‾̑•)✧˖°", u"(´∩｀。) ", u" º·(˚ ˃̣̣̥᷄⌓˂̣̣̥᷅ )‧º·˚", u" (｀◕‸◕´+) ",
              u"(oﾟωﾟo)", u"(ΦωΦ)", u" (*′∇`*)", u"(￣y▽￣)~*", u"------\(˙<>˙)/------",
              u"(#‵′)凸 ", u"(；°○° ) ", u"  ٩(͡๏̯͡๏)۶ ", u"( ＿ ＿)ノ｜扶墙", u"（＾∀＾）", u"(•̀ᴗ•́)و ̑̑ "
              ]

def get_current_dir():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    # print("当前目录：",file_dir)
    return file_dir
def get_faces_list():
    face_path = os.path.join(get_current_dir(), "faces")
    if os.path.exists(face_path):
        faces_list = os.listdir(face_path)
        # print("表情列表：",faces_list)
        return [os.path.join(face_path, i) for i in faces_list]
    else:
        return
def pictureReply():
    face_word = random.choice(word_faces)
    return face_word

@itchatmp.msg_register(itchatmp.content.TEXT)
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
        # reply = pictureReply()
        reply = u"接收到图片"
        return reply
    if msg["MsgType"] == "event":
        # print("hhh")
        if msg["Event"] == "subscribe":
            # print("关注")
            reply =u"你好，欢迎关注squirrel"
            return reply
        if msg["Event"] == "unsubscribe":
            # print("取消关注")
            return
        else:
            return
    else:
        return



app = itchatmp.run(isWsgi=True)
