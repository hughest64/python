import time
""" some tests """
class Timer(object):

    def __init__(self):
        self.s = 0

    def Set(self, s):
        self.s = s

    def Run(self):
        self.s -= 1
        time.sleep(1)

    def Display(self):
        return self.s


#########################

# used in GUI file
timer = Timer()
timer.Set(10)
display = timer.Display()

while display >= 0:
    # replace with DrawText method in GUI OnPaint() function
    print str(display)
    display -= 1
    # decrement the timer
    timer.Run()
