#-*- coding:utf-8 -*-

import web, os
from hashlib import sha1
from xml.sax.saxutils import escape
from pyweixin import WeiXin as Wx

web.config.debug = True

if 'SERVER_SOFTWARE' in os.environ:
    from bae.api import logging
    onBAE = True
else:
    onBAE = False
    import logging
    logging.basicConfig(filename='log.out', level=logging.INFO)

TOKEN = 'NEUPIONEER204'

urls = (
    '/(.*)/', 'redirect',
    '/weixin', 'Weixin'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class redirect:
    def GET(self, path):
        web.seeother('/' + path)

class Weixin:
    def GET(self):
        valid_data = web.input()
        sign = valid_data.signature
        signList = [TOKEN, valid_data.timestamp, valid_data.nonce]
        signList = sorted(signList)
        clientSign = sha1(''.join(signList)).hexdigest()
        if sign == clientSign:
            return valid_data.echostr
        else:
            return sign, signList, clientSign

    def POST(self):
        rawPost = web.data()
        res = {}
        if rawPost:
            wx = Wx.on_message(rawPost)
            reqContent = wx.to_json()
            if reqContent['MsgType'] == 'location':
                lat = reqContent['Location_X']
                lng = reqContent['Location_Y']
                from lbsapi import getPOIByCircle
                try:
                    content = getPOIByCircle(center=(lat, lng), radius=2000)
                except:
                    content = u'error'
            else:
                content = escape(rawPost)
            return wx.to_xml(from_user_name=reqContent['ToUserName'],
                             to_user_name=reqContent['FromUserName'],
                             create_time=reqContent['CreateTime'],
                             msg_type='text',
                             content=content,
                             func_flag=0)
        else:
            return '404'

if onBAE:
    app = web.application(urls, globals()).wsgifunc()
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(app)
else:
     app = web.application(urls, globals())
if __name__ == '__main__':
    app.run()
