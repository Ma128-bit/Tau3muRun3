from ROOT import gROOT, gPad, TCanvas, TLatex, TLegend, TChain, EnableImplicitMT, RooRealVar, RooArgSet, RooDataSet, RooJohnson, RooFit, RDataFrame, gInterpreter, RooExtendPdf, TFile, TH1, gStyle
from ROOT import TCut, RooSimultaneous, RooFormulaVar, RooCategory, RooWorkspace, RooArgList, RooAddPdf, RooExponential, RooGaussian, RooCBShape, RooNumber, RooVoigtian, RooStats
import ctypes
import argparse, os
import numpy as np 
import CMSStyle as CMS

gROOT.SetBatch(True)
EnableImplicitMT(16)
gStyle.SetOptStat(True)
TH1.SetDefaultSumw2()

branches = {}
categories = []
bdt_cuts = {}
year_set = 2022 #updated from argparse
year_lab = 22 #updated from argparse
label = ""

def parse_config(configfile):
    with open(configfile) as f:
        lines = f.readlines()

        #hardcoded dictionary containing branch names (to accomodate changes across different minitrees)
        branch_names = lines[0].rstrip().split(',')
        branches["tree"]   = branch_names[0]
        branches["mass"]   = branch_names[1]
        branches["bdt"]    = branch_names[2]
        branches["categ"]  = branch_names[3]
        branches["isMC"]   = branch_names[4]
        branches["weight"] = branch_names[5]
        branches["year"]   = branch_names[6]

        #list of subcategories
        categories.extend(lines[1].rstrip().split(','))

        #list of bdt cuts. working points parsed from config file
        bdt_wp = lines[2].rstrip().split(',')
        for i, cat in enumerate(categories):
            if i<3:
                bdt_cuts[cat] = "{0}>".format(branches["bdt"]) + bdt_wp[i]
            else:
                bdt_cuts[cat] = "{0}<={1} && {0}>{2}".format(branches["bdt"], bdt_wp[i-3], bdt_wp[i])
       # print(branches)
       # print(categories)
       # print(bdt_cuts)

def load_data(inputfile):

    temp_ws = RooWorkspace('temp_ws')

    tree = TChain(branches["tree"])
    tree.AddFile(inputfile)

    mass = RooRealVar(branches["mass"], branches["mass"], 1.62, 2.0)
    bdt =  RooRealVar(branches["bdt"],  branches["bdt"], -0.1, 1.1)
    categ = RooRealVar(branches["categ"],  branches["categ"], 0, 2) #mass resolution category 0=A, 1=B, 2=C
    isMC  = RooRealVar(branches["isMC"],   branches["isMC"], 0, 4) #0=data, 1=Ds, 2=Bu, 3=Bd, 4=W
    weight = RooRealVar(branches["weight"], branches["weight"], 0, 1) #normalization * MC corrections
    year = RooRealVar(branches["year"], branches["year"], 2016, 2025)

    variables = RooArgSet(mass)
    variables.add(bdt)
    variables.add(categ)
    variables.add(isMC)
    variables.add(weight)
    variables.add(year)

    mass.setRange("SB1_A",1.62,1.75)
    mass.setRange("SB2_A",1.80,2.0)
    mass.setRange("SB1_B",1.62,1.74)
    mass.setRange("SB2_B",1.82,2.0)
    mass.setRange("SB1_C",1.62,1.73)
    mass.setRange("SB2_C",1.83,2.0)

    mass.setRange("SIG_A",1.75,1.80) #12MeV sigma
    mass.setRange("SIG_B",1.74,1.82) #19MeV sigma
    mass.setRange("SIG_C",1.73,1.83) #23MeV sigma
    mass.setRange("fullRange",1.62,2.0)

    for i, cat in enumerate(categories):
       MC_cut = branches["isMC"]+">0"
       data_cut = branches["isMC"]+"==0"
       year_cut = branches["year"]+"=="+year_set
       if 'A' in cat:
           category_cut = branches["categ"]+"== 0"
       elif 'B' in cat:
           category_cut = branches["categ"]+"== 1"
       elif 'C' in cat:
           category_cut = branches["categ"]+"== 2"
       else: category_cut = ""

       #MC
       cuts = MC_cut + " & " + bdt_cuts[cat] + " & " + category_cut + " & " + year_cut
       MC = RooDataSet("Sig_"+cat, "Sig_"+cat, tree, variables, cuts , branches["weight"] )

       #data
       cuts_data = data_cut + " & " + bdt_cuts[cat] + " & " + category_cut + " & " + year_cut
       data = RooDataSet("Bkg_"+cat, "Bkg_"+cat, tree, variables, cuts_data , branches["weight"] )

       #reduce to only one variable and import
       MC_reduced = MC.reduce(RooArgSet(mass))
       data_reduced = data.reduce(RooArgSet(mass))
       temp_ws.Import(data_reduced,RooFit.RenameVariable(branches["mass"],"m3m"))
       temp_ws.Import(MC_reduced,RooFit.RenameVariable(branches["mass"],"m3m"))

    os.makedirs("Workspaces", exist_ok=True)
    output = TFile.Open("Workspaces/temp_ws_"+year_lab+".root","recreate")
    print("Writing temporary workspace")
    temp_ws.Write()
    output.Close()
    return temp_ws

