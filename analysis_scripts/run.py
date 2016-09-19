import ROOT as r
from workflow import workflow

fsig = r.TFile("../bae-mc-12215002-2012-down.root")
tsig = fsig.Get("bar-muon-tuple/DecayTree")
f = r.TFile("../BuKMuMuX.root")
t = f.Get("Bplus_Tuple/DecayTree")

fnew = r.TFile("newtree.root","RECREATE")
tnew = t.CloneTree(-1,'fast')
tnew.SetBranchStatus('*',0)



myworkflow = workflow()

myworkflow.module_names.append('addRestFrameVars')


myworkflow.run(tnew)
