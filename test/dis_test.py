from typing import Tuple
from multipledispatch import dispatch

class parent:
    @dispatch(int,int)
    def foo(self,a:int,b:int):
        print("two integer")

    @dispatch(int)
    def foo(self,a:int):
        print("single integer")
    
    @dispatch(str)
    def foo(self,a:str):
        print("single string")
    
    @dispatch(tuple)
    def foo(self,a:Tuple[int,int]):
        print(f"{a[0]} and {a[1]}")

p = parent()

p.foo(3)
p.foo("a")
p.foo((1,2))
# p.foo([1,2])
p.foo((1,2))