def bkg_model(temp_ws, final_ws, ismultipdf, isblind):

    for i, cat in enumerate(categories):
       dataset = temp_ws.data("Bkg_"+cat)
       mass = dataset.get().find("m3m")
       print("Dataset events: ",dataset.sumEntries())
       if isblind:
          fit_range = "SB1_A,SB2_A" if "A" in cat else "SB1_B,SB2_B" if "B" in cat else "SB1_C,SB2_C" if "C" in cat else "fullRange"
       else:
          fit_range = "fullRange"

       if ismultipdf==True:
          print("****************** MultiPDF ******************")
          multipdfFile = TFile.Open("MultiPdfWorkspaces/workspace_"+year_lab+"_"+cat+".root","read")
          ws = multipdfFile.Get('w')
          bkg_multi_pdf = ws.pdf("multipdf_bkg_"+year_lab+"_"+cat)
          bkg_pdf = bkg_multi_pdf.getCurrentPdf()
       else:
          alpha = RooRealVar("expo_slope_"+year_lab+"_"+cat, "expo_slope_"+year_lab+"_"+cat, -0.9, -10, 10)
          bkg_pdf = RooExponential("expo_bkg_"+year_lab+"_"+cat, "expo_bkg_"+year_lab+"_"+cat, mass, alpha)

       pdf_norm = RooRealVar("nbkg_"+cat, "nbkg_"+cat, 10.0, 0.0, 50000.0)
       bkg_modl = RooAddPdf("bkg_model_"+cat, "bkg_model_"+cat, RooArgSet(bkg_pdf), RooArgSet(pdf_norm))
       #bkg_modl = RooExtendPdf("bkg_model_"+cat, "bkg_model_"+cat, bkg_pdf, pdf_norm, "full_range") #RooExtendPdf doesn't handle normalization correclty
       bkg_modl.fitTo(dataset, RooFit.Range(fit_range), RooFit.PrintLevel(-1))
       print("Bkg events from fit: ", pdf_norm.getVal())

       ### #### use in case of RooExtendPdf!!
       ### #get integral over fit range and infer yield
       ### norm_full = bkg_pdf.createIntegral(RooArgSet(mass), RooFit.Range("fullRange")).getVal()
       ### norm_sb   = bkg_pdf.createIntegral(RooArgSet(mass), RooFit.Range(fit_range)).getVal()
       ### n_full    = pdf_norm.getVal() * (norm_full / norm_sb)
       ### print(f"Inferred number of events in full range: {n_full}")

       ### #update pdf_norm to match the full range yield -> this will be used to generate the Asimov
       ### pdf_norm.setVal(pdf_norm.getVal() * (norm_full / norm_sb))
       ### #######

       #save extended pdf to temp ws only for plotting purposes
       getattr(temp_ws, 'import')(bkg_modl)

       #save bkg model to final workspace
       getattr(final_ws, 'import')(mass)
       if ismultipdf == True:
          bkg_multi_pdf.SetName("multipdf_bkg_"+year_lab+"_"+cat)
          getattr(final_ws, 'import')(bkg_multi_pdf)
          #pdf_norm.SetName("multipdf_bkg_"+year_lab+"_"+cat+"_norm")
          #getattr(final_ws, 'import')(pdf_norm)
       else:
          bkg_pdf.SetName("expo_bkg_"+year_lab+"_"+cat)
          getattr(final_ws, 'import')(bkg_pdf)
          #getattr(final_ws, 'import')(pdf_norm)

       #save data to workspace (if blind, save toys)
       if isblind==True:
          toy_data = RooStats.AsymptoticCalculator.GenerateAsimovData(bkg_modl, RooArgSet(mass))
          toy_data.SetName("data_obs_"+year_lab+"_"+cat)
          print("Asimov events: ",toy_data.sumEntries())
          getattr(final_ws, 'import')(toy_data)
       else:
          dataset.SetName("data_obs_"+year_lab+"_"+cat)
          getattr(final_ws, 'import')(dataset)

