



taskname = ['MC bae']

#bu2jpsiK
#data = ['/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/12143001/ALLSTREAMS.DST']

#SL
#data = ['/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21r0p1Filtered/10010037/B2KMU.TRIGSTRIP.DST']

#K1mumu
data = ['/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/12215002/ALLSTREAMS.DST']
#data = ['/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08d/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/11102202/ALLSTREAMS.DST']



num=0

ds=BKQuery(path = data[num],dqflag = "All")
print ds.getDataset()
j = Job(
		name = taskname[num],
		backend = Dirac(),
	        application = DaVinci(version =  'v41r0',optsfile = '/afs/cern.ch/user/y/yamhis/BAE/davinci_scripts/bae-B2XMuMu.py'),  
         	splitter = SplitByFiles(
			filesPerJob = 20,
			ignoremissing = True
			),
                maxFiles = -1,
		outputfiles = [
                LocalFile('*.root'),
		],
		inputdata = ds.getDataset()
		)


j.submit()


