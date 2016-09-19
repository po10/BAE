import ROOT as r
from module import module


class workflow:
  def __init__(self):
    self.module_names = []
 

  def parseSelection(self):
     

  def run(self,t):
     
    for modname in self.module_names:
      mymod = getattr(__import__(modname,fromlist=[modname]),modname)
      mymodule = mymod()
      mymodule.activateBranches(t)
    for i,event in enumerate(t):
      if (i%10000 == 0):
        print 'processing event number',i
      passed = True
      for modname in self.module_names:
        mymod = getattr(__import__(modname,fromlist=[modname]),modname)
        mymodule = mymod()
        passed = passed and mymodule.run(t)
        #if passed:
          #t.Fill() 