def signal_model(temp_ws, final_ws):
    #the signal shapes are fitted separately for the eta categories A, B, C
    #the subcategories A1, A2, A3 shape some parameters and are fitted simultaneously
    for etacat in ["A", "B", "C"]:
        print("*********** Signal Model in category "+etacat+" ***********")
        subcat = RooCategory("subcat", "subcat")
        samplemap = {}
        for i, cat in enumerate(categories):
           if etacat in cat: #e.g. A1, A2, A3
              subcat.defineType(cat)
              dataset = temp_ws.data("Sig_"+cat)
              mass = dataset.get().find("m3m")
              samplemap[cat] = dataset

        #construct combined dataset in (mass,subcat)
        combData = RooDataSet(
            "combData",
            "combined data",
            {mass},
            Index=subcat,
            Import=samplemap )

        #construct a simultaneous pdf using category "subcat" as index
        simPdf = RooSimultaneous("simPdf", "sim pdf", subcat)

        #parameters in common
        sig_m0    =  RooRealVar("sig_m0_"+etacat, "sig_m0_"+etacat, 1.776, 1.775, 1.778)
        sig_alpha =  RooRealVar("sig_alpha_"+etacat, "sig_alpha_"+etacat, 1, -10., 10.)
        sig_n     =  RooRealVar("sig_n_"+etacat, "sig_n_"+etacat, 1.0, 0.0, 200.0)

        #parameters not common
        sig_gauss_sigma = [None]*3
        sig_cb_sigma = [None]*3
        sig_f = [None]*3
        #shapes
        sig_pdf_cb = [None]*3
        sig_pdf_gauss = [None]*3
        sig_model = [None]*3
        j = 0
        for i, cat in enumerate(categories):
           if etacat in cat: #e.g. A1, A2, A3
              #parameters not in common
              sig_gauss_sigma[j] =  RooRealVar("sig_gauss_sigma_"+cat, "sig_gauss_sigma_"+cat, 0.010, 0.00001, 0.8)
              sig_cb_sigma[j]    =  RooRealVar("sig_cb_sigma_"+cat, "sig_cb_sigma_"+cat, 0.010, 0.00001, 0.8)
              sig_f[j] =  RooRealVar("sig_f_"+cat, "sig_f_"+cat, 0.5, 0.0, 1.0)

              sig_pdf_cb[j] = RooCBShape("sig_CB_"+cat, "sig_CB_"+cat, mass, sig_m0, sig_cb_sigma[j], sig_alpha, sig_n)
              sig_pdf_gauss[j] = RooGaussian("sig_GS_"+cat, "sig_GS_"+cat, mass, sig_m0, sig_gauss_sigma[j])
              sig_model[j] = RooAddPdf("sig_model"+cat, "sig_model"+cat, RooArgList(sig_pdf_cb[j], sig_pdf_gauss[j]), sig_f[j])

              #associate model with the categories
              simPdf.addPdf(sig_model[j], cat)
              j = j+1

        fitResult = simPdf.fitTo(combData, Save=True)
        fitResult.Print()

        j = 0
        for i, cat in enumerate(categories):
           if etacat in cat: #e.g. A1, A2, A3
              #import fitted pdf to temp_ws for plotting purposes only
              getattr(temp_ws, 'import')(sig_model[j]) 

              #we introduce a correction to the mean and CB sigma
              sig_m0_unc = RooRealVar("sig_mean_"+year_lab+"_"+etacat, "sig_mean_"+year_lab+"_"+etacat, 0.0, -5, 5)
              sig_m0_unc.setVal(0.0)
              sig_m0_formula = RooFormulaVar("sig_m0_corr_"+cat, "(1+0.0015*{0})*{1}".format("sig_mean_"+year_lab+"_"+etacat, sig_m0.getVal()*0.9985), RooArgList(sig_m0_unc))

              sig_cb_sigma_unc = RooRealVar("sig_width"+year_lab+"_"+etacat, "sig_width"+year_lab+"_"+etacat, 0.0, -5, 5)
              sig_cb_sigma_unc.setVal(0.0)
              sig_cb_sigma_formula = RooFormulaVar("sig_cb_sigma_corr_"+cat, "(1+0.08*{0})*{1}".format("sig_width"+year_lab+"_"+etacat, sig_cb_sigma[j].getVal()), RooArgList(sig_cb_sigma_unc))

              #fix the range for all parameters by recreating them
              m0 = RooRealVar("sig_m0_"+etacat, "sig_m0_"+etacat, sig_m0.getVal(), sig_m0.getVal(), sig_m0.getVal())
              m0.setError(sig_m0.getError())
              alpha = RooRealVar("sig_alpha_"+etacat, "sig_alpha_"+etacat, sig_alpha.getVal(), sig_alpha.getVal(), sig_alpha.getVal())
              alpha.setError(sig_alpha.getError())
              n = RooRealVar("sig_n_"+etacat, "sig_n_"+etacat, sig_n.getVal(), sig_n.getVal(), sig_n.getVal())
              n.setError(sig_n.getError())
              gauss_sigma = RooRealVar("sig_gauss_sigma_"+cat, "sig_gauss_sigma_"+cat, sig_gauss_sigma[j].getVal(), sig_gauss_sigma[j].getVal(), sig_gauss_sigma[j].getVal())
              gauss_sigma.setError(sig_gauss_sigma[j].getError())
              cb_sigma = RooRealVar("sig_cb_sigma_"+cat, "sig_cb_sigma_"+cat, sig_cb_sigma[j].getVal(), sig_cb_sigma[j].getVal(), sig_cb_sigma[j].getVal())
              cb_sigma.setError(sig_cb_sigma[j].getError())
              f = RooRealVar("sig_f_"+cat, "sig_f_"+cat, sig_f[j].getVal(), sig_f[j].getVal(), sig_f[j].getVal())
              f.setError(sig_f[j].getError())

              #recreate the signal shape using the two RooFormulaVar and the fixed params
              final_pdf_cb = RooCBShape("sig_CB_"+cat, "sig_CB_"+cat, mass, sig_m0_formula, sig_cb_sigma_formula, alpha, n)
              final_pdf_gauss = RooGaussian("sig_GS_"+cat, "sig_GS_"+cat, mass, sig_m0_formula, gauss_sigma)
              final_model = RooAddPdf("sig_model_"+year_lab+"_"+cat, "sig_model_"+year_lab+"_"+cat, RooArgList(final_pdf_cb, final_pdf_gauss), f)
              j = j+1

              #import to workspace
              getattr(final_ws, 'import')(final_model)

    getattr(final_ws, 'import')(mass)

    #set parameters constant
    it = final_ws.allVars().createIterator()
    all_vars = [it.Next() for _ in range(final_ws.allVars().getSize())]
    for var in all_vars:
       if "sig_" in var.GetName():
          print(var.GetName())
          var.setConstant(True)


