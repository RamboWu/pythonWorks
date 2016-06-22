#  -*- coding: utf-8 -*-
#!/usr/bin/python

from CommandManager import Manager

def  accepts (* types) :
    def  check_accepts ( f) :
        def  new_f (* args,  ** kwds) :
            print(args, ' / ', kwds)
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

@ accepts ( int ,  ( int , float ))
@ returns (( int , float ))
def  func ( arg1,  arg2) :
    return  arg1 *  arg2

manager = Manager()

@manager.command
def test():
    print ('hahah')

@manager.option('-u', '--username', dest='username')
def login(username=None):
    print(username)

if  __name__ ==  '__main__':
    #print(manager._commands)
    manager.run()
    #a =  func( arg1=float(3.1) , arg2=4)
    #print(a)
    #useful(3,4)
    pass
