#coding=utf-8 
import math;
import random;
import time;
import calendar
import support



import sys; x='coosk'; sys.stdout.write(x + '\n')

print '\n'

print 'hello world'

print '\n'

if True:
    print "True"
else:
    print "False"

print '\n'


a=b=c=1;                          #可直接定义
print a,b,c;

print '\n'

s='COOSK'                         #str
print s;

print '\n'

list = ['abcd',796,'efgh',233,666]
print list[0:3]                   # 输出第一个至第二个的元素

print '\n'

dict={} #字典
dict['one']='this is one'
tinydict = {'name':'17GB','age':20,'sex':'man'}
print dict['one']
print tinydict                    # 输出完整字典
print tinydict.keys()             # 输出所有键
print tinydict.values()           # 输出所有值
                                  # del dict['one'];   删除键是'one'的条目
                                  # dict.clear();      清空词典所有条目
                                  # del dict ;         删除词典
print '\n'

dict1 = {'name':'17GB','age':7}
dict2 = dict1.copy()              # 复制
print 'the dict2 is: %s'%(dict1)
                                  # dict.get('')       查找 
print '\n'                        # dict.setdefault(key, default=None) 如果键不已经存在于字典中，将会添加键并将值设为默认值 
# for循环的语法格式如下：
# for iterating_var in sequence:
#   statements(s)

fruits=['apple','banana','orange'] # 实例
for fruit in fruits:
	print 'the fruit is :',fruit

print '\n'

for x in range(20,30):             # 迭代 10 到 20 之间的数字
	for i in range(2,x):           # 根据因子迭代
		if x%i == 0:               # 不需要括号
		   j=x/i
		   print '%d = %d * %d' % (x,i,j)
		   break
	else :                         # 注意符号：
	 print x, 'is zhi shu'

print '\n'

print 'math.ceil(100.12) : ',math.ceil(100.12)   # 返回大于或者等于指定表达式的最小整数

print '\n'

# 输出 100 <= number < 1000 间的偶数
print 'randrange(100,1000,2):',random.randrange(100,1000,2)

# 输出 100 <= number < 1000 间的其他数
print 'randrange(100,1000,3):',random.randrange(100,1000,3)

print '\n'

print 'my name is %s i am %d old' % ('COOSK',20) #  %s格式化字符串  %d格式化整数

print '\n'

t=time.asctime(time.localtime(time.time())  )    # 获取时间    
print 'the time is :', t 

print '\n'

m = calendar.month(2017,7)
print 'the month is :'
print m;

print '\n'

def printme( like,hate ):        # 函数
   "YOOOOOO"
   print ('Like'),like;
   print ('Hate'),hate;
   return;

printme(like = 'cat',hate = 'dog');

print '\n'

def function(var1,var2):         # 可写函数说明
	total = var1 + var2
	print ('the value is :'),total
	return total;

total = function(13,53);         # 调用function函数,对total进行定义

print '\n'

support.TheName('COOSK')         # 调用support模块中的内容

print '\n'

content = dir(math)              # content内容，dir()函数一个排好序的字符串列表，内容是一个模块里定义过的名字。
print content;

print '\n'

# 输入
str0 = raw_input('please enter your input:') 
print 'I think your input is:',str0

print '\n'

#file object = open(file_name [, access_mode][, buffering])
#打开和关闭文件
fo = open('food.txt','wb')
print 'file name:',fo.name
print 'is close or not ? ',fo.close
print 'opening mode :',fo.mode   # 访问模式

print '\n'

# 对文件进行写入
fo = open('C:/Users/Administrator/Desktop/food.txt','wb')
fo.write('python is a great language')
# 写入完后关闭文件
fo.close()

print '\n'

# try:
# <语句>        #运行别的代码
# except <名字>：
# <语句>        #如果在try部份引发了'名字'异常
# except <名字>，<数据>:
# <语句>        #如果引发了'名字'异常，获得附加的数据
# else:
# <语句>        #如果没有异常发生

print 'all code are over'

raw_input("\n\nPress the enter key to exit.") #回车结束程序