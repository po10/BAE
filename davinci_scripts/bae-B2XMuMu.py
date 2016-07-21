
"""
Authors : P.Owen, Y.Amhis 
When : July 2016
What : Option file to make MC tuples. 
First re-run the stripping, add and add a kaon. Easy enough 


"""

from Gaudi.Configuration import *
from PhysSelPython.Wrappers import Selection, SelectionSequence, DataOnDemand
from GaudiConfUtils.ConfigurableGenerators import FilterDesktop, CombineParticles



from Configurables import DecayTreeTuple, FitDecayTrees, TupleToolRecoStats, TupleToolTrigger, TupleToolTISTOS, CondDB, SelDSTWriter
from DecayTreeTuple.Configuration import *
from PhysSelPython.Wrappers import MergedSelection

# 
name = 'bukmumu'

"""
Options for building Stripping21 (was 20, but we want 21)

"""

from Configurables import EventNodeKiller
eventNodeKiller = EventNodeKiller('Stripkiller')
eventNodeKiller.Nodes = ['/Event/AllStreams','/Event/Strip']

from Gaudi.Configuration import *
MessageSvc().Format = "% F%30W%S%7W%R%T %0W%M"

# Tighten Trk Chi2 to <3
from CommonParticles.Utils import DefaultTrackingCuts
DefaultTrackingCuts().Cuts  = { "Chi2Cut" : [ 0, 4 ],
                                "CloneDistCut" : [5000, 9e+99 ] }

#
# Build the streams and stripping object
# WARNING : the Stripping version needs to be updated 
from StrippingArchive.Stripping20r0p3.StrippingB2XMuMu import B2XMuMuConf as builder
from StrippingArchive.Stripping20r0p3.StrippingB2XMuMu import defaultConfig as config

#from StrippingSettings.Utils import strippingConfiguration
#from StrippingArchive.Utils import buildStreams, cloneLinesFromStream
#from StrippingArchive import strippingArchive
config['MuonPID'] = -999999

#stripping='stripping20'
stripping = 'stripping21' 

#get the configuration dictionary from the database
#config  = strippingConfiguration(stripping)
#config['HLT_FILTER_HMuNu']=""
lb = builder('B2XMuMu',config)
print config
#get the line builders from the archive#
# Merge into one stream and run in flag mode
#
AllStreams = StrippingStream("Dimuon")

for line in lb.lines():
    print line.name()
    if line.name() == 'StrippingB2XMuMu_InclDiMuHighQ2Line':
        AllStreams.appendLines([line])
       
    if line.name() == 'StrippingB2XMuMu_InclDiMuLowQ2Line':
        AllStreams.appendLines([line])    

sc = StrippingConf( Streams = [ AllStreams ],
                    MaxCandidates = 2000
                    )





# Here we just put the output candidates in an Tuple
tuple = DecayTreeTuple("Jpsi_Tuple")
tuple.Decay = "[B0 -> ^mu+ ^mu-]CC"
tuple.Inputs = ["Phys/B2XMuMu_InclDiMuHighQ2Line/Particles"]


# But what we really want is to make a dimuon and a Kaon  
from StandardParticles import StdLooseKaons as kaons

LowQ2MuonsOnDemand = DataOnDemand(Location = "Phys/B2XMuMu_InclDiMuLowQ2Line/Particles")
HighQ2MuonsOnDemand = DataOnDemand(Location = "Phys/B2XMuMu_InclDiMuLowHighQ2Line/Particles")


bothstripping = MergedSelection("Selection_mergeddaughters",
       RequiredSelections = [LowQ2MuonsOnDemand,HighQ2MuonsOnDemand])

_filterDimuons = FilterDesktop(Code="ABSID==511") # Dimuons from B0--> mu mu stripping selection
_selDimuons= Selection( "_selDimuons", Algorithm = _filterDimuons, RequiredSelections = [bothstripping] )

# Try and make B->J/psi K
_B = CombineParticles()
_B.DaughtersCuts = { "K+" : "PT>500*MeV" }
_B.MotherCut = "(DMASS('B+')<5000*MeV) & (VFASPF(VCHI2)<25.0)" #need to check these cuts
_B.DecayDescriptors = [ "[B+ -> J/psi(1S) K+]cc" ] 


_BdecaySelection = Selection( "TurboB", Algorithm = _B, RequiredSelections = [_selDimuons,kaons] )
SeqB = SelectionSequence('SeqB', TopSelection = _BdecaySelection)

tupleB = tuple.clone("bae-muon-tuple")
tupleB.Inputs = [SeqB.outputLocation()]
tupleB.Decay = "[B+ -> J/psi(1S) K+]CC"


