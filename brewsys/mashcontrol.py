class MashController(object):
    def __init__(self):

        self.sttemp      = 0 # strike temp
        self.atemp       = 0 # actual temp(from sensor)
        self.mtemp       = 0 # desired temp(from xml)
        self.act_sp_temp = 0 # actual sparge water temp(from sensor)
        self.diff        = 0 # amount above mash temp to set stemp
        self.sptemp      = 0 # sparge water temp(mtemp + diff)
        
        self.sol    = False  # state of the solenoiod(False is closed state)
        self.spark  = False  # state of sparker

    def HeatStrike(self):
        # open solenoiod
        # fire burner
        # heat strike water to self.sttemp
        # close solenoid
        pass

    def HeatMash(self):
        """
        Used when self.atemp is more that 1 degree lower
        than self.mtemp or to go to the next mash step
        """
        # self.diff = 20
        # set self.sptemp
        # open solenoid   # maybe this goes in self.SpargeEvent(None)?
        # fire burner     # maybe this goes in self.SpargeEvent(None)?
        # run/maintain until self.atemp is within 1 degree of self.mtemp
        # event loop to maintain?!!! self.SpargeEvent()
        pass

    def TooHot(self):
        # close solenoid
        # do nothing until conditions for Maintain() are met
        pass

    def Maintain(self):
        # self.diff = 10
        # set self.sptemp()
        # open solenoid # maybe this goes in self.SpargeEvent()?
        # fire burner   # maybe this goes in self.SpargeEvent()?
        # close solenoid when self.sttemp is reached,
        # event loop to maintain?!!! self.SpargeEvent()
        pass

    def TempCheck(self, e):
        """
        This will need an event to check self.atemp periodically.
        """
        if self.atemp == '<low condition>':
            self.HeatMash()

        elif self.atemp == '<high condition>':
            self.TooHot()

        else:
            self.Maintain()
        

    def SpargeEvent(self, e):
        """
        This will need an event to check self.act_sp_temp
        """
        # heat water to self.sptemp and maintain +/- 2 degrees
        
        # if we are -2 degrees below desired temp
        if self.act_sp_temp < self.mtemp + self.diff - 2:
          # this would halt heating at a certain point to let the mash temp naturally come up
          # and self.atemp < self.mtemp - x degrees? 
          
            # open solenoid
            self.sol = True
            # fire burner, this will need to be timed to stop after x seconds!!!
            self.spark = True
            
        elif self.act_sp_temp == self.mtemp + self.diff + 2:
            # make sure the soloenoid is closed and we aren't sparking
            self.sol = False
            self.spark = False
    
            # - enter TooHot() or Maintain()?