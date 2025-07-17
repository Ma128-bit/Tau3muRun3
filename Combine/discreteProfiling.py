from ROOT import gROOT, TCanvas, TChain, EnableImplicitMT, TFile, TH1F, TArrow, TMath, TLegend
from ROOT import RooWorkspace, RooArgList, RooAddPdf, RooChi2Var, RooAbsData, RooCategory, RooMultiPdf, RooExtendPdf, RooRealVar, RooArgSet, RooDataSet, RooGenericPdf, RooFit
import argparse, json, os
import numpy as np

gROOT.SetBatch(True)
EnableImplicitMT()

save_at="MultiPdfPlots/"
branches = {}
categories = []
bdt_cuts = {}
year_set = 2022 #updated from argparse

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
       data_cut = branches["isMC"]+"==0"
       year_cut = branches["year"]+"=="+year_set
       if 'A' in cat:
           category_cut = branches["categ"]+"== 0"
       elif 'B' in cat:
           category_cut = branches["categ"]+"== 1"
       elif 'C' in cat:
           category_cut = branches["categ"]+"== 2"
       else: category_cut = ""

       #data
       cuts_data = data_cut + " & " + bdt_cuts[cat] + " & " + category_cut + " & " + year_cut
       data = RooDataSet("Bkg_"+cat, "Bkg_"+cat, tree, variables, cuts_data , branches["weight"] )

       #reduce to only one variable and import
       data_reduced = data.reduce(RooArgSet(mass))
       temp_ws.Import(data_reduced,RooFit.RenameVariable(branches["mass"],"m3m"))

    return temp_ws

def getGoodnessOfFit(mass, mpdf, data, name, nBinsForFit=40, i=0):
    ntoys = 1000
    name = f"{save_at}{name}_gofTest{i}.pdf"
    norm = RooRealVar("norm", "norm", data.sumEntries(), 0, 10e6)

    pdf = RooExtendPdf("ext", "ext", mpdf, norm)

    plot_chi2 = mass.frame()
    data.plotOn(plot_chi2, RooFit.Binning(nBinsForFit), RooFit.Name("data"))
    pdf.plotOn(plot_chi2, RooFit.Name("pdf"))

    npara = pdf.getParameters(data).getSize()
    chi2 = plot_chi2.chiSquare("pdf", "data", npara)
    print(
        f"[INFO] Calculating GOF for pdf {pdf.GetName()}, using {npara} fitted parameters"
    )

    if data.sumEntries() / nBinsForFit < 5:
        print("[INFO] Running toys for GOF test")
        params = pdf.getParameters(data)
        preParams = RooArgSet()
        params.snapshot(preParams)
        ndata = int(data.sumEntries())

        npass = 0
        toy_chi2 = []
        for itoy in range(ntoys):
            params.assignValueOnly(preParams)
            nToyEvents = np.random.poisson(ndata)
            binnedtoy = pdf.generateBinned(RooArgSet(mass), nToyEvents, 0, 1)
            pdf.fitTo(
                binnedtoy,
                RooFit.Minimizer("Minuit2", "minimize"),
                RooFit.Minos(0),
                RooFit.Hesse(0),
                RooFit.PrintLevel(-1),
                RooFit.Strategy(0),
            )

            plot_t = mass.frame()
            binnedtoy.plotOn(plot_t)
            pdf.plotOn(plot_t)
            chi2_t = plot_t.chiSquare(npara)
            if chi2_t >= chi2:
                npass += 1
            toy_chi2.append(chi2_t * (nBinsForFit - npara))
            del plot_t

        print("[INFO] complete")
        prob = npass / ntoys

        can = TCanvas()
        medianChi2 = np.median(toy_chi2)
        rms = np.sqrt(medianChi2)

        toyhist = TH1F(
            f"gofTest_{pdf.GetName()}.pdf",
            ";Chi2;",
            50,
            medianChi2 - 5 * rms,
            medianChi2 + 5 * rms,
        )
        for chi2_val in toy_chi2:
            toyhist.Fill(chi2_val)
        toyhist.Draw()

        lData = TArrow(
            chi2 * (nBinsForFit - npara),
            toyhist.GetMaximum(),
            chi2 * (nBinsForFit - npara),
            0,
        )
        lData.SetLineWidth(2)
        lData.Draw()
        can.SaveAs(name)

        params.assignValueOnly(preParams)
    else:
        prob = TMath.Prob(chi2 * (nBinsForFit - npara), nBinsForFit - npara)

    print(f"[INFO] GOF Chi2 in Observed =  {chi2 * (nBinsForFit - npara)}")
    print(f"[INFO] GOF p-value  =  {prob}")

    del pdf
    return prob


