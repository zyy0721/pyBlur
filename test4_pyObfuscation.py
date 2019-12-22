import array
import time
from memory_profiler import profile
@profile
def oo000 ( ) :
 ii = [ ]
 ii . extend ( range ( 1000000 ) )
 return ii
 if 51 - 51: IiI1i11I
@profile
def Iii1I1 ( ) :
 ii = array . array ( "l" )
 ii . extend ( range ( 1000000 ) )
 return ii
 if 73 - 73: II1I1iiiiii * ooo0OO / o0OO00 / oo
@profile
def i1iII1IiiIiI1 ( ) :
 for iIiiiI1IiI1I1 in range ( 0 , 1000 ) :
  print ( iIiiiI1IiI1I1 )
  if 87 - 87: OoOoOO00
if __name__ == "__main__" :
 stime = time.time()
 Iii1I1 ( )
 oo000 ( )
 i1iII1IiiIiI1 ( )
 etime = time.time()
 print(etime-stime)
