### source /cvmfs/sft.cern.ch/lcg/views/LCG_106_swan/x86_64-el9-gcc13-opt/setup.sh 

import sys, os, subprocess, uproot, joblib
import numpy as np
import pandas as pd
from ROOT import RDF
from sklearn.ensemble import HistGradientBoostingClassifier
import argparse
import json

cat_dict = {
           "A":0,
           "B":1,
           "C":2
           }

def load_data(file_names):
    """Load ROOT data and turn tree into a pd dataframe"""
    trees = []
    for file in file_names:
        print("Loading data from", file)
        f = uproot.open(file)
        tree = f["FinalTree"]
        trees.append(tree.arrays(library="pd"))
    data = pd.concat(trees)
    return data

def save_data(data, filename):
    data_v2 = {col: data[col].values for col in data.columns}
    with uproot.recreate(filename) as file:
        file["FinalTree"] = data_v2
    del data_v2
    print("File ROOT saved: ", filename)

#def save_data(data, fileName):
#    rdf = RDF.FromPandas(data)
#    rdf = rdf.Redefine("year", "(int) year;")
#    rdf = rdf.Redefine("category_v2", "(int) category_v2;")
#    rdf.Snapshot("FinalTree", fileName+".root")
#    print("File ROOT saved!")

def predict(data, workdir, folds, features, label):
    data_new = pd.DataFrame()
    #for control channel, I set privateMVA_mu3 as privateMVA_mu2
    features = [var.replace('privateMVA_mu3', 'privateMVA_mu2') for var in features]
    for category in cat_dict.keys():
      print("Start prediction category:", category)
      data_cat = data[data["category_v2"]==cat_dict[category]]
      for f in range(0,int(folds)):
         print(" --- Prediction fold: ", str(f))
         model = joblib.load(workdir+'/model_Cat_{}_fold{}.pkl'.format(category, str(f)))
         data_cat_fold = data_cat[data_cat["evt"]%(int(folds))==f]
         X = data_cat_fold[features]
         X = X.values
         predictions = model.predict(X)
         print(predictions)
         data_cat_fold["bdt_cv_"+label] = predictions
         data_new = pd.concat([data_new, data_cat_fold], ignore_index=True)
         del predictions
         del X
      print(data_new)
    print("Done!")
    return data_new


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--inputfile", type=str, help="(comma separated list of) Path to the TTRee file to process")
    parser.add_argument("--config", type=str, help="Path to the copy of the JSON configuration file")
    parser.add_argument("--label", type=str, help="Label to add to the 'bdt_cv' branch")
    args = parser.parse_args()
    config = args.config

    with open(config, 'r') as file:
        json_file = json.load(file)
    output_path = json_file['output_folder']
    date = json_file['date']
    label_out = json_file['label']
    out_tree_name = json_file['out_tree_name']
    pos_dir_xgboost = config.split(output_path)[0]
    folds = json_file["number_of_splits"]
    features = json_file["training_variables"]

    if not output_path.endswith("/"):
        output_path += "/"

    if not pos_dir_xgboost.endswith("/"):
        pos_dir_xgboost += "/"

    if not date.endswith("/"):
        date += "/"

    if date.startswith("/"):
        date = date[1:]

    if output_path.startswith("/"):
        output_path = output_path[1:]

    workdir = pos_dir_xgboost + output_path + label_out + "_" + date
    print(workdir)

    infile = args.inputfile.split(',')

    data = load_data(infile)
    data = predict(data, workdir, folds, features, args.label)

    outfile = infile[0].split(".root")[0]+"_"+args.label+".root"
    save_data(data, outfile)

    """
    branches_temp = [var + str(1) for var in branches_MVA] + [var + str(2) for var in branches_MVA] + [var + str(3) for var in branches_MVA]
    for v in branches_temp:
        print(v, " : ", (data[v] == -99).sum())
    
    print(len(data))
    data = data[(data[branches_temp] != -99).all(axis=1)]
    """

