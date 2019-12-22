import array
def test_list():
    x = []
    x.extend(range(1000000))
    return x

def test_array():
    x = array.array("l")
    x.extend(range(1000000))
    return x

def test_loop():
    for num in range(0,1000):
        print (num)

if __name__ == "__main__":
    test_array()
    test_list()
    test_loop()