def plotMC(temp_ws, final_ws):
    os.makedirs("Plots", exist_ok=True)
    for i, cat in enumerate(categories):
       fitted_model = temp_ws.pdf("sig_model"+cat)
       dataset = temp_ws.data("Sig_"+cat)
       mass = temp_ws.var("m3m")
       corrected_model = final_ws.pdf("sig_model_"+year_lab+"_"+cat)
       plot = mass.frame()
       plot.SetTitle("Signal Category "+cat)
       can = TCanvas("c2", "c2", 800, 800)
       dataset.plotOn(plot, RooFit.MarkerColor(1), RooFit.MarkerStyle(6), RooFit.MarkerSize(0.75))
       fitted_model.paramOn(plot, RooFit.Layout(0.5, 0.9, 0.9))
       fitted_model.plotOn(plot, RooFit.LineColor(2), RooFit.LineWidth(2))
       #corrected_model.paramOn(plot, RooFit.Layout(0.5, 0.9, 0.4))
       corrected_model.plotOn(plot, RooFit.LineColor(4), RooFit.LineWidth(2))
       plot.Draw()

       leg = TLegend(0.1,0.70,0.4,0.86)
       leg.AddEntry(plot.getObject(0),"MC Signal (B=10^{-7})","LPE");
       leg.AddEntry(plot.getObject(2),"Signal Model","L");
       leg.AddEntry(plot.getObject(1),"After mass/scale correction","L");
       leg.SetBorderSize(0)
       leg.SetFillStyle(0)
       leg.SetTextSize(0.029)
       leg.Draw()

       #add chi2 on canvas
       chi2 = TLatex(0.55,0.5, "\\chi^{2}\\text{/NDOF} = "+str(round(plot.chiSquare(),2)) )
       chi2.SetTextSize(0.04)
       chi2.SetNDC(1)
       chi2.Draw("same")

       can.Update()
       can.SaveAs("Plots/Signal_"+cat+"_"+year_lab+"_"+label+".png")
       del can
       del plot


