#coding=utf8
import sys, os,random
import requests, json

key = 'e0daf2ded41fdc6e471377498759b8e3'
KEYS = ['241b5a1059b04c898d00d197522a917c', 'ca6acaabfd7a40edb0b42a7bea233dc7', '85c0d048714b43e6bed1b0c966c20cbe']
def get_response(msg, storageClass = None, userName = None, userid = 'ItChat'):
    url = 'http://www.tuling123.com/openapi/api'
    payloads = {
        'key': random.choice(KEYS),
        'info': msg,
        'userid': userid,
    }
    try:
        r = requests.post(url, data = json.dumps(payloads)).json()
    except:
        return
    if not r['code'] in (100000, 200000, 302000, 308000, 313000, 314000): return
    if r['code'] == 100000: # 文本类
        return '\n'.join([r['text'].replace('<br>','\n')])
    elif r['code'] == 200000: # 链接类
        return '\n'.join([r['text'].replace('<br>','\n'), r['url']])
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


if __name__ == '__main__':
    while True:
        a = raw_input('>').decode(sys.stdin.encoding)
        print get_response(a, 'ItChat')
