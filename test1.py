import random
def getNum():
    return random.random()*10

def Myadd(a,b):
    return a+b

if __name__ == '__main__':
    num1 = getNum()
    num2 = getNum()
    print Myadd(num1,num2)