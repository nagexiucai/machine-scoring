#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2017/12/27 11:57
# @Author  : Bob
# @Website : www.nagexiucai.com
# @E-Mail  : me@nagexiucai.com
# @Summary : 根据小学数学原理作业。

x = 9527.0

# 是质数否
# for i in range(1,4764):
#     d = x/i
#     q = d - int(d)
#     if not q:
#         print(i,q)
# 1 0.0
# 7 0.0
# 1361 0.0

y = 1314

# 分数是循环小数否、求循环节
T = []
k = 0
p = 0
while True:
    k += 1
    if k == 10000:
        break
    t, s = divmod(y,x)
    if int(s) == y:
        y *= 10
        print(k,t,s)
        if p == 0:
            p = k
        continue
    T.append(str(int(t)))
    y = int(s)
    if not s:
        break

print(p,"".join(T))
