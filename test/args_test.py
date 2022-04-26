from multipledispatch import dispatch
from soupsieve import Iterable

class arg_test:
    def foo(self,*args):
        print(f"args : {args}")

        for i in args:
            self.bar(i)

    @dispatch(tuple)
    def bar(self,t:tuple):
        print(f"tuple : {t}")

    @dispatch(int)
    def bar(self,i:int):
        print(f"integer : {i}")
    
    @dispatch(int,int)
    def bar(self,i:int):
        print(f"integer : {i}")

a = arg_test()

a.foo(1,2,3,(5,1),23,(84),(1,15,2,63))

