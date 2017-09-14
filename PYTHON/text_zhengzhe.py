#  -*- coding: UTF-8 -*-

import re


pat = '[a-zA-Z]+'
text = '"Hm...err -- are you sure?" he said, sounding insecure.'
re.findall( pat, text, re.M|re.I)
# findall 列出字符串中模式的所有匹配项
print 'the re.findall are :',re.findall(pat,text, re.M|re.I)

print '\n'

some_text = 'apple, bear, happy home'
re.split('[,]+',some_text, re.M|re.I)
# split 根据模式的匹配项来分割字符串
print 'the re.split are : ', re.split('[,]+',some_text, re.M|re.I)

print '\n'

some_part = '{name}'
text_1 = 'Dear {name}...'
re.sub(some_part, 'Mrs.Alice',text_1, re.M|re.I)
# sub 将字符串中所有 pat 的匹配项用 repl 替换
# sub (pat, rep, string[,count = 0])
print '',re.sub(some_part, 'Mrs.Alice',text_1, re.M|re.I)

print '\n'

some_line = 'coosk-kunkun.github.io'
m = re.match(r'coosk\.(.*)\..{3}', some_line, re.M|re.I)
if m:
	print '', m.group(0)
	print '', m.group(1)
else:
	print 'no'