tuple.ToolList =  [
      "TupleToolKinematic"
    , "TupleToolEventInfo"
    , "TupleToolRecoStats"
    , "TupleToolMCTruth"
    , "TupleToolMCBackgroundInfo"
   # , "TupleBuKmmFit"
] # Probably need to add many more Tools. 


tuple.addBranches ({         
      "muplus" :  "[B0 -> ^mu+ mu-]CC",
      "muminus" :  "[B0 -> mu+ ^mu-]CC",
      "B" : "[B0 -> mu+ mu-]CC",
})



LoKi_All=tuple.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_All")
LoKi_All.Variables = {
        'MINIPCHI2' : "MIPCHI2DV(PRIMARY)", 
        'MINIP' : "MIPDV(PRIMARY)",
        'IPCHI2_OWNPV' : "BPVIPCHI2()", 
        'IP_OWNPV' : "BPVIP()"
}




LoKi_muplus=tuple.muplus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_muplus")
LoKi_muplus.Variables = {
       'PIDmu' : "PIDmu",
       'ghost' : "TRGHP",
       'TRACK_CHI2' : "TRCHI2DOF",
       'NNK' : "PPINFO(PROBNNK)",
       'NNpi' : "PPINFO(PROBNNpi)",
       'NNmu' : "PPINFO(PROBNNmu)"
}

LoKi_muminus=tuple.muminus.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_muminus")
LoKi_muminus.Variables = {
       'PIDmu' : "PIDmu",
       'ghost' : "TRGHP",
       'TRACK_CHI2' : "TRCHI2DOF",
       'NNK' : "PPINFO(PROBNNK)",
       'NNpi' : "PPINFO(PROBNNpi)",
       'NNmu' : "PPINFO(PROBNNmu)"
}


LoKi_B=tuple.B.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_B")
LoKi_B.Variables = {
       'DTF_CHI2' : "DTF_CHI2NDOF(True)",
       'TAU' : "BPVLTIME()",
       'DIRA_OWNPV' : "BPVDIRA",
       'FD_CHI2' : "BPVVDCHI2",
       'ENDVERTEX_CHI2' : "VFASPF(VCHI2/VDOF)",
}


list = [
      "L0DiMuonDecision"
    , "L0MuonDecision"
    , "Hlt1TrackAllL0Decision"
    , "Hlt1TrackMuonDecision"
    , "Hlt1DiMuonLowMassDecision"
    , "Hlt1DiMuonHighMassDecision"
    , "Hlt1SingleMuonHighPTDecision"
    , "Hlt2TopoMu2BodyBBDTDecision"
    , "Hlt2TopoMu3BodyBBDTDecision"
    , "Hlt2Topo2BodyBBDTDecision"
    , "Hlt2Topo3BodyBBDTDecision"
    , "Hlt2DiMuonDetachedDecision"
    , "Hlt2SingleMuonDecision"
    , "Hlt2DiMuonDetachedHeavyDecision"
] #Is the trigger list uptodate? 


tuple.B.ToolList += [ "TupleToolTISTOS" ]
tuple.B.addTool( TupleToolTISTOS, name = "TupleToolTISTOS" )
tuple.B.TupleToolTISTOS.Verbose = True
tuple.B.TupleToolTISTOS.TriggerList = list



dstWriter = SelDSTWriter('BuKmumuDSTWriter',
                   SelectionSequences = sc.activeStreams(),
                   OutputFileSuffix = 'Stripped')




from Configurables import DaVinci
DaVinci().TupleFile = "BuKMuMu.root"
DaVinci().EvtMax = 5000
DaVinci().DataType = '2012'
DaVinci().Simulation   = True
DaVinci().Lumi = not DaVinci().Simulation

_myseq = GaudiSequencer("myseq")
_myseq.Members += [ eventNodeKiller, sc.sequence()] #redo the stripping
_myseq.Members += [SeqB.sequence() ] # make B candidates (muon channel)
_myseq.Members += [tuple, tupleB] # put stuff in a Tuple
DaVinci().UserAlgorithms = [_myseq] # run the whole thing
DaVinci().MainOptions  = ""



"""
#we should put this back later if we want to smear stuff
from Configurables import TrackSmeared
TrackSmeared("TrackSmearing").smearBest = True
TrackSmeared("TrackSmearing").Scale = 0.5
TrackSmearingSeq = GaudiSequencer("TrackSmearingSeq")
TrackSmearingSeq.Members = [ TrackSmeared("TrackSmearing") ]
"""
