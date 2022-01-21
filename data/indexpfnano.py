import subprocess
import json

def get_children(parent):
	#print(f"DEBUG : Call to get_children({parent})")
	command = f"eos root://cmseos.fnal.gov ls -F {parent}"
	#print(command)
	result = subprocess.getoutput(command)#, stdout=subprocess.PIPE)
	#print(result)
	return result.split("\n")

def get_subfolders(parent):
	subfolders = []
	for x in get_children(parent):
		if len(x) == 0: 
			continue
		if x[-1] == "/":
			subfolders.append(x)
	return subfolders

def make_index():
prefix = "/store/user/lpcpfnano"
folders = {
	"dryu/v2_2/2017": [
		"SingleMu2017", 
		"JetHT2017", 
	], 
	"yihan/v2_2/2017": [
		"WJetsToQQ", 
		"TTbar", 
		"JetHT2017", 
	], 
	"yihan/v2_2/2018": [
		"JetHT2018", 
		"TTbar", 
	], 
	"jekrupa/v2_2/2018": [
		"JetHT2018", 
		"QCD", 
		"WJetsToQQ", 
		"ZJetsToQQ", 
	], 
	"yihan/v2_2/2016": [
		"JetHT2016", 
		"TTbar", 
		"QCD", 
	], 
	"yihan/v2_2/2016APV": [
		"TTbar", 
		"QCD", 
	], 
	"drankin/v2_2/2016": [
		"SingleElectron2016", 
		"WJetsToLNu", 
		"TTbar", 
	], 
	"drankin/v2_2/2016APV": [
		"WJetsToLNu", 
		"TTbar", 
	], 
	"drankin/v2_2/2018": [
		"EGamma2018", 
		"TTbar", 
		"WJetsToLNu", 
	], 
	"pharris/v2_2/2016": [
		"JetHT2016", 
		"SingleTop", 
	], 
	"pharris/v2_2/2017": [
		"SingleTop", 
		"JetHT2017", 
	], 
	"pharris/v2_2/2018": [
		"JetHT2018", 
		"SingleTop", 
	], 
	"cmantill/v2_2/2018": [
		"MET2018", 
		"DYJetsToLL", 
		"HTT", 
		"HWW", 
	], 
	"cmantill/v2_2/2017": [
		"MET2017", 
		"DYJetsToLL", 
		"HTT", 
		"HWWPrivate", 
		"HWW", 
	], 
	"cmantill/v2_2/2016": [
		"MET2016", 
		"DYJetsToLL", 
		"HWW", 
		"HTT", 
	], 
	"cmantill/v2_2/2016APV": [
		"DYJetsToLL", 
		"HWW", 
	], 
	"emoreno/v2_2/2016APV": [
		"TTbar", 
	], 
	"emoreno/v2_2/2016": [
		"TTbar", 
		"JetHT2016", 
	], 
	"drankin/v2_2/2017": [
		"SingleElectron2017", 
		"WJetsToLNu", 
		"TTbar", 
		"FlatTauTau", 
	], 
	"jekrupa/v2_2/2017": [
		"JetHT2017", 
		"TTbar", 
		"WJetsToQQ", 
		"ZJetsToQQ", 
		"QCD", 
		"VectorZPrime", 
	], 
	"dryu/v2_2/2016": [
		"JetHT2016", 
		"SingleMu2016", 
		"VectorZPrime", 
	], 
	"dryu/v2_2/2018": [
		"JetHT2018", 
		"SingleMu2018", 
		"VectorZPrime", 
	], 
	"dryu/v2_2_1/2017": [
		"SingleMu2017", 
	], 
	"dryu/v2_2_1/2018": [
		"SingleMu2018", 
	], 
	"dryu/v2_2_1/2016": [
		"SingleMu2016", 
	], 
	"jekrupa/v2_2/2016": [
		"JetHT2016", 
		"ZJetsToQQ", 
		"WJetsToQQ", 
	], 
	"jekrupa/v2_2/2016APV": [
		"VectorZPrime", 
		"ZJetsToQQ", 
		"WJetsToQQ", 
	], 
	"emoreno/v2_2/2017": [
		"JetHT2017", 
	], 
	"emoreno/v2_2/2018": [
		"JetHT2018", 
		"TTbar", 
	]
}
# Data path:
# .......prefix........|......f1......|.....f2.....|...f3.....|.........f4........|.....f5......|.f6.|....
# /store/user/lpcpfnano/dryu/v2_2/2017/SingleMu2017/SingleMuon/SingleMuon_Run2017C/211102_162942/0000/*root
# 
# MC path:
# /store/user/lpcpfnano/jekrupa/v2_2/2017/WJetsToQQ/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/WJetsToQQ_HT-800toInf/211108_171840/0000/*root
index = {}
for f1 in sorted(folders.keys()):
	print(f1)
	year = f1.split("/")[-1]
	if not year in index:
		index[year] = {}

	for f2 in folders[f1]:
		print(f"\t{f2}")
		sample_short = f2.replace("/", "")
		if not sample_short in index[year]:
			index[year][sample_short] = {}
		#print(f"{f1}/{f2}")
		f2_subfolders = get_subfolders(f"{prefix}/{f1}/{f2}")

		for f3 in f2_subfolders:
			#print(f"\t\tf3={f3}")
			sample_long = f3.replace("/", "")
			f3_subfolders = get_subfolders(f"{prefix}/{f1}/{f2}/{f3}")

			for f4 in f3_subfolders:
				subsample = f4.replace("/", "")
				#print(f"\t\t\t\tf4={f4}")
				if not subsample in index[year][sample_short]:
					index[year][sample_short][subsample] = []
				f4_subfolders = get_subfolders(f"{prefix}/{f1}/{f2}/{f3}/{f4}")
				if len(f4_subfolders) >= 2:
					print(f"WARNING : Found multiple timestamps for {prefix}/{f1}/{f2}/{f3}/{f4}")

				for f5 in f4_subfolders: # Timestamp
					#print(f"\t\t\t\t\tf5={f5}")
					f5_subfolders = get_subfolders(f"{prefix}/{f1}/{f2}/{f3}/{f4}/{f5}")
					for f6 in f5_subfolders: # 0000, 0001
						f6_children = get_children((f"{prefix}/{f1}/{f2}/{f3}/{f4}/{f5}/{f6}"))
						#print(f6_children)

						root_files = [f"{prefix}/{f1}/{f2}/{f3}/{f4}/{f5}/{f6}/{x}".replace("//", "/") for x in f6_children if x[-5:] == ".root"]

						index[year][sample_short][subsample].extend(root_files)
with open("pfnanoindex.json", "w") as f:
	json.dump(index, f, sort_keys=True, indent=2)