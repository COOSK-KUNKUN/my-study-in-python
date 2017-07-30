#coding=utf-8 
import math

class ClassName(object):                   # 创建类
	"""所有学生的基类"""   
	Classcount = 0                         # 类体

	def __init__(self, name,score,age):    # __init__() 方法被称为类的构造函数或初始化方法，当创建了这个类的实例时就会调用该方法
		self.name = name
		self.score = score
		self.age = age
		ClassName.Classcount += 1

	def displaycount( self ):
		print 'total ClassName are %d' % ClassName.Classcount
		pass

	def displayClassName( self ):
		print 'name:',self.name,',score:',self.score,',age:',self.age
		pass

class1 = ClassName('COOSK',80,18)             # 创建 classname 类的第一个对象
class2 = ClassName('17GB',90,18)              # 创建 classname 类的第二个对象
class1.displayClassName()
class2.displayClassName()
print 'total ClassName are %d' % ClassName.Classcount

print '\n'

print 'ClassName.__doc__:', ClassName.__doc__        # 类的文档字符串   
print 'ClassName.__name__:', ClassName.__name__      # 类名 
print 'ClassName.__module__:', ClassName.__module__  # 类定义所在的模块（类的全名是'__main__.className'，如果类位于一个导入模块mymod中，那么className.__module__ 等于 mymod） 
print 'ClassName.__bases__:', ClassName.__bases__    # 类的所有父类构成元素（包含了以个由所有父类组成的元组） 
print 'ClassName.__dict__:' , ClassName.__dict__     # 类的属性（包含一个字典，由类的数据属性组成）

print '\n'

class parent(object):            # 定义父类
	"""docstring for parent"""
	parentAttr = 200             # Attr 对象属性

	def __init__( self ):
	   print'调用父类构造函数'
	   pass

	def parentMethod( self ):
	   print '调用父类方法'
	   pass
		
	def setAttr( self, attr ):   # 设置属性
  	    parent.parentAttr = attr
	    pass

	def getAttr( self ):         # 获取属性
	   print'父类属性 :', parent.parentAttr
	   pass

class Child(parent):
	"""docstring for ClassName"""
	def __init__( self ):
	   print'调用子类构造方法'
	   pass

	def childMethod( self ):
		print'调用子类的方法'
		pass

c = Child()                     # 实例化子类
c.childMethod()                 # 调用子类的方法
c.parentMethod()                # 调用父类方法
c.setAttr(233)                  # 再次调用父类的方法
c.getAttr()	                    # 再次调用父类的方法

print '\n'

class dog(object):
	"""docstring for ClassName"""
	def __init__( self ):
		print 'wang!'
		pass

	def dogMethod( self ):
		print 'aowuuuuuuuu!'
		pass

	def setAttr( self, attr ):
		dog.dogAttr = attr
		pass

	def getAttr( self ):
		print 'emmmmmmmmmmm'
		pass

class cat(dog):
	"""docstring for cat"""
	def __init__(self ):
		print 'miaomiaomiao'
		pass

	def catMthod( self ):
		print 'miaoooooooooo'
		pass

d = cat()
d.catMthod()
d.dogMethod()

print '\n'		

class sun(object):             # 方法重写 如果你的父类方法的功能不能满足你的需求，你可以在子类重写你父类的方法
	"""docstring for sun"""
	def myMethod( self ):
		print '调用父类的方法'
		pass

class moon(object):
	"""docstring for moon"""
	def myMethod( self ):
		print '调用子类的方法，并实现方法的重写（重载）'
		pass

a = moon()
a.myMethod()

print '\n'

class num(object):
	"""运算符重载 for num"""
	def __init__(self,a,b):
		self.a = a
		self.b = b
		pass

	def __str__( self ):          
	    # 用于将值转化为适于人阅读的形式,简单的调用方法 : str(obj)  
         return 'num is (%d,%d)' % (self.a,self.b)
		 

	def __add__( self,other ):
         return 'num is (%d,%d)' % (self.a + other.a,self.b + other.b)

n1 = num(5,10)
n2 = num(3,-2)
print n1+n2		

print '\n'

# 类的私有方法
# __private_method：两个下划线开头，声明该方法为私有方法，不能在类地外部调用。
# 在类的内部调用 slef.__private_methods

class private(object):
	"""docstring for private"""
	__privateCount = 0     # 私有变量
	publicCount = 0        # 公开变量

	def count( self ):
		self.__privateCount += 1
		self.publicCount += 1
		print self.__privateCount
		
counter = private()
counter.count()
counter.count()
print counter.publicCount   # 无（）

try:
	print counter.__privateCount()
	pass
except Exception as e:
	print '报错，实例不能访问私有变量'
	
print '\n'


print 'all code are over'

raw_input("\n\nPress the enter key to exit.") #回车结束程序