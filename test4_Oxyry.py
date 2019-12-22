import array
from memory_profiler import profile
import time
@profile
def test_list ():#line:3
    O0O0000OOO00OO0OO =[]#line:4
    O0O0000OOO00OO0OO .extend (range (1000000 ))#line:5
    return O0O0000OOO00OO0OO #line:6
@profile
def test_array ():#line:8
    O0O000OO0OOOO0O00 =array .array ("l")#line:9
    O0O000OO0OOOO0O00 .extend (range (1000000 ))#line:10
    return O0O000OO0OOOO0O00 #line:11
@profile
def test_loop ():#line:13
    for O0O0OO00OO0O0O000 in range (0 ,1000 ):#line:14
        print (O0O0OO00OO0O0O000 )#line:15
if __name__ =="__main__":#line:17
    stime = time.time()
    test_array ()#line:18
    test_list ()#line:19
    test_loop ()#line:20
    etime = time.time()
    print(etime - stime)
