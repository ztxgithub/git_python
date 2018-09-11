#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# import logging
#
# print(r'''hello world
# hello world2
# hello world3''')
#
# logging.info("%d" % 1)

def person(name, age, **kw):
    print ('name:', name, 'age:', age, 'other:', kw)

person('1', '2', city='Beijing')

# 命名关键字
# def person_n(name, *, addr):
#     print(name, addr)
#
#
# person('1', addr='Beijing')