def plot(temp_ws, final_ws, ismultipdf, isblind):
    binning = RooFit.Binning(38, 1.62, 2.0)
    os.makedirs("Plots", exist_ok=True)
    for i, cat in enumerate(categories):
       mass = final_ws.var("m3m")
       sig_data  = temp_ws.data("Sig_"+cat) #needed to normalize MC shape
       sig_model = final_ws.pdf("sig_model_"+year_lab+"_"+cat)
       bkg_model = temp_ws.pdf("bkg_model_"+cat)
       if ismultipdf==True:
          bkg_pdf = final_ws.pdf("multipdf_bkg_"+year_lab+"_"+cat)
       else:
          bkg_pdf = final_ws.pdf("expo_bkg_"+year_lab+"_"+cat)
       if isblind==True:
          fit_range = "SB1_A,SB2_A" if "A" in cat else "SB1_B,SB2_B" if "B" in cat else "SB1_C,SB2_C" if "C" in cat else "fullRange"
          data = temp_ws.data("Bkg_"+cat)
          sideband = "(m3m < 1.75 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.80)" if "A" in cat else "(m3m < 1.74 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.82)" if "B" in cat else "(m3m < 1.73 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.83)" if "C" in cat else "m3m > 0"
          data = data.reduce(RooArgSet(mass),sideband)
       else:
          data = final_ws.data("data_obs_"+year_lab+"_"+cat) #if blind, this is asimov toy
          fit_range = "fullRange"
       plot = mass.frame()
       plot.SetTitle("Category "+cat)
       can = TCanvas("c2", "c2", 800, 800)
       sig_data.plotOn(plot, RooFit.MarkerColor(0), RooFit.LineColor(0), RooFit.FillColor(0), RooFit.FillStyle(4000), RooFit.MarkerSize(0.0), RooFit.DrawOption('B'), RooFit.XErrorSize(0), binning) #not visible
       sig_model.plotOn(plot, RooFit.LineColor(2), RooFit.LineWidth(2), RooFit.Name("sig_pdf"))
       data.plotOn(plot, RooFit.MarkerColor(1),RooFit.MarkerSize(1.0), RooFit.LineWidth(2), RooFit.Name("data"), binning)
       bkg_pdf.plotOn(plot, RooFit.Range("fullRange"), RooFit.NormRange(fit_range), RooFit.LineColor(4), RooFit.LineWidth(2), RooFit.MoveToBack(), RooFit.Name("bkg_pdf"))
       plot.Draw()

       #apply CMS style
       CMS.setTDRStyle()
       x_txt = 0.50
       margin = 0.12

       #latex
       latex = TLatex()
       latex.SetNDC()
       latex.SetTextAlign(12)
       latex.SetTextSize(0.05)
       latex.SetTextFont(42)
       latex.SetTextColor(1)

       #legend
       legend = TLegend(x_txt, 0.60, 0.90, 0.80)
       legend.SetBorderSize(0)
       legend.SetFillStyle(0)
       legend.SetTextSize(0.04)
       legend.SetTextFont(42)
       legend.AddEntry(plot.findObject('data'), 'Data', 'lep')
       legend.AddEntry(plot.findObject('bkg_pdf'), 'Background-only fit', 'l')
       legend.AddEntry(plot.findObject('sig_pdf'), 'Signal (B(#tau(3#mu)) = 10^{-7})', 'l')
       legend.Draw("same")

       #frame settings
       plot.SetMaximum(1.5*plot.GetMaximum())
       plot.SetMinimum(0.00)
       #plot.GetYaxis().SetTitleOffset(1.4)
       plot.GetYaxis().SetTitleSize(0.05)
       plot.GetYaxis().SetLabelSize(0.045)

       #plot.GetXaxis().SetTitleOffset(1.2)
       plot.GetXaxis().SetTitleSize(0.05)
       plot.GetXaxis().SetLabelSize(0.045)
       plot.GetXaxis().SetTitle("m_{3#mu} (GeV)")
       plot.GetYaxis().SetTitle("Events / 10 MeV")

       #canvas and text
       gPad.SetMargin(margin,0.05,margin,0.07) # left, right, bottom, top
       latex.DrawLatex(x_txt, 0.85, f'#bf{{HF Category {cat}}}')
       CMS.setCMSLumiStyle(can, 
          iPosX=11, 
          era=year_set, 
          extra='Preliminary')

       can.Update()
       can.SaveAs("Plots/Category_"+cat+"_"+year_lab+"_"+label+".png")
       del can
       del plot

