import os
import ROOT
ROOT.gROOT.SetBatch(True)
import subprocess
import argparse
import pandas as pd
import math
import cmsstyle as CMS
import argparse
import ctypes

def parse_args():
    parser = argparse.ArgumentParser(description="Plotting Triplet Mass or Decay Length Histograms")

    parser.add_argument(
        "--year",
        type=str,
        default="Run3",
        help="Year of the data you want to plot (e.g., 2022). If not specified, 2022+2023 is set"
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Input file path"
    )
    parser.add_argument(
        "--weight",
        type=str,
        help="Name of weight branch in MC, if any"
    )
    parser.add_argument(
        "--include-flow",
        dest="include_flow",
        action="store_true",
        help="Include overflow bin in the histogram (default: True)"
    )
    parser.set_defaults(include_flow=True)

    return parser.parse_args()

def set_overflow(hist):
    hist.SetBinContent(hist.GetNbinsX(), hist.GetBinContent(hist.GetNbinsX()) + hist.GetBinContent(hist.GetNbinsX() + 1))

def b_normalization(filename, year, weight, include_flow):
    directory = "b_normalization"
    os.makedirs(directory, exist_ok=True)
    file = ROOT.TFile(filename, "READ")
    datatree = file.Get("FinalTree")
    idx = 0

    #masscut = "& tripletMass>1.93 & tripletMass<2.01"
    masscut = ""
    if(year=="2022"):
        CMS.SetLumi(f"2022 1.715 ")
        extracut = " "
        yearcut = "& year == 2022 "
        idx = 1
    elif(year=="2023"):
        CMS.SetLumi(f"2023 1.344 ")
        extracut = " "
        yearcut = "& year == 2023 "
        idx = 2
    else:
        CMS.SetLumi(f"2022+2023 3.1 ")
        extracut = " "
        yearcut = " "

    if(weight):
        weight = "(nsigDs_sw*"+weight+")"
    else:
        weight = "nsigDs_sw"

    # fill histograms
    n_bins=25
    xmin = 0.0
    xmax = 1.0
    hist_data = ROOT.TH1F(f"properDecayLength{idx}", "Proper Decay length Distribution", n_bins, xmin, xmax)
    hist_prompt = ROOT.TH1F(f"properDecayLength{idx}_isprompt", "Proper Decay length Distribution", n_bins, xmin, xmax)
    hist_non_prompt = ROOT.TH1F(f"properDecayLength{idx}_isnotprompt", "Proper Decay length Distribution", n_bins, xmin, xmax)

    hist_data.SetLineColor(ROOT.kGreen)
    hist_prompt.SetLineColor(ROOT.kRed)
    hist_non_prompt.SetLineColor(ROOT.kBlue)
    hist_non_prompt.SetLineWidth(2)
    hist_prompt.SetLineWidth(2)

    fit_variable = "(bs_d2D*tripletMass/Pt_tripl)*10" #proper decay length in mm
    #fit_variable = "(bs_d2D*1.96847/Pt_tripl)*10" #proper decay length in mm
    #fit_variable = "(bs_d2D)" #BS-SV displacement in mm
    #fit_variable = "(bs_d2Dsig)" #BS-SV displacement significance

    datatree.Draw(fit_variable+">>"+f"properDecayLength{idx}", f"(isMC==0 "+yearcut+extracut+masscut+")*"+weight)
    datatree.Draw(fit_variable+">>"+f"properDecayLength{idx}_isprompt", f"(isMC>0 & decay_isPrompt==0 "+yearcut+extracut+masscut+")*"+weight)
    datatree.Draw(fit_variable+">>"+f"properDecayLength{idx}_isnotprompt", f"(isMC>0 & decay_isPrompt==1 "+yearcut+extracut+masscut+")*"+weight)

    if include_flow:
        set_overflow(hist_data)
        set_overflow(hist_prompt)
        set_overflow(hist_non_prompt)

    #normalizing histograms
    scalingMC_to1 = hist_prompt.Integral() + hist_non_prompt.Integral()
    hist_prompt.Scale(1/scalingMC_to1)
    hist_non_prompt.Scale(1/scalingMC_to1)
    hist_data.Scale(1/hist_data.Integral())

    #defining f_MC as non_prompt/total
    y_np_err = ctypes.c_double(0.)
    y_np = hist_non_prompt.IntegralAndError(1, hist_non_prompt.GetNbinsX(), y_np_err, "")
    f_MC = y_np
    f_MC_error = y_np_err.value

    #plotting
    CMS.SetExtraText("Preliminary")

    CMS.SetEnergy(13.6)
    dicanvas = CMS.cmsDiCanvas("", xmin, xmax, 0., hist_data.GetMaximum()*1.1, -6, 6, 'Decay radius (L_{xy}M/p_{T}) [mm]', "a.u.", "Pull", square=CMS.kSquare, iPos=0, extraSpace=0.1, scaleLumi=None)
    dicanvas.SetCanvasSize(1300,1500)
    dicanvas.cd(1)

    x = ROOT.RooRealVar("x", "Variable", xmin, xmax)
    roo_hist_data = ROOT.RooDataHist("roo_hist_non_prompt", "Non-Prompt Data", ROOT.RooArgList(x), hist_data)
    xframe = x.frame()
    roo_hist_data.plotOn(xframe)
    roo_hist_prompt = ROOT.RooDataHist("roo_hist_prompt", "Prompt Data", ROOT.RooArgList(x), hist_prompt)
    roo_hist_non_prompt = ROOT.RooDataHist("roo_hist_non_prompt", "Non-Prompt Data", ROOT.RooArgList(x), hist_non_prompt)

    #building pdf as (1-f)*prompt + f*non_prompt
    pdf_prompt = ROOT.RooHistPdf("pdf_prompt", "Prompt PDF", ROOT.RooArgSet(x), roo_hist_prompt)
    pdf_non_prompt = ROOT.RooHistPdf("pdf_non_prompt", "Non-Prompt PDF", ROOT.RooArgSet(x), roo_hist_non_prompt)
    f = ROOT.RooRealVar("fraction", "fraction",0.2, 0., 1.)
    pdf_sum = ROOT.RooAddPdf("totalPDF", "totalPDF", ROOT.RooArgList(pdf_non_prompt, pdf_prompt), ROOT.RooArgList(f))
    pdf_sum.fitTo(roo_hist_data, ROOT.RooFit.SumW2Error(True))

    pdf_sum.plotOn(xframe, ROOT.RooFit.LineColor(ROOT.kGreen), ROOT.RooFit.LineStyle(ROOT.kDashed))
    xframe.Draw("SAME")
    hist_prompt.Draw("HIST SAME")
    hist_non_prompt.Draw("HIST SAME")
    print(hist_non_prompt.Integral())
    print(hist_prompt.Integral())
    print(hist_data.Integral())

    dicanvas.cd(2)
    framePull = x.frame() # frame for the pulls
    framePull.SetTitle("Pulls bin-by-bin")
    framePull.addObject( xframe.pullHist(), "p" )# RooPlot has a list of objects (TObjects) that can be drawn
    framePull.SetMinimum(-6)
    framePull.SetMaximum(6)
    #ROOT.gPad.SetPad(0.,0.,1.,0.3)
    framePull.Draw("same")

    line1 = ROOT.TLine(xmin, -5, xmax, -5)  # xmin, y = -5, xmax, y = -5
    line2 = ROOT.TLine(xmin, 5, xmax, 5)  # xmin, y = -5, xmax, y = -5
    line3 = ROOT.TLine(xmin, 0, xmax, 0)  # xmin, y = -5, xmax, y = -5
    # Set the line color to red and style to dashed
    line1.SetLineColor(ROOT.kRed)
    line1.SetLineStyle(ROOT.kDashed)
    line2.SetLineColor(ROOT.kRed)
    line2.SetLineStyle(ROOT.kDashed)
    line3.SetLineColor(ROOT.kBlue)
    line3.SetLineStyle(ROOT.kDashed)
    # Draw the lines
    line1.Draw("same")
    line2.Draw("same")
    line3.Draw("same")
    dicanvas.cd(1)
    sum_pdf_dummy = ROOT.TGraph()
    sum_pdf_dummy.SetLineColor(ROOT.kGreen)
    sum_pdf_dummy.SetLineWidth(2)
    sum_pdf_dummy.SetLineStyle(ROOT.kDashed)
    legend = CMS.cmsLeg(0.50, 0.6, 0.85, 0.9)
    legend.AddEntry(roo_hist_data, "Data (sWeighted)", "lep")  # "lep" = line, error bars, points
    legend.AddEntry(hist_non_prompt, "MC D_{s} from B decays", "l")
    legend.AddEntry(hist_prompt, "MC Prompt D_{s}", "l")
    string = "Fit\;(f"
    legend.AddEntry(sum_pdf_dummy, f"{string}={f.getVal():.3f} \\pm {f.getError():.3f}"+")", "l")
    legend.Draw("SAME")
    # Create a TPaveText box just below the legend
    text_box = ROOT.TPaveText(0.50, 0.50, 0.85, 0.60, "NDC")
    text_box.SetTextFont(42)  # Set regular font
    text_box.SetTextSize(0.04)  # Adjust text size if necessary
    text_box.SetFillColor(0)  # Transparent background
    text_box.SetBorderSize(0)  # No border
    text_box.AddText(f"f_{{MC}}={f_MC:.3f} \\pm {f_MC_error:.3f}")
    text_box.Draw("SAME")
    #dicanvas.cd(1).SetLogy(True)
    dicanvas.Update()
    dicanvas.SaveAs(f"TransvProperLength_{year}.png")
    print(f"f: {f.getVal()} +/- {f.getError()}")
    dicanvas.Clear()

if __name__ == "__main__":
    args = parse_args()
    print(f"Year selected: {args.year}")
    print(f"Including overflow bin: {args.include_flow}")
    b_normalization(args.file, args.year, args.weight, args.include_flow)
