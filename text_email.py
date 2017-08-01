# -*- coding: UTF-8 -*-
# llkwabnxnrcicaea

# Python创建 SMTP 对象语法如下：
# smtpObj = smtplib.SMTP( [host [, port [, local_hostname]]] )
# port: 如果你提供了 host 参数, 你需要指定 SMTP 服务使用的端口号，一般情况下SMTP端口号为25

# Python SMTP对象使用sendmail方法发送邮件，语法如下：
# SMTP.sendmail(from_addr, to_addrs, msg[, mail_options, rcpt_options]
# from_addr: 邮件发送者地址。 
# to_addrs: 字符串列表，邮件发送地址。 
# msg: 发送消息 
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host="smtp.163.com"           #设置服务器
mail_user="coosk_kunkun@163.com"   #用户名
mail_pass="coosk18907591168"       #口令

sender = 'coosk_kunkun@163.com'
receivers = ['532866709@qq.com']

message = MIMEText('python 邮件发送测试...', 'plain','utf-8')   # 设置正文
message['From'] = Header('COOSK', 'utf-8')                     # 设置发送人
message['To']   = Header('测试','utf-8')                       # 设置接收人

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
	smtpObj = smtplib.SMTP()
	smtpObj.connect(mail_host, 25)
	smtpObj.login(mail_user,mail_pass)
	smtpObj.sendmail(sender, receivers, message.as_string())
	print 'success!'
except smtplib.SMTPException:
	print 'fail'
	

# 发送失败