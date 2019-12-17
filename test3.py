import random
def getArray():
    return list(random.random()*100 for x in xrange(20))

def bubbleSort(arr):
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

if __name__ == '__main__':
    arr = getArray()
    bubbleSort(arr)
