import ROOT as r
from math import *


f1 = r.TFile("bae-mc-12143001-2012-up.root")
f2 = r.TFile("bae-mc-10010037-2012-up.root")

#f3 = r.TFile("/afs/cern.ch/user/y/yamhis/RataWork/bae-mc-12215002-2012-down.root")
#this one is empty, note sure why?


t1 = f1.Get("bar-muon-tuple/DecayTree")
t1.SetBranchStatus("*",0)
t1.SetBranchStatus("Bplus_P*",1)
t1.SetBranchStatus("Kplus_P*",1)
t1.SetBranchStatus("Kplus_M",1)
t1.SetBranchStatus("Bplus_M",1)
t1.SetBranchStatus("*travelled",1)
t1.SetBranchStatus("Bplus_BKGCAT",1)
t1.SetBranchStatus("Jpsi_M", 1)
t2 = f2.Get("bar-muon-tuple/DecayTree")
t2.SetBranchStatus("*",0)
t2.SetBranchStatus("Bplus_P*",1)
t2.SetBranchStatus("Kplus_P*",1)
t2.SetBranchStatus("Kplus_M",1)
t2.SetBranchStatus("Bplus_M",1)
t2.SetBranchStatus("*travelled",1)
t2.SetBranchStatus("Jpsi_M", 1)
"""
t3 = f3.Get("bar-muon-tuple/DecayTree")
t3.SetBranchStatus("*",0)
t3.SetBranchStatus("Bplus_P*",1)
t3.SetBranchStatus("Kplus_P*",1)
t3.SetBranchStatus("Kplus_M",1)
t3.SetBranchStatus("Bplus_M",1)
t3.SetBranchStatus("*travelled",1)
"""



FromMeV2ToGeV2 =  1000000



bu_mass_hist = r.TH1D("bu_mass_hist","bu_mass_hist",100,2000,10000)
bu_mass_cat0_hist = r.TH1D("bu_mass_cat0_hist","bu_mass_cat0_hist",100,2000,10000)

b_sl_mass_hist = r.TH1D("b_sl_mass_hist","b_sl_mass_hist",100,2000,10000)
b_sl_mass_hist = r.TH1D("b_K1mumu_mass_hist","b_K1mumu_mass_hist",100,2000,10000)


dimuon_frombu_hist = r.TH1D("dimuon_frombu_hist", "dimuon_frombu_hist", 100, 0.011236,36);
dimuon_frombu_cat0_hist = r.TH1D("dimuon_frombu_cat0_hist", "dimuon_frombu_cat0_hist", 100, 0.011236,36);
dimuon_fromsl_hist = r.TH1D("dimuon_fromsl_hist", "dimuon_fromsl_hist", 100, 0.011236,36);

#make a little loop
for event in t1:
  bu_mass_hist.Fill(t1.Bplus_M)
  dimuon_frombu_hist.Fill(t1.Jpsi_M*t1.Jpsi_M/FromMeV2ToGeV2)
  if t1.Bplus_BKGCAT == 0 :
     bu_mass_cat0_hist.Fill(t1.Bplus_M)
     dimuon_frombu_cat0_hist.Fill(t1.Jpsi_M*t1.Jpsi_M/FromMeV2ToGeV2)

#make an other little loop
for event in t2:
  b_sl_mass_hist.Fill(t2.Bplus_M)
  dimuon_fromsl_hist.Fill(t2.Jpsi_M*t2.Jpsi_M/FromMeV2ToGeV2)


#for event in t3:
#  b_K1mumu_mass_hist.Fill(t3.Bplus_M)



bu_mass_hist.SetLineColor(591)
bu_mass_hist.SetTitle("")
bu_mass_hist.GetXaxis().SetTitle("K#mu^{+}#mu^{-} [MeV/c^{2}]")
bu_mass_hist.Draw()
bu_mass_cat0_hist.Draw("SAME")
bu_mass_cat0_hist.SetLineColor(810)
bu_mass_cat0_hist.SetFillColor(810)

b_sl_mass_hist.Draw("SAME")
bu_mass_hist.Draw("SAME")
#r.gPad.SaveAs("$HOME/www/BAE/plots/bmass.pdf")
r.gPad.SetLogy()
r.gPad.SaveAs("bmass.pdf")


dimuon_frombu_hist.Draw()
dimuon_frombu_hist.SetLineColor(591)
dimuon_frombu_cat0_hist.Draw("SAME")
dimuon_frombu_cat0_hist.SetFillColor(810)
dimuon_frombu_cat0_hist.SetLineColor(810)
dimuon_frombu_hist.SetTitle("")
dimuon_frombu_hist.GetXaxis().SetTitle("q^{2}[GeV^{2}/c^{-4}]")
dimuon_fromsl_hist.Draw("SAME")
r.gPad.SaveAs("dimuon.pdf")
