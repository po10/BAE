
import ROOT as r


class module:

  def __init__(self):
    self.name = 'undefined'
    self.requiredBranches = []

  def run(self,t):
    print 'you have not implemented this for class:',self.name

  def activateBranches(self,t):
    for branch in self.requiredBranches:
      t.SetBranchStatus(branch,1) 
