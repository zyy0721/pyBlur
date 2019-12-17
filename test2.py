class DoMain:

    def __init__(self):
        self.a = "zyyhasasecrects"

    def Ask(self):
        res = raw_input("Please enter your password: ")

        if res == self.a:
            print "Succeed"
        else:
            print "Failed"

if __name__ == "__main__":
    dm = DoMain()
    dm.Ask()