def write_datacard(temp_ws, final_ws, ismultipdf, isblind):
    for i, cat in enumerate(categories):
        #take rates from workspaces
        with open("datacards"+year_lab+"_"+label+"/datacard_"+cat+".txt", 'w') as card:
            card.write(
            '''
imax 1 number of bins
jmax 1 number of processes minus 1
kmax * number of nuisance parameters
--------------------------------------------------------------------------------
shapes bkg           HF_{bin_name}       ../workspaces{year}/workspace_{year}_{label}.root ws_hf_{year}:{bkg_pdf}
shapes sig           HF_{bin_name}       ../workspaces{year}/workspace_{year}_{label}.root ws_hf_{year}:sig_model_{bin_name}
shapes data_obs      HF_{bin_name}       ../workspaces{year}/workspace_{year}_{label}.root ws_hf_{year}:data_obs_{bin_name}
--------------------------------------------------------------------------------
bin               HF_{bin_name}
observation       {obs:d}
--------------------------------------------------------------------------------
bin                                     HF_{bin_name}       HF_{bin_name}
process                                 sig                 bkg
process                                 0                   1
rate                                    {sig_rate:.4f}      {bkg_rate:.2f}
--------------------------------------------------------------------------------
BR_dstaunu  lnN                       1.03               -   
BR_dsmmp    lnN                       1.08               -   
BR_bds      lnN                       1.05               -   
BR_btau     lnN                       1.03               -   
BR_dscal    lnN                       1.03               -   
BR_bscal    lnN                       1.04               -   
CMS_mc_norm_dsmmp_{year}    lnN       {mc_norm_dsmmp}    -
CMS_mc_norm_bds_{year}      lnN       {mc_norm_bds}      -
CMS_eff_bdt_{year}          lnN       {eff_bdt}          -
CMS_eff_m_triggerhlt_{year} lnN       {eff_hlt}          -
CMS_eff_m_triggerl1_{year}  lnN       {eff_l1}           -
CMS_eff_m_reco_{year}       lnN       {muon_reco}        -
CMS_eff_trk_reco_{year}     lnN       {trk_reco}         -
CMS_eff_m_accept            lnN       {accept}           -
--------------------------------------------------------------------------------
bkg_rate_{bin_name} rateParam  HF_{bin_name}  bkg  1. [0.99,1.01]
bkg_rate_{bin_name} flatParam
signal_mean_{bin_name_eta}  param  0.0 1.0
signal_width_{bin_name_eta} param  0.0 1.0
'''.format(
               label = label,
               year = year_lab,
               bin_name = year_lab+"_"+cat,
               bin_name_eta = str(year_lab+"_"+cat)[:4], #to get 22_A instead of 22_A1
               bkg_pdf = "multipdf_bkg_"+year_lab+"_"+cat if ismultipdf else "expo_bkg_"+year_lab+"_"+cat,
               obs = -1 if isblind else final_ws.data("data_obs_"+year_lab+"_"+cat).sumEntries(),
               bkg_rate = temp_ws.var("nbkg_"+cat).getVal(), #in temp_ws we save the extended pdf that brings the normalization info
               sig_rate = temp_ws.data("Sig_"+cat).sumEntries(), #weighted sum of MC entries
               sig_rate_var = temp_ws.data("Sig_"+cat).sumEntries(), #weighted sum of MC entries
               mc_norm_dsmmp = "1.06" if year_set==2022 else "1.03", #normalisation factor computed on control channel
               mc_norm_bds   = "1.07" if year_set==2022 else "1.07",   #B/D ratio
               eff_bdt       = "1.10" if year_set==2022 else "1.10",   #Uncertainty on the BDT data/MC correction
               eff_hlt       = "1.02" if year_set==2022 else "1.02",   #HLT is not identical in control and signal channels
               eff_l1        = "1.01" if year_set==2022 else "1.03",   #L1 TripleMu seeds are not used for control channel
               muon_reco     = "1.02" if year_set==2022 else "1.02",   #muon reconstruction and ID scale factors
               trk_reco      = "1.025" if year_set==2022 else "1.029",   #track reconstruction efficiency (TRK POG)
               accept        = "1.07",   #3mu/2mu acceptace ratio is checked for different generators
               )
            )
            if ismultipdf: 
               card.write("multipdf_bkg_cat_{bin_name} discrete".format(bin_name = year_lab+"_"+cat))
            else:
               card.write("{slope_name}    param  {slopeval:.4f} {slopeerr:.4f}".format(
                slope_name = "expo_slope_"+year_lab+"_"+cat,
                slopeval   = final_ws.var("expo_slope_"+year_lab+"_"+cat).getVal(),
                slopeerr   = final_ws.var("expo_slope_"+year_lab+"_"+cat).getError()
                ))

