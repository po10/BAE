import ROOT as r
from math import *

def plotMissingMass(t,hname):

	t.SetBranchStatus("*",0)
	t.SetBranchStatus("Bplus_P*",1)
	t.SetBranchStatus("Kplus_P*",1)
	t.SetBranchStatus("Kplus_M",1)
	t.SetBranchStatus("Bplus_M",1)
	t.SetBranchStatus("*travelled",1)

	mB = 5284.0

	hmissing_mass = r.TH1D(hname+"_missingmass","missing_mass_hist",50,-4,12)
	hmXs = r.TH1D(hname+"_mXs","hmXs",50,-2000,4000)

	i = 0

	for event in t:
	  pz = (mB/t.Bplus_M)*t.Bplus_PZ
	  Bvect = r.TVector3(t.Bplus_X_travelled,t.Bplus_Y_travelled,t.Bplus_Z_travelled).Unit()
	  p = pz/Bvect.Z()
	  px = p*Bvect.X()
	  py = p*Bvect.Y()
	  E = sqrt(p*p+mB*mB)
	  BLvect = r.TLorentzVector(px,py,pz,E)
	  visLvect = r.TLorentzVector(t.Bplus_PX,t.Bplus_PY,t.Bplus_PZ,t.Bplus_PE)
	  missingvect = BLvect - visLvect
	  missingmass = missingvect.M2()/1e6
	  hmissing_mass.Fill(missingmass)
	  kaonvect = r.TLorentzVector(t.Kplus_PX,t.Kplus_PY,t.Kplus_PZ,t.Kplus_PE)
	  Xsvect = kaonvect+missingvect
	  mXs = Xsvect.M()
	  #if t.Bplus_M < 5280:
	    #print t.Bplus_M,BLvect.M()
	     
	  hmXs.Fill(mXs)
	  i+=1
	  if i%10000 == 0:
	    print 'reading event number',i
	  if i > 10000:
	    break
	hmissing_mass.GetXaxis().SetTitleOffset(0.8)
	hmissing_mass.GetXaxis().SetTitle("m_{miss}^{2} [GeV^{2}/c^{4}]")
	hmissing_mass.Draw()
	r.gPad.SetBottomMargin(0.18)
	r.gPad.SaveAs("missing_mass.pdf")

	hmXs.GetXaxis().SetTitleOffset(0.8)
	hmXs.GetXaxis().SetTitle("m_{Xs} [GeV/c^{2}]")
        return hmXs
  
 

fsig = r.TFile("../bae-mc-12215002-2012-down.root")
tsig = fsig.Get("bar-muon-tuple/DecayTree")
f = r.TFile("../BuKMuMuX.root")
t = f.Get("Bplus_Tuple/DecayTree")

hmXs = plotMissingMass(t,"data")
hmXs_sig = plotMissingMass(tsig,"signal")
hmXs.SetLineColor(r.kRed)
hmXs.Draw()
hmXs_sig.Draw("same")

leg = r.TLegend(0.2,0.5,0.5,0.7)
leg.SetFillColor(0)
leg.AddEntry(hmXs,"data","l")
leg.AddEntry(hmXs_sig,"K#pi#pi#mu#mu","l")
leg.Draw()
r.gPad.SaveAs("mXs.pdf")


