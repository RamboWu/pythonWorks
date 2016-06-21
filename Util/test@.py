#  -*- coding: utf-8 -*-
#!/usr/bin/python

def onexit(f):
    def plusResult(i):
        return i + 1
    return plusResult

@onexit
def func(i):
    return i

def spamrun(fn):
    def sayspam(a):
        print ("spam,spam,spam", a)
    return sayspam

@spamrun
def useful(a,b):
    print (a**2+b**2)

def  accepts (* types) :
    def  check_accepts ( f) :
        def  new_f (* args,  ** kwds) :
            for  ( a,  t)  in  zip ( args,  types) :
                assert  isinstance ( a,  t),  \
                       "arg %r does not match %s " % ( a, t)
            return  f(* args,  ** kwds)
        return  new_f
    return  check_accepts

def  returns ( rtype) :
    def  check_returns ( f) :
        def  new_f (* args,  ** kwds) :
            result =  f(* args,  ** kwds)
            assert  isinstance ( result,  rtype),  \
                   "return value %r does not match %s " % ( result, rtype)
            return  result
        return  new_f
    return  check_returns

#@ accepts ( int ,  ( int , float ))
#@ returns (( int , float ))
def  func ( arg1,  arg2) :
    return  arg1 *  arg2

func = returns(( int , float ))(func)

if  __name__ ==  '__main__':
    a =  func( 3 , 'a')
    print(a)
    #useful(3,4)
