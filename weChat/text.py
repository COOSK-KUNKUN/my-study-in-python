# -*- coding: UTF-8 -*-

from wxpy import *

bot = Bot('bot.pkl', console_qr = True)
# 创建一个机器人
# console_qr – 在终端中显示登陆二维码
# 可为整数(int)，表示二维码单元格的宽度。
# 通常为 2 (当被设为 True 时，也将在内部当作 2)

myself = bot.self
# 登陆自己的号

bot.file_helper.send('Hello from wxpy!')
# 发送文字文件

bot.enable_puid('wxpy_puid.pkl')
# 启用 puid 属性，并指定 puid 所需的映射数据保存/载入路径

my_friend = bot.friends().search('COOSK')[0]
# 指定一个好友

print(my_friend.puid)

bot.self.add()
bot.self.accept()
# 在 Web 微信中把自己加为好友

bot.self.send('COOSK')
# 发送消息给自己

def upload_file(self, path):
    '''
    C:\Users\Administrator\Desktop\YiOlyiY_yYQYl0iUMXXJs0r3XOpiNZrrfSiIbVh_Re4.jpg
    https://i.redditmedia.com/YiOlyiY_yYQYl0iUMXXJs0r3XOpiNZrrfSiIbVh_Re4.jpg?w=1024&s=0ad4ecfdcfaf8f628d82fe9e884d35ef
    '''
    logger.info('{}: uploading file: {}'.format(self, path))

    @handle_response()
    def do():
        upload = functools.partial(self.core.upload_file, fileDir = path)
        ext = os.path.splitext(path)[1].lower()

        if ext in ('.bmp', '.png', '.jpeg', '.jpg', '.gif'):
            return upload(isPicture = True)
        elif ext == '.mp4':
            return upload(isVideo = True)
        else:
            return upload()
            pass
        pass
    return do().get('MediaId')

my_friend.send_image('BePWHDWDDiofy-U0ikQmK3WWmvg1_cNJbyB8ZRmK1Ho.jpg')
# 发送图片
embed()