if __name__ == "__main__":
    log = open("discrete_profiling.log", "w")
    # Import info from user
    parser = argparse.ArgumentParser(description="config and root file, settings")
    parser.add_argument("--config", type=str, help="config name")
    parser.add_argument("--inputfile", type=str, help="path to input ntuple")
    parser.add_argument("--inputworkspace", type=str, help="path to input workspace. If set, config and inputfile are ignored and the datasets are directly taken from the ws. Useful to speed up.")
    parser.add_argument("--blind", action="store_true", help="is blind analysis")
    parser.add_argument("--year", type=str, default="2022", help="data taking year")
    args = parser.parse_args()
    year_set = args.year
    year = str(year_set)[-2:] 
    isblind = True if args.blind else False
    parse_config(args.config)
    if args.inputworkspace:
        wsfile = TFile.Open(args.inputworkspace, "read")
        temp_ws = wsfile.Get('temp_ws') 
    else:
        temp_ws = load_data(args.inputfile)

    
    for cat in categories:
        log.write("I'm in %s \n" % cat)
        fit_range = "SB1_A,SB2_A" if "A" in cat else "SB1_B,SB2_B" if "B" in cat else "SB1_C,SB2_C" if "C" in cat else "fullRange"
        sideband = "(m3m < 1.75 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.80)" if "A" in cat else "(m3m < 1.74 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.82)" if "B" in cat else "(m3m < 1.73 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.83)" if "C" in cat else "m3m > 0"
        data = temp_ws.data("Bkg_"+cat)
        mass = data.get().find("m3m")

        if isblind:
            data = data.reduce(RooArgSet(mass),sideband)
        else:
            data = data.reduce(RooArgSet(mass))

        hist = data.binnedClone('histo_'+cat)
        max_order = 3
        max_order = min(max_order, int(hist.sumEntries())-2)
        log.write("Max order: %d \n" % max_order)

        # Create workspace
        pdfs = RooWorkspace('pdfs_'+cat)
        print("Creating workspace")
        getattr(pdfs, 'import')(mass)

        c_powerlaw = RooRealVar("c_PowerLaw_{}".format(cat), "", 1, -100, 100)
        powerlaw = RooGenericPdf("PowerLaw_{}".format(cat), "TMath::Power(@0, @1)", RooArgList(mass, c_powerlaw))
        getattr(pdfs, 'import')(powerlaw)

        pdfs.factory("Exponential::Exponential_{C}({M}, alpha_{C}[-0.9, -10, 10])".format(M="m3m", C=cat))

        # Bernstein: oder n has n+1 coefficients (starts from constant)
        for i in range(1, max_order+1):
            c_bernstein = '{'+f'c_Bernstein{i}0_{cat}[1]'+','+','.join(['c_Bernstein{}{}_{}[.1, 0.0, 1.0]'   .format(i, j, cat) for j in range(1, i+1)])+'}'
            #c_bernstein = '{'+','.join(['c_Bernstein{}{}_{}[.1, 0.0, 1.0]'   .format(i, j, cat) for j in range(0, i+1)])+'}'
            #print(c_bernstein)
            #exit()
            pdfs.factory('Bernstein::Bernstein{}_{}({}, {})'.format(i, cat, "m3m", c_bernstein))

        # Chebychev: order n has n coefficients (starts from linear)
        for i in range(max_order):
            c_chebychev = '{'+','.join(['c_Chebychev{}{}_{}[-10.0, 10.0]'.format(i+1, j, cat) for j in range(i+1)])+'}'
            pdfs.factory('Chebychev::Chebychev{}_{}({}, {})'.format(i+1, cat, "m3m", c_chebychev)) 

        # Polynomial: order n has n coefficients (starts from constant)
        for i in range(2, max_order):
            c_polynomial = '{'+','.join(['c_Polynomial{}{}_{}[0, 10]'.format(i+1, j, cat) for j in range(i+1)])+'}'
            pdfs.factory('Polynomial::Polynomial{}_{}({}, {})'.format(i, cat, "m3m", c_polynomial)) 

        frame = mass.frame()
        frame.SetTitle(cat)
        binning = RooFit.Binning(38, 1.62, 2.0)
        data.plotOn(frame, binning)
        
        envelope = RooArgList("envelope")
        
        can = TCanvas()
        leg = TLegend(0.5, 0.65, 0.9, 0.9)
        
        gofmax  = -1
        gofmin = 1000
        bestfit = None
        worstfit = None
        families = ['Exponential', 'PowerLaw', 'Bernstein']

        allpdfs_list = RooArgList(pdfs.allPdfs())
        allpdfs_list = [allpdfs_list.at(j) for j in range(allpdfs_list.getSize())]

        converged = 0
        
        for j, fam in enumerate(families):
            log.write("> I'm in %s \n" % fam)

            fam_gofmax = 0
            pdf_list = [p for p in allpdfs_list if p.GetName().startswith(fam)]
            mnlls    = []
            for i, pdf in enumerate(pdf_list):
                log.write(">> Pdf: %s \n" % pdf.GetName())
                norm = RooRealVar("multipdf_nbkg_{}".format(cat), "", 10.0, 0.0, 5000.0)
                ext_pdf = RooAddPdf(pdf.GetName()+"_ext", "", RooArgList(pdf), RooArgList(norm))

                if isblind:
                    results = ext_pdf.fitTo(data,  RooFit.Save(True), RooFit.Range(fit_range), RooFit.Extended(True))
                else:
                    results = ext_pdf.fitTo(data,  RooFit.Save(True), RooFit.Extended(True))
                chi2 = RooChi2Var("chi2"+pdf.GetName(), "", ext_pdf, hist, RooFit.DataError(RooAbsData.Expected))
                mnll = results.minNll()+0.5*(i)

                gof_prob = TMath.Prob(chi2.getVal(), int(hist.sumEntries())-pdf.getParameters(data).selectByAttrib("Constant", False).getSize())
                #if few entries, use toy-based GOF
                if data.sumEntries()<100:
                    gof_prob = getGoodnessOfFit(mass, pdf, data, cat+f"{i}{j}", 20, i)
                fis_prob = TMath.Prob(2.*(mnlls[-1]-mnll), i-converged) if len(mnlls) else 0
                if results.covQual()==3:
                    mnlls.append(mnll)
                    converged = i

                log.write(">>> %s chi2 %f \n" % (pdf.GetName(), chi2.getVal()) )
                log.write(">>> results.covQual(): %f \n" % results.covQual())
                log.write(">>> fis_prob: %f \n" % fis_prob)
                log.write(">>> gof_prob: %f \n" % gof_prob)

                if (gof_prob > 0.01 and fis_prob < 0.1 and results.covQual()==3) or ("Exponential" in pdf.GetName()):
                #if (fis_prob < 0.1) or ("Exponential" in pdf.GetName()):
                    if gof_prob > gofmax:
                        gofmax = gof_prob
                        bestfit = pdf.GetName()
                    if gof_prob < gofmin:
                        gofmin = gof_prob
                        worstfit = pdf.GetName()

                    envelope.add(pdf)

                    log.write(">>> "+pdf.GetName()+" added to envelope \n")
                    print(">>>", pdf.GetName(), " added to envelope")
                    print("gof_prob:", gof_prob, " fis_prob:", fis_prob, " mnll: ",mnll)
                    ext_pdf.plotOn(frame, RooFit.LineColor(envelope.getSize()), RooFit.Name(pdf.GetName()),
                                RooFit.NormRange(fit_range if isblind else "full_range"),
                                RooFit.Range(fit_range if isblind else "full_range"))
                #elif fis_prob >= 0.1:
                #    break
                del chi2 
        for pdf in [envelope.at(i) for i in range(envelope.getSize())]:
            #if worst_fit==True:
            #    leg.AddEntry(frame.findObject(pdf.GetName()), pdf.GetName()+" (worstfit)" if worstfit==pdf.GetName() else pdf.GetName(), "l")
            #else:
            leg.AddEntry(frame.findObject(pdf.GetName()), pdf.GetName()+" (bestfit)" if bestfit==pdf.GetName() else pdf.GetName(), "l")

        frame.Draw()
        leg.Draw("SAME")
        can.Update()

        if not os.path.exists("MultiPdfWorkspaces"):
            os.makedirs("MultiPdfWorkspaces")
        if not os.path.exists("MultiPdfPlots"):
            os.makedirs("MultiPdfPlots")

        can.SaveAs("MultiPdfPlots/multipdf_"+year+"_"+cat+".png")

        roocat = RooCategory("multipdf_bkg_cat_{}_{}".format(year, cat), "")
        multipdf = RooMultiPdf("multipdf_bkg_{}_{}".format(year, cat), "", roocat, envelope)
        #indexing Expo in the multipdf. Change line below to switch to "bestfit"
        #roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index('Exponential_{}'.format(cat)))
        if bestfit is not None:
            roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index(bestfit))
        else:
            print(len(envelope))
            exit()
            roocat.setIndex([envelope.at(i).GetName() for i in range(envelope.getSize())].index(0))

        output = TFile.Open("MultiPdfWorkspaces/workspace_"+year+"_"+cat+".root","recreate")
        print("Creating workspace")
        w = RooWorkspace('w')
        getattr(w, 'import')(envelope)
        getattr(w, 'import')(multipdf)
        getattr(w, 'import')(roocat) 
        #getattr(w, 'import')(norm) 
        w.Print()
        w.Write()
        output.Close()
        
        del w
        del output
        del roocat
        del multipdf
        del hist
        del pdfs
        del data

    log.close()
