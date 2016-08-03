import ROOT as r
from math import *
from array import array
from ROOT import TFile, TTree, TCut



#get the file
#f1  = r.TFile("bae-mc-12143001-2012-up-workcopy.root", "update") #B+ --> J/psi K
f1 = r.TFile("bae-mc-10010037-2012-up.root", "update") # SL stuff
#get the tree
t1 = f1.Get("bar-muon-tuple/DecayTree")


#f1 = r.TFile("bae-mc-12143001-2012-up-workcopy.root", "update")
#f2 = r.TFile("bae-mc-10010037-2012-up.root")

#f3 = r.TFile("/afs/cern.ch/user/y/yamhis/RataWork/bae-mc-12215002-2012-down.root")
#this one is empty, note sure why?


#t1 = f1.Get("bar-muon-tuple/DecayTree")

print "This amazing ntuple contains : "+str(t1.GetEntries())

#let's set branches

t1.SetBranchStatus("*",0)

t1.SetBranchStatus("Bplus_M*",1)

t1.SetBranchStatus("Bplus_ENDVERTEX_*",1)

t1.SetBranchStatus("Bplus_OWNPV_*",1)

t1.SetBranchStatus("Kplus_P*",1)

t1.SetBranchStatus("Jpsi_P*",1)

t1.SetBranchStatus("muplus_P*",1)

t1.SetBranchStatus("muminus_P*",1)


t1.SetBranchStatus ("Bplus_FD_OWNPV",1)


#from PDG
PDG_Kaon = 493.677
#Stuff we will need
Hop_B =0
HopCorrection = 0
t1.Branch( 'Hop_B', Hop_B, 'Hop_B/D' )
t1.Branch( 'HopCorrection', HopCorrection, 'HopCorrection/D' )


bu_mass_hist = r.TH1D("bu_mass_hist","bu_mass_hist",100,2000,10000)


HopCorrection_hist = r.TH1D("HopCorrection_hist","HopCorrection_hist",100,-5,+5)
Hop_B_hist = r.TH1D("Hop_B_hist","Hop_B_hist",100,2000,10000)

# we always need little counters

MaxEntries = t1.GetEntries()
i = 0

#for event in t1 :
for loopy in range (MaxEntries) :
    t1.GetEntry(loopy)

    bu_mass_hist.Fill(t1.Bplus_M)
    #print t1.Bplus_M
    cosThetaKaon =  (( t1.Bplus_ENDVERTEX_X- t1.Bplus_OWNPV_X) * t1.Kplus_PX + ( t1.Bplus_ENDVERTEX_Y- t1.Bplus_OWNPV_Y) * t1.Kplus_PY + (t1.Bplus_ENDVERTEX_Z- t1.Bplus_OWNPV_Z) * t1.Kplus_PZ)/(t1.Kplus_P * t1.Bplus_FD_OWNPV)
    cosThetaDiMuon =(( t1.Bplus_ENDVERTEX_X- t1.Bplus_OWNPV_X) * t1.Jpsi_PX + ( t1.Bplus_ENDVERTEX_Y- t1.Bplus_OWNPV_Y) * t1.Jpsi_PY + ( t1.Bplus_ENDVERTEX_Z- t1.Bplus_OWNPV_Z) * t1.Jpsi_PZ) /(t1.Jpsi_P * t1.Bplus_FD_OWNPV)

    pTKaon = t1.Kplus_P*sqrt(1.- cosThetaKaon*cosThetaKaon )
    pTDiMuon = t1.Jpsi_P*sqrt(1.- cosThetaDiMuon*cosThetaDiMuon )

    HopCorrection = pTDiMuon/pTKaon # you will go in the tree
    HopCorrection_hist.Fill(HopCorrection)

    KaonPlusMissingE4Mom =r.TLorentzVector ()
    KaonPlusMissingE4Mom.SetXYZM(HopCorrection*t1.Kplus_PX, HopCorrection*t1.Kplus_PY, HopCorrection*t1.Kplus_PZ, PDG_Kaon)

    OriginalDiMuon4Mom = r.TLorentzVector()
    OriginalDiMuon4Mom .SetPxPyPzE(t1.Jpsi_PX, t1.Jpsi_PY, t1.Jpsi_PZ, t1.Jpsi_PE )

    B4Mom =  KaonPlusMissingE4Mom + OriginalDiMuon4Mom
    Hop_B = B4Mom.M() # you will go in the tree
    Hop_B_hist.Fill(Hop_B)


    t1.Fill()
    i+=1






c = r.TCanvas("c", "c", 300,500)
c.Divide(1,2)
c.cd(1)
Hop_B_hist.Draw()
bu_mass_hist.Draw("SAME")
bu_mass_hist.SetLineColor(2)
c.cd(2)
HopCorrection_hist.Draw()
c.SaveAs("HopHistos.pdf")
f1.Write()
f1.Close()
print "I am done people "
