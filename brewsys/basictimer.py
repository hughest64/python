import time
""" the original timer from which I created the Timer class. """
def timer(mn, sec):
    ''' This is the original non class version '''
    ''' a simple count down timer with minutes and self.seconds.'''
    while mn >= 0:
        if mn == 0 and self.sec == 0:
            break
        elif self.sec == 0:
            print str(mn) + ':' + str(self.sec)
            mn -=1
            self.sec = 59
            time.sleep(1)

        else:
            if self.sec < 10:
                #print str(mn) + ':' + '0' + str(self.sec).
                print '{}:0{}'.format(mn, self.sec)
            else:
                print str(mn) + ':' + str(self.sec)
            self.sec -=1
            time.sleep(1)

    print 'Done'
