# coding=utf-8
##########   快捷键   ###########
# ctrl + /       快速注释
# shift + enter  快速回车
# shift + tab    取消缩进
################################


##########   格式化   #############################
# print('{0} love {1}'.format('I',"you"))
# print('{a} love {b}'.format(a='I',b="you"))
# print('{{0}}'.format('不打印'))
# print('%c' % 97)
# print('%c %c %c' % (97,98,99))
# print('%d + %d = %d' % (4,5,4+5))
##################################################

#################   数组   ########################
# b = [5,3]
# a = b
# c = b[:]
# b.append(5)
# b.extend([3,'abc',3])
# b.insert(1, 6)
# print(a)
# print(c)

# temp = ('a','b','d','e','f')      #元组
# temp = temp[:2]+("c",)+temp[2:]
# print(temp)

# a = list("Hello World")
# print(a)

# a = [1,3,5,7,9]
# b = [2,4,6,8,10]
# print(list(zip(a,b)))
# print(list(enumerate(a)))
##############################################

###############   定义函数   #####################
# def my_first_func(*para):    #收集参数
#     print(para)
#
#
# my_first_func(1,2,3)


# def total(a=5, *numbers, **phonebook):
#     print('a', a)
#
#     for single_item in numbers:
#         print('single_item', single_item)
#
#     for first_part, second_part in phonebook.items():
#         print(first_part, second_part)
#
# print(total(10, 1, 2, 3, Jack=1123, John=2231, inge=1550))      #函数没有返回值，print会出现None


# def funx(x):
#     def funy(y):
#         return x*y
#     return funy
#
# i = funx(8)
# print(i)
# print(type(i))
# print(i(5))
# print(funx(8)(5))


# g = lambda x, y : x ** 2 + y ** 2 - 1
# print(g(5,3))

# print(list(filter(lambda x:x%2, range(10))))       #0~9中的奇数

# print(list(map(lambda x:x*2, range(10))))
###################################################################


######################   函数递归   #################################
# def factorial(n):       #递归计算阶乘
#     if n == 1:
#         return 1
#     else:
#         return n * factorial(n-1)
#
# print(factorial(5))

# def fabonacci(n):       #递归求斐波那契数列
#     if n == 1 or n == 2:
#         return 1
#     else:
#         return fabonacci(n-1)+fabonacci(n-2)
#
# print(fabonacci(10))


# def hanoi(n,x,y,z):       #递归求解汉诺塔
#
#     if n == 1:
#         print(x,'-->',z)
#
#     else:
#         hanoi(n-1,x,z,y)
#         print(x,'-->',z)
#         hanoi(n-1,y,x,z)
#
#
# hanoi(10,'x','y','z')
###############################################################################################

##########################   字典   #########################################################
# dict1 = {'A':'a', 'B':'b', 'C':'c', 'D':'d'}
# print('A对应的是'+dict1['A'])

# dict2 = dict(((1,'a'), (2,'b'),(3,'c')))
# print(dict2)

# dict3 = dict(A='a', B='b', C='c')
# print(dict3)
# dict3['A']='aa'
# print(dict3)
# dict3['D']='d'
# print(dict3)

# dict4 = {}
# dict4 = dict4.fromkeys(range(15),"赞")
# for each_key in dict4.keys():
#     print(each_key)
# for each_value in dict4.values():
#     print(each_value)
# for each_item in dict4.items():
#     print(each_item)

###############################################################################################

##################################   集合   #########################################
# set1 = {1,2,3,4,5,4,3,2,1}
# print(set1)

# num1 = [1,2,3,4,5,4,3,2,1]      # 去除列表中的重复数据
# num1 = list(set(num1))
# print(num1)

# set2 = {1,2,3,4,5}
# set2.add(6)
# set2.remove(5)
# print(set2)

# set3 = frozenset([1,2,3,4,5])
# set3.add(6)     #会报错
####################################################################################

##############################   OS模块   ##########################################
# import os

###################################################################################

##############################   pickle模块   ######################################
# import pickle
# list1 = [123,456,789]
# pickle_file = open('list1.pkl','wb')
# pickle.dump(list1,pickle_file)
# pickle_file.close()
# pickle_file = open('list1.pkl','rb')
# list2 = pickle.load(pickle_file)
# print(list2)
###################################################################################

##############################   异常处理   ########################################
# try:
#     int('abc')
#     sum = 1 + '1'
#     f = open('我为什么是一个文件.txt')
#     print(f.read())
#     f.close()
# except OSError as reason:
#     print('文件出错了,错误的原因是:'+str(reason))
# except TypeError as reason:
#     print('类型出错了，错误的原因是：'+str(reason))
# except:
#     print('出错了')
# finally:
#     print('依然会执行')
##################################################################

##########################   对象   ################################
# class Mylist(list):       #继承
#     pass
# list2 = Mylist()
# list2.append(3)
# print(list2)

