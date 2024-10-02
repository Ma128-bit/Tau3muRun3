from python_analysis import *
import ROOT
import sys
import argparse
import uproot
import pandas as pd
import awkward as ak

def main():
    parser = argparse.ArgumentParser(
                        prog='ProgramName',
                        description='Analysis tau3mu control channel (DsPhiPi)',
                        epilog='Text at the bottom of help')
    parser.add_argument('-n','--narg')           # positional argument
    parser.add_argument('-t','--type')      # option that takes a value
    parser.add_argument('-d','--data')      # option that takes a value
    args = parser.parse_args()
    print(args.type)
    #print(args.filename, args.count, args.verbose)
    fileout = ""

    tree = ROOT.TTree()
    print(args.type)
    type = args.type
    print(f"type: {type}\n")
    datasetName = args.data
    print(f"datasetName : {datasetName}\n")

    if type == "data_control":
        print("Control channel analysis on data\n")
        print(f"Data {datasetName}")
        chain = pd.DataFrame()
        #chain = ROOT.TChain("Tree3Mu/ntuple")
        file = uproot.open("/lustre/cms/store/user/fnenna/ParkingDoubleMuonLowMass7/SkimDsPhiPi_2024eraF_stream7_Mini_v3/240917_162014/0001/Tree_PhiPi_1179.root")
        tree = file["Tree3Mu"]
        new = tree["ntuple"].arrays(library= "pd")
        chain = pd.concat([chain, new])
        fileout = "AnalysedTree_data_control_2024W_control1419.root"
        #class_data = Extended_MyAnalizerControl2(chain, fileout)
        #class_data.Loop_DsPhiPi(type, datasetName)
        Loop_DsPhiPi(chain, type, datasetName, fileout)
    else: 
        print("Input not valid, analysis has not be developped for not control channel")


if __name__ == "__main__":
    main()