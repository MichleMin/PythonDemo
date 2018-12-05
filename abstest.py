#!/usr/bin/env python3
import math
def my_abs(x):
    # 参数类型检查
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x


def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny


def power(x, n=2):
    s = 1 
    while n > 0:
        n = n - 1
        s = s * x
    return s

# 可变参数
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum += n * n
    return sum

# 命名关键字参数
def person(name, age, **kw):
    if "city" in kw:
        pass
    if "job" in kw:
        pass
    print('name:', name, 'age:', age, 'other:', kw)


def findMinAndMax(L):
    if L==[]:
        return (None,None)
    S = sorted(L)
    return (S[0],S[-1])
    # min = L[0]
    # max = L[0]
    # for x in L:
    #     if min > x:
    #         min = x
    #     if max < x:
    #         max = x
    # return (min,max)

def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a + b
        n += 1
    return 'done'


print(power(9,3))
print(calc(1,2,3,4))
numbers = [1,2,3,4]
print(calc(*numbers))

person("hemin",26,city="眉山",addr="Chengdu",zipcode=12345)

print("输出最小值和最大值",findMinAndMax([3,-1,2,8,5,55]))
fib(32)