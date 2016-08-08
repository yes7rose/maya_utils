# -*- coding: utf-8 -*-

#  只是个模板，继承还是有问题，不用于继承
class Singleton(object):
    def __init__(self):
        globals()[self.__class__.__name__] = self

    def __call__(self):
        return self
    
# class Singleton:
#     def __call__(self):
#         return self
# 
# Singleton = Singleton()