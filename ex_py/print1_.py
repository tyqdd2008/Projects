#! /usr/bin/env python

def func(arg1,arg2 = 'default',*arg3,**arg4):
    print "arg1 = %s,arg2 = %s,arg3 = %s,arg4 = %s" %(arg1,arg2,arg3,arg4)

func(1)
func(1,2)
func(1,2,3,4)
func(1,2,3,4,x = 1,y  = 2)
#func(x = 1)
func(arg1 = 1)
func(1,x = 1)