if __name__ == "__main__":
    # Import info from user
    parser = argparse.ArgumentParser(description="config and root file, settings")
    parser.add_argument("--config", type=str, help="config name")
    parser.add_argument("--inputfile", type=str, help="path to input ntuple")
    parser.add_argument("--inputworkspace", type=str, help="path to input workspace. If set, config and inputfile are ignored and the datasets are directly taken from the ws. Useful to speed up.")
    parser.add_argument("--multipdf", action="store_true", help="is multipdf")
    parser.add_argument("--blind", action="store_true", help="is blind analysis")
    parser.add_argument("--year", type=str, default="2022", help="data taking year")
    parser.add_argument("--label", type=str, default="", help="some label to identify this workspace/datacard production")
    args = parser.parse_args()

    year_set = args.year
    year_lab = str(year_set)[-2:]
    ismultipdf = True if args.multipdf else False
    isblind = True if args.blind else False
    label = args.label+"_multipdf" if ismultipdf else args.label+"_expo"
    parse_config(args.config)

    if args.inputworkspace:
        wsfile = TFile.Open(args.inputworkspace, "read")
        temp_ws = wsfile.Get('temp_ws') 
    else:
        temp_ws = load_data(args.inputfile)

    final_ws = RooWorkspace('ws_hf_'+year_lab)

    #fit data and MC
    bkg_model(temp_ws, final_ws, ismultipdf, isblind)
    signal_model(temp_ws, final_ws)

    #write workspaces and datacards
    final_ws.Print()
    os.makedirs("workspaces"+year_lab, exist_ok=True)
    output = TFile.Open("workspaces"+year_lab+"/workspace_"+year_lab+"_"+label+".root","recreate")
    print("Saving workspace in workspaces"+year_lab+"/workspace_"+year_lab+"_"+label+".root")
    final_ws.Write()
    output.Close()

    os.makedirs("datacards"+year_lab, exist_ok=True)
    write_datacard(temp_ws, final_ws, ismultipdf, isblind)

    #make and save some plots 
    plotMC(temp_ws, final_ws)
    plot(temp_ws, final_ws, ismultipdf, isblind)