# class Ball:
#     def __init__(self,name):
#         self.name = name
#     def kick(self):
#         print('我是%s，谁踢我' % self.name)
#
# b = Ball('土豆')
# b.kick()

# class Person:
#     __name='xzj'        # 双下划线有隐藏的作用
#     def getname(self):
#         return self.__name
#
# p = Person()
# print(p.getname())
# #p.__name与p.name都无法在外部将name输出
# print(p._Person__name)      #这样可以输出

# class Parent:
#     def hello(self):
#         print("正在调用父类的方法")
#
# class  Child(Parent):
#     def hello(self):
#         print('正在调用子类的方法')
#
# c = Child()
# c.hello()


# import random as r
# class Fish:
#     def __init__(self):
#         self.x = r.randint(0,10)
#         self.y = r.randint(0,10)
#
#     def move(self):
#         self.x -= 1
#         print('我的位置是:',self.x,self.y)
#
# class Goldfish(Fish):
#     pass
#
# class Carp(Fish):
#     pass
#
# class Salmon(Fish):
#     pass
#
# class Shark(Fish):
#     def __init__(self):
#         super().__init__()
#         self.hungry = True
#
#     def eat(self):
#         if self.hungry:
#             print('吃')
#             self.hungry = False
#         else:
#             print('不吃')
#
# fish = Fish()
# goldfish = Goldfish()
# salmon = Salmon()
# shark = Shark()
#
# fish.move()
# goldfish.move()
# salmon.move()
# shark.eat()


# class Turtle:
#     def __init__(self,x):
#         self.num = x
#
# class Fish:
#     def __init__(self,x):
#         self.num = x
#
# class Pool:
#     def __init__(self,x,y):
#         self.turtle = Turtle(x)
#         self.fish = Fish(y)
#
#     def print_num(self):
#         print("共有乌龟%d只，小鱼%d条" % (self.turtle.num, self.fish.num))
#
# pool1 = Pool(10,1)
# pool1.print_num()

# class C:
#     count = 0
#
# a = C()
# b = C()
# c = C()
# c.count += 10
# C.count += 100
# print(a.count,b.count,c.count)

# class A:
#     pass
# class B(A):
#     pass
#
# b1 = B()
# print(issubclass(B,A))
# print(isinstance(b1,B))
# print(isinstance(b1,A))
# class C:
#     def __init__(self,x=0):
#         self.x = x
# c1 = C()
# print(hasattr(c1,'x'))
# print(getattr(c1,'x'))
# print(getattr(c1,'y','您访问的属性不存在'))
# setattr(c1,'y','z')
# print(getattr(c1,'y','您访问的属性不存在'))

# class C:
#     def __init__(self,size = 10):
#         self.size = size
#     def getSize(self):
#         return self.size
#     def setSize(self,value):
#         self.size = value
#     def delSize(self):
#         del self.size
#     x = property(getSize,setSize,delSize)
#
# c1 = C()
# print(c1.x)
# c1.x = 18
# print(c1.x)
# print(c1.getSize())
# del c1.x
# print(c1.size)      #会报错

# class Capstr(str):
#     def __new__(cls, string):
#         string = string.upper()
#         return str.__new__(cls, string)
#
# a = Capstr('I love you.')
# print(a)

# class New_int(int):
#     def __add__(self, other):
#         return int.__sub__(self,other)
#     def __sub__(self, other):
#         return int.__add__(self,other)
#
# a = New_int(3)
# b = New_int(5)
# print(a+b)
# print(a-b)


#计时器
# import time as t
#
# class Mytimer():
#     def __init__(self):
#         self.unit = ['年','月','日','小时','分钟','秒']
#         self.prompt = '未开始计时'
#         self.lasted = []
#         self.start = 0
#         self.stop = 0
#
#     def __str__(self):
#         return  self.prompt
#
#     __repr__ = __str__
#
#     def _start(self):
#         self.start = t.localtime()
#         self.prompt = '提示:请先调用_stop()停止计时'
#         print('计时开始')
#
#     def _stop(self):
#         if not self.start:
#             print('请先调用_start()开始计时')
#         else:
#             self.stop = t.localtime()
#             self._calc()
#             print('计时结束')
#
#     def _calc(self):
#         self.lasted = []
#         self.prompt = '总共运行了'
#         for index in range(6):
#             self.lasted.append(self.stop[index]-self.start[index])
#             if self.lasted[index]:
#                 self.prompt += (str(self.lasted[index])+self.unit[index])
#         print(self.prompt)
#         self.start = 0
#         self.stop = 0       #初始化
#
# t1 = Mytimer()
# t1._start()
# t1._stop()              #可利用debug试运行

#######################################################################

##############################   迭代器   ################################
# a = 'I love you!'
# b = iter(a)
#
# while True:
#     try:
#         each = next(b)
#     except StopIteration:
#         break
#     print(each)
##########################################################################
