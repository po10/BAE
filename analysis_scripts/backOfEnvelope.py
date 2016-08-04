

#branching fraction of B+->K+mu+mu-
kmumu_BF = 5e-7

#number of Kmumnu signal observed 
kmumu_nSig = 5000

#Guessed branching fraction of B->KmumuX (based on table 1 from http://arxiv:1312.5364v2)
kmumuX_BF = 3e-6

#Not only take B+ BF but also B0, Lb and Bs
Bp_frac = 0.4

#Relative efficiencies (definitely going to be worse for us as we need to cut out more background, for now assume the same)
releff = 1.0

kmumuX_nSig = releff*kmumu_nSig*(kmumuX_BF/kmumu_BF)/Bp_frac

print 'guesstimated number of mumu signal',kmumuX_nSig

#Ratio of electron/muon efficiencies
electron_to_muon = 0.1

keeX_nSig = kmumuX_nSig*electron_to_muon

print 'guesstimated number of electron signal',keeX_nSig


