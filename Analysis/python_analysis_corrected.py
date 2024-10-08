import ROOT
import math
import pandas as pd
import uproot
import sys, os, time
import re
import numpy as np

NCUTS = 9
NMU = 3
    
def BestTripletFinder(df, triplIndex):
    bestChi2 = 15000000000000000
    index = 0
    for i in range(len(triplIndex)):
        if df.TripletVtx2_Chi2.iloc[0][triplIndex[i]] < bestChi2:
            bestChi2 = df.TripletVtx2_Chi2.iloc[0][triplIndex[i]]
            index = triplIndex[i]
    return index

def DimuonMass(df, mu_index1, mu_index2):
    inv = 0
    charge1 = df.MuonCharge.iloc[0][mu_index1]
    charge2 = df.MuonCharge.iloc[0][mu_index2]
    pt1 = df.MuonPt.iloc[0][mu_index1]
    pt2 = df.MuonPt.iloc[0][mu_index2]
    eta1 = df.MuonEta.iloc[0][mu_index1]
    eta2 = df.MuonEta.iloc[0][mu_index2]
    phi1 = df.MuonPhi.iloc[0][mu_index1]
    phi2 = df.MuonPhi.iloc[0][mu_index2]
    en1 = df.MuonEnergy.iloc[0][mu_index1]
    en2 = df.MuonEnergy.iloc[0][mu_index2]
    total_charge = charge1 + charge2
    if total_charge != 0: return inv
    else:
        mu1 = ROOT.TLorentzVector()
        mu1.SetPtEtaPhiE(pt1, eta1, phi1, en1)
        mu2 = ROOT.TLorentzVector()
        mu2.SetPtEtaPhiE(pt2, eta2, phi2, en2)
        mutot = ROOT.TLorentzVector()
        mutot = mu1 + mu2
        return mutot.M()
        
def DuplicateFinder(df, eta1, eta2, etaTr, phi1, phi2, phiTr, pt1, pt2, ptTr):
    if ((abs(eta1-etaTr)>0.0001 and abs(eta2-etaTr)>0.0001 and abs(phi1-phiTr)>0.0001 and abs(phi2-phiTr)>0.0001 and abs(pt1-ptTr)>0.0001 and abs(pt2-ptTr)>0.0001) and (abs(eta1-eta2)>0.0001 and abs(phi1-phi2)>0.0001 and abs(pt1-pt2)>0.0001) ):
        return True
    else: 
        return False
        
def Fill_CutName(df, listCut):
    nameCut = ["BeforeCuts", "L1_fired", "HLT_fired", "MuonID", "DiMu_mass", "TriMu_mass", "mu1_TrMatch", "mu12_TrMatch", "mu123_TrMatch"]
    #print(len(nameCut))
    #print(NCUTS)
    if len(nameCut) != NCUTS: 
        print("length of the cut names does not match number of cuts")
        return
    for i in range(NCUTS):
        listCut.append(nameCut[i])
    
def Draw_CutEffCanvas(df, canv, hist, cut, listCut):
    #print(cut)
    canv = ROOT.TCanvas("", "")
    canv.cd()
    for k in range(len(listCut)):
        hist.Fill(k+1, cut[k])
        hist.GetXaxis().SetBinLabel(k+1, listCut[k])
    hist.DrawCopy("HIST TEXT0")
    hist.Write()


def Get_MuonAndTrackVariables(df, mu_Ind): #, pt, eta, phi)
    #print(df.Mu01_Pt.iloc[0])
    pt = [df.Mu01_Pt.iloc[0][mu_Ind[0]], df.Mu02_Pt.iloc[0][mu_Ind[1]], df.Tr_Pt.iloc[0][mu_Ind[2]]]
    eta = [df.Mu01_Eta.iloc[0][mu_Ind[0]], df.Mu02_Eta.iloc[0][mu_Ind[1]], df.Tr_Eta.iloc[0][mu_Ind[2]]]
    phi = [df.Mu01_Phi.iloc[0][mu_Ind[0]], df.Mu02_Phi.iloc[0][mu_Ind[1]], df.Tr_Phi.iloc[0][mu_Ind[2]]]
    return pt, eta, phi

#def MatchIndex(df, type, ind, mu_Ind, mu):
def MatchIndex(df, type, ind):
    list_ind = [ind, ind, ind]
    pt, eta, phi = Get_MuonAndTrackVariables(df, list_ind)
    mu = []
    if type == "ID":
        for k in range(NMU-1):
            mu.append(MuonFinder(df, pt[k], eta[k], phi[k]))
        mu.append(TrackFinder(df, pt[2], eta[2], phi[2]))
    return mu

def MuonP(df, pt, eta, phi):
    muon = ROOT.TVector3()
    muon.SetPtEtaPhi(pt, eta, phi)
    return muon.Mag()

def TreeFin_Angle(df, ind):
    a_x = df.TripletVtx2_x.iloc[0][ind] - df.RefittedPV2_x.iloc[0][ind]
    a_y = df.TripletVtx2_y.iloc[0][ind] - df.RefittedPV2_y.iloc[0][ind]
    a_z = df.TripletVtx2_z.iloc[0][ind] - df.RefittedPV2_z.iloc[0][ind]
    b = ROOT.TVector3()
    b.SetPtEtaPhi(df.Triplet2_Pt.iloc[0][ind], df.Triplet2_Eta.iloc[0][ind],df.Triplet2_Phi.iloc[0][ind])
    b_x = b.Px()
    b_y = b.Py()
    b_z = b.Pz()
    a_mod = abs(df.FlightDistPVSV2.iloc[0][ind])
    b_mod = abs(b.Mag())
    cos_ang = ((a_x*b_x)+(a_y*b_y)+(a_z*b_z))/(a_mod*b_mod)
    angle = math.acos(min(max(cos_ang,-1.0),1.0))
    return angle


def TreeFin_Fill(df, jentry, df_fin, debugMode, isMC, ind, mu_Ind, mu, lumi, run, evt, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2,L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath):
    #print("il baco è qui")
    if debugMode:
        print("Ciao1")
    #mu = MatchIndex(df, "ID", ind)
    #print(mu_Ind)
    #print(df.Mu01_Pt.iloc[0])
    pt, eta, phi = Get_MuonAndTrackVariables(df, mu_Ind)#, pt, eta, phi)
    cLP = -999
    tKink = -999
    segmComp = 999
    DeltaR_max = -999
    DeltaZ_max = -999
    temp1 = []
    temp = []
    dR = []
    dZ = []
    temp1.append(df.dxy_mu1.iloc[0][mu_Ind[0]])
    temp1.append(df.dxy_mu2.iloc[0][mu_Ind[1]])
    temp1.append(df.dxy_mu3.iloc[0][mu_Ind[2]])
    dR.append(math.sqrt(pow((eta[0]-eta[1]),2)+pow((phi[0]-phi[1]),2)))
    dR.append(math.sqrt(pow((eta[0]-eta[2]),2)+pow((phi[0]-phi[2]),2)))
    dR.append(math.sqrt(pow((eta[2]-eta[1]),2)+pow((phi[2]-phi[1]),2)))
    dZ.append(abs(df.Muon_vz.iloc[0][mu[0]] - df.Muon_vz.iloc[0][mu[1]] ))
    dZ.append(abs(df.Muon_vz.iloc[0][mu[0]] - df.Track_vz.iloc[0][mu[2]] ))
    dZ.append(abs(df.Track_vz.iloc[0][mu[2]]  - df.Muon_vz.iloc[0][mu[1]] ))
    d0 = 999
    temp.append(abs(df.dxy_mu1.iloc[0][mu_Ind[0]]/ df.dxyErr_mu1.iloc[0][mu_Ind[0]]))
    temp.append(abs(df.dxy_mu2.iloc[0][mu_Ind[1]]/ df.dxyErr_mu2.iloc[0][mu_Ind[1]]))
    temp.append(abs(df.dxy_mu3.iloc[0][mu_Ind[2]]/ df.dxyErr_mu3.iloc[0][mu_Ind[2]]))
    d0sig = 999
    d0sig_max = -999
    if debugMode: print("Ciao2")
    for k in range(2):
        if (df.Muon_combinedQuality_chi2LocalPosition.iloc[0][mu[k]] > cLP): cLP = df.Muon_combinedQuality_chi2LocalPosition.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_trkKink.iloc[0][mu[k]] > tKink): tKink = df.Muon_combinedQuality_trkKink.iloc[0][mu[k]]
        if (df.Muon_segmentCompatibility.iloc[0][mu[k]] < segmComp): segmComp = df.Muon_segmentCompatibility.iloc[0][mu[k]]
        if (temp1[k] < d0): d0 = temp1[k]
        if (temp[k] < d0sig): d0sig = temp[k]
        if (temp[k] > d0sig_max): d0sig_max = temp[k]
        if (dR[k] > DeltaR_max): DeltaR_max = dR[k]
        if (dZ[k] > DeltaZ_max): DeltaZ_max = dZ[k]

    if debugMode: print("Ciao3")

    if (isMC!=0): puFactor = df.nPileUpInt.iloc[0]
    else: 
        puFactor = df.pileupFactor.iloc[0]  
    tripletMass = df.Triplet2_Mass.iloc[0][ind]
    if (tripletMass>2.1 or tripletMass<1.62):
        print(f"ECCO IL BACO !!!!\nTripletMass: {tripletMass}\nrun = {run} lumi = {lumi} evt = {evt}")
    #tripletMassReso = ResoTriplMass(mu_Ind, mu)    
    #timeAtIpInOut_sig3 = Muon_timeAtIpInOut->at(mu[2])/ Muon_timeAtIpInOutErr->at(mu[2]);
    cQ_uS = 0
    cQ_tK = 0
    cQ_gK = 0
    cQ_tRChi2 = 0
    cQ_sRChi2 = 0
    cQ_Chi2LM = 0
    cQ_Chi2LP = 0
    cQ_lD = 0
    cQ_gDEP = 0
    cQ_tM = 0
    cQ_gTP = 0
    caloComp = 999
    for k in range(2):
        if (df.Muon_combinedQuality_updatedSta.iloc[0][mu[k]] > cQ_uS): cQ_uS = df.Muon_combinedQuality_updatedSta.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_trkKink.iloc[0][mu[k]] > cQ_tK): cQ_tK = df.Muon_combinedQuality_trkKink.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_glbKink.iloc[0][mu[k]] > cQ_gK): cQ_gK = df.Muon_combinedQuality_glbKink.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_trkRelChi2.iloc[0][mu[k]] > cQ_tRChi2): cQ_tRChi2 = df.Muon_combinedQuality_trkRelChi2.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_staRelChi2.iloc[0][mu[k]] > cQ_sRChi2): cQ_sRChi2 = df.Muon_combinedQuality_staRelChi2.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_chi2LocalPosition.iloc[0][mu[k]] > cQ_Chi2LP): cQ_Chi2LP = df.Muon_combinedQuality_chi2LocalPosition.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_chi2LocalMomentum.iloc[0][mu[k]] > cQ_Chi2LM): cQ_Chi2LM = df.Muon_combinedQuality_chi2LocalMomentum.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_localDistance.iloc[0][mu[k]] > cQ_lD): cQ_lD = df.Muon_combinedQuality_localDistance.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_globalDeltaEtaPhi.iloc[0][mu[k]] > cQ_gDEP): cQ_gDEP = df.Muon_combinedQuality_globalDeltaEtaPhi.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_tightMatch.iloc[0][mu[k]] > cQ_tM): cQ_tM = df.Muon_combinedQuality_tightMatch.iloc[0][mu[k]]
        if (df.Muon_combinedQuality_glbTrackProbability.iloc[0][mu[k]] > cQ_gTP): cQ_gTP = df.Muon_combinedQuality_glbTrackProbability.iloc[0][mu[k]]
        if (df.Muon_caloCompatibility.iloc[0][mu[k]] < caloComp): caloComp = df.Muon_caloCompatibility.iloc[0][mu[k]]
    #calEn_hadMu3 = Muon_calEnergy_had->at(mu[2]);
    #fliDistPVSV_Chi2 = FlightDistPVSV_chi2->at(ind);
    '''
    //isGlb3 = Muon_isGlobal->at(mu[2]);
    //isTracker3 = Muon_isTrackerMuon->at(mu[2]);
    //isLoose3 = Muon_isLoose->at(mu[2]);
    //isSoft3 = Muon_isSoft->at(mu[2]);
    //isPF3 = Muon_isPF->at(mu[2]);
    //isRPC3 = Muon_isRPCMuon->at(mu[2]);
    //isSA3 = Muon_isStandAloneMuon->at(mu[2]);
    //isCalo3 = Muon_isCaloMuon->at(mu[2]);
    '''
    #had03 = df.Muon_hadEt03->at(mu[2])
    #had05 = df.Muon_hadEt05->at(mu[2])
    #nJets03 = df.Muon_nJets03->at(mu[2])
    #nJets05 = df.Muon_nJets05->at(mu[2])
    #nTracks03 = df.Muon_nTracks03->at(mu[2])
    #nTracks05 = df.Muon_nTracks05->at(mu[2])
    #sumPt03 = df.Muon_sumPt03->at(mu[2])
    #sumPt05 = df.Muon_sumPt05->at(mu[2])
    #hadVeto03 = df.Muon_hadVetoEt03->at(mu[2])
    #hadVeto05 = df.Muon_hadVetoEt05->at(mu[2])
    #emVeto03 = df.Muon_emVetoEt03->at(mu[2])
    #emVeto05 = df.Muon_emVetoEt05->at(mu[2])
    #trVeto03 = df.Muon_trackerVetoPt03->at(mu[2])
    #trVeto05 = df.Muon_trackerVetoPt05->at(mu[2])
    #
    #
    # mu1
    # mu3
    '''
    isQValid3 = df.Muon_isQualityValid.iloc[0][mu[2]]
    isTValid3 = df.Muon_isTimeValid.iloc[0][mu[2]]
    isIsoValid3 = df.Muon_isIsolationValid.iloc[0][mu[2]]
    GLnormChi2_mu3 = df.Muon_GLnormChi2.iloc[0][mu[2]]
    GL_nValidMuHits3 = df.Muon_GLhitPattern_numberOfValidMuonHits.iloc[0][mu[2]]
    trkLayersWMeas3 = df.Muon_trackerLayersWithMeasurement.iloc[0][mu[2]]
    nValidPixelHits3 = df.Muon_Numberofvalidpixelhits.iloc[0][mu[2]]
    outerTrk_P_3 = df.Muon_outerTrack_p.iloc[0][mu[2]]
    outerTrk_Eta_3 = df.Muon_outerTrack_eta.iloc[0][mu[2]]
    outerTrk_normChi2_3 = df.Muon_outerTrack_normalizedChi2.iloc[0][mu[2]]
    outerTrk_muStValidHits_3 = df.Muon_outerTrack_muonStationsWithValidHits.iloc[0][mu[2]]
    innerTrk_P_3 = df.Muon_innerTrack_p.iloc[0][mu[2]]
    innerTrk_Eta_3 = df.Muon_innerTrack_eta.iloc[0][mu[2]]
    innerTrk_normChi2_3 = df.Muon_innerTrack_normalizedChi2.iloc[0][mu[2]]
    QInnerOuter_3 = df.Muon_QInnerOuter.iloc[0][mu[2]]
    cQ_uS_3 = df.Muon_combinedQuality_updatedSta.iloc[0][mu[2]]
    cQ_tK_3 = df.Muon_combinedQuality_trkKink.iloc[0][mu[2]]
    cQ_gK_3 = df.Muon_combinedQuality_glbKink.iloc[0][mu[2]]
    cQ_tRChi2_3 = df.Muon_combinedQuality_trkRelChi2.iloc[0][mu[2]]
    cQ_sRChi2_3 = df.Muon_combinedQuality_staRelChi2.iloc[0][mu[2]]
    cQ_Chi2LP_3 = df.Muon_combinedQuality_chi2LocalPosition.iloc[0][mu[2]]
    cQ_Chi2LM_3 = df.Muon_combinedQuality_chi2LocalMomentum.iloc[0][mu[2]]
    cQ_lD_3 = df.Muon_combinedQuality_localDistance.iloc[0][mu[2]]
    cQ_gDEP_3 = df.Muon_combinedQuality_globalDeltaEtaPhi.iloc[0][mu[2]]
    cQ_tM_3 = df.Muon_combinedQuality_tightMatch.iloc[0][mu[2]]
    cQ_gTP_3 = df.Muon_combinedQuality_glbTrackProbability.iloc[0][mu[2]]
    segmComp_3 = df.Muon_segmentCompatibility.iloc[0][mu[2]]
    caloComp_3 = df.Muon_caloCompatibility.iloc[0][mu[2]]
    '''    
    start = time.time()
    if(debugMode): print("Ciao13")
    #df_fin["isMC"].append(isMC)
    #print(df_fin)
    #print("success!")
    df_fin["isMC"][jentry] = ((isMC))
    df_fin["lumi"][jentry] = ((lumi))
    df_fin["run"][jentry] = ((run))
    df_fin["evt"][jentry] = ((evt))
    df_fin["puFactor"][jentry] = ((puFactor))
    df_fin["L1_DoubleMu0_er1p5"][jentry] = ((L1_DoubleMu0_er1p5))
    df_fin["L1_DoubleMu0_er1p4"][jentry] = ((L1_DoubleMu0_er1p4))
    df_fin["L1_DoubleMu4_dR1p2"][jentry] = ((L1_DoubleMu4_dR1p2))
    df_fin["L1_DoubleMu4p5_dR1p2"][jentry] = ((L1_DoubleMu4p5_dR1p2))
    df_fin["L1_DoubleMu0_er2p0"][jentry] = ((L1_DoubleMu0_er2p0))
    df_fin["L1_DoubleMu0_er2p0_bk"][jentry] = ((L1_DoubleMu0_er2p0_bk))
    df_fin["L1seed"][jentry] = ((L1seed))
    df_fin["HLTpath"][jentry] = ((HLTpath))
    df_fin["DeltaR_max"][jentry] = ((DeltaR_max))
    df_fin["DeltaZ_max"][jentry] = ((DeltaZ_max))
    df_fin["Pmu3"][jentry] = (MuonP(df, pt[2], eta[2], phi[2]))
    df_fin["cLP"][jentry] = ((cLP))
    df_fin["tKink"][jentry] = ((tKink))
    df_fin["segmComp"][jentry] = ((segmComp))
    df_fin["tripletMass"][jentry] = ((tripletMass))
    ####df_fin["tripletMassReso"][jentry] = ((tripletMassReso))
    df_fin["fv_nC"][jentry] = (df.TripletVtx2_Chi2.iloc[0][ind]/3)
    df_fin["fv_dphi3D"][jentry] = (TreeFin_Angle(df, ind))
    df_fin["fv_d3D"][jentry] = (df.FlightDistPVSV2.iloc[0][ind])
    df_fin["fv_d3Dsig"][jentry] = (df.FlightDistPVSV2_Significance.iloc[0][ind])
    df_fin["d0"][jentry] = ((d0))
    df_fin["nVtx"][jentry] = (df.PVCollection_Size.iloc[0])
    df_fin["d0sig"][jentry] = ((d0sig))
    df_fin["MVA1"][jentry] = ( df.Muon_MVA.iloc[0][mu[0]])
    df_fin["MVA2"][jentry] = ( df.Muon_MVA.iloc[0][mu[1]])
    df_fin["MVA3"][jentry] = (0.)
    df_fin["MVASoft1"][jentry] = ( df.Muon_SoftMVA_Val.iloc[0][mu[0]])
    df_fin["MVASoft2"][jentry] = (df.Muon_SoftMVA_Val.iloc[0][mu[1]])
    df_fin["MVASoft3"][jentry] = (0.)
    df_fin["d0sig_max"][jentry] = ((d0sig_max))
    df_fin["mindca_iso"][jentry] = (df.Triplet_mindca_iso.iloc[0][ind])
    df_fin["trkRel"][jentry] = (df.Triplet_relativeiso.iloc[0][ind])
    df_fin["Pmu1"][jentry] = (MuonP(df, df.Mu01_Pt.iloc[0][mu_Ind[0]], df.Mu01_Eta.iloc[0][mu_Ind[0]], df.Mu01_Phi.iloc[0][mu_Ind[0]]))
    df_fin["Ptmu1"][jentry] = (df.Mu01_Pt.iloc[0][mu_Ind[0]])
    df_fin["Etamu1"][jentry] = (df.Mu01_Eta.iloc[0][mu_Ind[0]])
    df_fin["Phimu1"][jentry] = (df.Mu01_Phi.iloc[0][mu_Ind[0]])
    df_fin["Pmu2"][jentry] = (MuonP(df, df.Mu02_Pt.iloc[0][mu_Ind[1]], df.Mu02_Eta.iloc[0][mu_Ind[1]], df.Mu02_Phi.iloc[0][mu_Ind[1]]))
    df_fin["Ptmu2"][jentry] = (df.Mu02_Pt.iloc[0][mu_Ind[1]])
    df_fin["Etamu2"][jentry] = (df.Mu02_Eta.iloc[0][mu_Ind[1]])
    df_fin["Phimu2"][jentry] = (df.Mu02_Phi.iloc[0][mu_Ind[1]])
    df_fin["Ptmu3"][jentry] = (df.Tr_Pt.iloc[0][mu_Ind[2]])
    df_fin["Etamu3"][jentry] = (df.Tr_Eta.iloc[0][mu_Ind[2]])
    df_fin["Phimu3"][jentry] = (df.Tr_Phi.iloc[0][(mu_Ind[2])])
    df_fin["dispMu1"][jentry] = (math.sqrt(pow(df.BS_x.iloc[0][mu_Ind[0]] - df.Muon_vx.iloc[0][mu[0]],2) + pow(df.BS_y.iloc[0][mu_Ind[0]] - df.Muon_vy.iloc[0][mu[0]],2) + pow(df.BS_z.iloc[0][mu_Ind[0]] - df.Muon_vz.iloc[0][mu[0]],2)))
    df_fin["dispMu2"][jentry] = (math.sqrt(pow(df.BS_x.iloc[0][mu_Ind[1]] - df.Muon_vx.iloc[0][mu[1]],2) + pow(df.BS_y.iloc[0][mu_Ind[1]] - df.Muon_vy.iloc[0][mu[1]],2) + pow(df.BS_z.iloc[0][mu_Ind[1]] - df.Muon_vz.iloc[0][mu[1]],2)))
    ####df_fin["dispMu3"][jentry] = ((dispMu3))
    df_fin["xydispMu1"][jentry] = (math.sqrt(pow(df.BS_x.iloc[0][mu_Ind[0]] - df.Muon_vx.iloc[0][mu[0]],2) + pow(df.BS_y.iloc[0][mu_Ind[0]] - df.Muon_vy.iloc[0][mu[0]],2)))
    df_fin["xydispMu2"][jentry] = (math.sqrt(pow(df.BS_x.iloc[0][mu_Ind[1]] - df.Muon_vx.iloc[0][mu[1]],2) + pow(df.BS_y.iloc[0][mu_Ind[1]] - df.Muon_vy.iloc[0][mu[1]],2)))
    ####df_fin["xydispMu3"][jentry] = ((xydispMu3))
    df_fin["P_tripl"][jentry] = (MuonP(df, df.Triplet2_Pt.iloc[0][ind], df.Triplet2_Eta.iloc[0][ind], df.Triplet2_Phi.iloc[0][ind]))
    df_fin["Pt_tripl"][jentry] = (df.Triplet2_Pt.iloc[0][ind])
    df_fin["Eta_tripl"][jentry] = (df.Triplet2_Eta.iloc[0][ind])
    df_fin["nStMu1"][jentry] = (df.Muon_numberOfMatchedStations.iloc[0][mu[0]])
    df_fin["nStMu2"][jentry] = (df.Muon_numberOfMatchedStations.iloc[0][mu[1]])
    ####df_fin["nStMu3"][jentry] = ((nStationsMu3))
    df_fin["Iso03Mu1"][jentry] = (df.Mu1_NTracks03iso.iloc[0][mu_Ind[0]])
    df_fin["Iso03Mu2"][jentry] = (df.Mu2_NTracks03iso.iloc[0][mu_Ind[1]])
    df_fin["Iso03Mu3"][jentry] = (df.Tr_NTracks03iso.iloc[0][mu_Ind[2]])
    df_fin["Iso05Mu1"][jentry] = (df.Muon_emEt05.iloc[0][mu[0]])
    df_fin["Iso05Mu2"][jentry] = (df.Muon_emEt05.iloc[0][mu[1]])
    ####df_fin["Iso05Mu3"][jentry] = ((Iso05Mu3))
    df_fin["nMatchesMu1"][jentry] = (df.Muon_numberOfMatches.iloc[0][mu[0]])
    df_fin["nMatchesMu2"][jentry] = (df.Muon_numberOfMatches.iloc[0][mu[1]])
    ####df_fin["nMatchesMu3"][jentry] = ((nMatchesMu3))
    df_fin["timeAtIpInOut_sig1"][jentry] = (df.Muon_timeAtIpInOut.iloc[0][mu[0]]/ df.Muon_timeAtIpInOutErr.iloc[0][mu[0]])
    df_fin["timeAtIpInOut_sig2"][jentry] = (df.Muon_timeAtIpInOut.iloc[0][mu[1]]/ df.Muon_timeAtIpInOutErr.iloc[0][mu[1]])
    ####df_fin["timeAtIpInOut_sig3"][jentry] = ((timeAtIpInOut_sig3))
    df_fin["cQ_uS"][jentry] = ((cQ_uS))
    df_fin["cQ_tK"][jentry] = ((cQ_tK))
    df_fin["cQ_gK"][jentry] = ((cQ_gK))
    df_fin["cQ_tRChi2"][jentry] = ((cQ_tRChi2))
    df_fin["cQ_sRChi2"][jentry] = ((cQ_sRChi2))
    df_fin["cQ_Chi2LP"][jentry] = ((cQ_Chi2LP))
    df_fin["cQ_Chi2LM"][jentry] = ((cQ_Chi2LM))
    df_fin["cQ_lD"][jentry] = ((cQ_lD))
    df_fin["cQ_gDEP"][jentry] = ((cQ_gDEP))
    df_fin["cQ_tM"][jentry] = ((cQ_tM))
    df_fin["cQ_gTP"][jentry] = ((cQ_gTP))
    df_fin["calEn_emMu1"][jentry] = (df.Muon_calEnergy_em.iloc[0][mu[0]])
    df_fin["calEn_emMu2"][jentry] = (df.Muon_calEnergy_em.iloc[0][mu[1]])
    ####df_fin["calEn_emMu3"][jentry] = ((calEn_emMu3))
    df_fin["calEn_hadMu1"][jentry] = (df.Muon_calEnergy_had.iloc[0][mu[0]])
    df_fin["calEn_hadMu2"][jentry] = (df.Muon_calEnergy_had.iloc[0][mu[1]])
    ####df_fin["calEn_hadMu3"][jentry] = ((calEn_hadMu3))
    df_fin["caloComp"][jentry] = ((caloComp))
    ####df_fin["fliDistPVSV_Chi2"][jentry] = ((fliDistPVSV_Chi2))
    df_fin["isGlb1"][jentry] = (df.Muon_isGlobal.iloc[0][mu[0]])
    df_fin["isMedium1"][jentry] = (df.Muon_isMedium.iloc[0][mu[0]])
    df_fin["isTracker1"][jentry] = (df.Muon_isTrackerMuon.iloc[0][mu[0]])
    df_fin["isLoose1"][jentry] = (df.Muon_isLoose.iloc[0][mu[0]])
    df_fin["isSoft1"][jentry] = (df.Muon_isSoft.iloc[0][mu[0]])
    df_fin["isPF1"][jentry] = ( df.Muon_isPF.iloc[0][mu[0]])
    df_fin["isRPC1"][jentry] = (df.Muon_isRPCMuon.iloc[0][mu[0]])
    df_fin["isSA1"][jentry] = (df.Muon_isStandAloneMuon.iloc[0][mu[0]])
    df_fin["isCalo1"][jentry] = (df.Muon_isCaloMuon.iloc[0][mu[0]])
    df_fin["isGlb2"][jentry] = (df.Muon_isGlobal.iloc[0][mu[1]])
    df_fin["isMedium2"][jentry] = (df.Muon_isMedium.iloc[0][mu[1]])
    df_fin["isTracker2"][jentry] = (df.Muon_isTrackerMuon.iloc[0][mu[1]])
    df_fin["isLoose2"][jentry] = (df.Muon_isLoose.iloc[0][mu[1]])
    df_fin["isSoft2"][jentry] = (df.Muon_isSoft.iloc[0][mu[1]])
    df_fin["isPF2"][jentry] = (df.Muon_isPF.iloc[0][mu[1]])
    df_fin["isRPC2"][jentry] = (df.Muon_isRPCMuon.iloc[0][mu[1]])
    df_fin["isSA2"][jentry] = (df.Muon_isStandAloneMuon.iloc[0][mu[1]])
    df_fin["isCalo2"][jentry] = (df.Muon_isCaloMuon.iloc[0][mu[1]])
    ''')
    df_fin["isGlb3"][jentry] = ((isGlb3))
    df_fin["isTracker3"][jentry] = ((isTracker3))
    df_fin["isLoose3"][jentry] = ((isLoose3))
    df_fin["isSoft3"][jentry] = ((isSoft3))
    df_fin["isPF3"][jentry] = ((isPF3))
    df_fin["isRPC3"][jentry] = ((isRPC3))
    df_fin["isSA3"][jentry] = ((isSA3))
    df_fin["isCalo3"][jentry] = ((isCalo3))
    '''
    df_fin["Vx1"][jentry] = (df.Muon_vx.iloc[0][mu[0]])
    df_fin["Vx2"][jentry] = (df.Muon_vx.iloc[0][mu[1]])
    df_fin["Vx3"][jentry] = (df.Track_vx.iloc[0][mu[2]])
    df_fin["Vy1"][jentry] = (df.Muon_vy.iloc[0][mu[0]])
    df_fin["Vy2"][jentry] = (df.Muon_vy.iloc[0][mu[1]])
    df_fin["Vy3"][jentry] = (df.Track_vy.iloc[0][mu[2]])
    df_fin["Vz1"][jentry] = (df.Muon_vz.iloc[0][mu[0]])
    df_fin["Vz2"][jentry] = (df.Muon_vz.iloc[0][mu[1]])
    df_fin["Vz3"][jentry] = (df.Track_vz.iloc[0][mu[2]])
    df_fin["RefVx1"][jentry] = (df.RefittedPV2_x.iloc[0][ind])
    ####df_fin["RefVx2"][jentry] = ((RefVx2))
    ####df_fin["RefVx3"][jentry] = ((RefVx3))
    df_fin["RefVy1"][jentry] = (df.RefittedPV2_y.iloc[0][ind])
    ####df_fin["RefVy2"][jentry] = ((RefVy2))
    ####df_fin["RefVy3"][jentry] = ((RefVy3))
    df_fin["RefVz1"][jentry] = (df.RefittedPV2_z.iloc[0][ind])
    ####df_fin["RefVz2"][jentry] = ((RefVz2))
    ####df_fin["RefVz3"][jentry] = ((RefVz3))
    df_fin["SVx"][jentry] = (df.TripletVtx2_x.iloc[0][ind])
    df_fin["SVy"][jentry] = (df.TripletVtx2_y.iloc[0][ind])
    df_fin["SVz"][jentry] = (df.TripletVtx2_z.iloc[0][ind])
    ''')
    df_fin["had03"][jentry] = ((had03))
    df_fin["had05"][jentry] = ((had05))
    df_fin["nJets03"][jentry] = ((nJets03))
    df_fin["nJets05"][jentry] = ((nJets05))
    df_fin["nTracks03"][jentry] = ((nTracks03))
    df_fin["nTracks05"][jentry] = ((nTracks05))
    df_fin["sumPt03"][jentry] = ((sumPt03))
    df_fin["sumPt05"][jentry] = ((sumPt05))
    df_fin["hadVeto03"][jentry] = ((hadVeto03))
    df_fin["hadVeto05"][jentry] = ((hadVeto05))
    df_fin["emVeto03"][jentry] = ((emVeto03))
    df_fin["emVeto05"][jentry] = ((emVeto05))
    df_fin["trVeto03"][jentry] = ((trVeto03))
    df_fin["trVeto05"][jentry] = ((trVeto05))
    '''
    #)new)branches))
    df_fin["EnMu1"][jentry] = (df.MuonEnergy.iloc[0][mu[0]])
    df_fin["EnMu2"][jentry] = (df.MuonEnergy.iloc[0][mu[1]])
    #####df_fin["EnMu3"][jentry] = ((EnMu3))
    df_fin["ChargeMu1"][jentry] = (df.MuonCharge.iloc[0][mu[0]])
    df_fin["ChargeMu2"][jentry] = (df.MuonCharge.iloc[0][mu[1]])
    df_fin["ChargeMu3"][jentry] = (df.Track_charge.iloc[0][mu[2]])
    #)Mu1))
    df_fin["isQValid1"][jentry] = (df.Muon_isQualityValid.iloc[0][mu[0]])
    df_fin["isTValid1"][jentry] = (df.Muon_isTimeValid.iloc[0][mu[0]])
    df_fin["isIsoValid1"][jentry] = (df.Muon_isIsolationValid.iloc[0][mu[0]])
    df_fin["GLnormChi2_mu1"][jentry] = (df.Muon_GLnormChi2.iloc[0][mu[0]])
    df_fin["GL_nValidMuHits1"][jentry] = (df.Muon_GLhitPattern_numberOfValidMuonHits.iloc[0][mu[0]])
    df_fin["trkLayersWMeas1"][jentry] = (df.Muon_trackerLayersWithMeasurement.iloc[0][mu[0]])
    df_fin["validMuonHitComb1"][jentry] = (df.Muon_validMuonHitComb.iloc[0][mu[0]])
    df_fin["nValidTrackerHits1"][jentry] = (df.Muon_Numberofvalidtrackerhits.iloc[0][mu[0]])
    df_fin["nValidPixelHits1"][jentry] = (df.Muon_Numberofvalidpixelhits.iloc[0][mu[0]])
    df_fin["outerTrk_P_1"][jentry] = (df.Muon_outerTrack_p.iloc[0][mu[0]])
    df_fin["outerTrk_Eta_1"][jentry] = (df.Muon_outerTrack_eta.iloc[0][mu[0]])
    df_fin["outerTrk_normChi2_1"][jentry] = (df.Muon_outerTrack_normalizedChi2.iloc[0][mu[0]])
    df_fin["outerTrk_muStValidHits_1"][jentry] = (df.Muon_outerTrack_muonStationsWithValidHits.iloc[0][mu[0]])
    df_fin["innerTrk_P_1"][jentry] = (df.Muon_innerTrack_p.iloc[0][mu[0]])
    df_fin["innerTrk_Eta_1"][jentry] = (df.Muon_innerTrack_eta.iloc[0][mu[0]])
    df_fin["innerTrk_normChi2_1"][jentry] = (df.Muon_innerTrack_normalizedChi2.iloc[0][mu[0]])
    df_fin['innerTrk_highPurity_1'][jentry] = (df.Muon_innerTrack_highPurity.iloc[0][mu[0]])
    df_fin['innerTrk_ValidFraction_1'][jentry] = (df.Muon_innerTrack_ValidFraction.iloc[0][mu[0]])
    df_fin['QInnerOuter_1'][jentry] = (df.Muon_QInnerOuter.iloc[0][mu[0]])
    df_fin['cQ_uS_1'][jentry] = (df.Muon_combinedQuality_updatedSta.iloc[0][mu[0]])
    df_fin['cQ_tK_1'][jentry] = (df.Muon_combinedQuality_trkKink.iloc[0][mu[0]])
    df_fin['cQ_gK_1'][jentry] = (df.Muon_combinedQuality_glbKink.iloc[0][mu[0]])
    df_fin['cQ_tRChi2_1'][jentry] = (df.Muon_combinedQuality_trkRelChi2.iloc[0][mu[0]])
    df_fin['cQ_sRChi2_1'][jentry] = (df.Muon_combinedQuality_staRelChi2.iloc[0][mu[0]])
    df_fin['cQ_Chi2LP_1'][jentry] = (df.Muon_combinedQuality_chi2LocalPosition.iloc[0][mu[0]])
    df_fin['cQ_Chi2LM_1'][jentry] = (df.Muon_combinedQuality_chi2LocalMomentum.iloc[0][mu[0]])
    df_fin['cQ_lD_1'][jentry] = (df.Muon_combinedQuality_localDistance.iloc[0][mu[0]])
    df_fin['cQ_gDEP_1'][jentry] = (df.Muon_combinedQuality_globalDeltaEtaPhi.iloc[0][mu[0]])
    df_fin['cQ_tM_1'][jentry] = (df.Muon_combinedQuality_tightMatch.iloc[0][mu[0]])
    df_fin['cQ_gTP_1'][jentry] = (df.Muon_combinedQuality_glbTrackProbability.iloc[0][mu[0]])
    df_fin['segmComp_1'][jentry] = (df.Muon_segmentCompatibility.iloc[0][mu[0]])
    df_fin['caloComp_1'][jentry] = (df.Muon_caloCompatibility.iloc[0][mu[0]])
    df_fin['match1_dX_1'][jentry] = (df.Muon_combinedQuality_match1_dX.iloc[0][mu[0]])
    df_fin['match1_pullX_1'][jentry] = (df.Muon_combinedQuality_match1_pullX.iloc[0][mu[0]])
    df_fin['match1_pullDxDz_1'][jentry] = (df.Muon_combinedQuality_match1_pullDxDz.iloc[0][mu[0]])
    df_fin['match1_dY_1'][jentry] = (df.Muon_combinedQuality_match1_dY.iloc[0][mu[0]])
    df_fin['match1_pullY_1'][jentry] = (df.Muon_combinedQuality_match1_pullY.iloc[0][mu[0]])
    df_fin['match1_pullDyDz_1'][jentry] = (df.Muon_combinedQuality_match1_pullDyDz.iloc[0][mu[0]])
    df_fin['match2_dX_1'][jentry] = (df.Muon_combinedQuality_match2_dX.iloc[0][mu[0]])
    df_fin['match2_pullX_1'][jentry] = (df.Muon_combinedQuality_match2_pullX.iloc[0][mu[0]])
    df_fin['match2_pullDxDz_1'][jentry] = (df.Muon_combinedQuality_match2_pullDxDz.iloc[0][mu[0]])
    df_fin['match2_dY_1'][jentry] = (df.Muon_combinedQuality_match2_dY.iloc[0][mu[0]])
    df_fin['match2_pullY_1'][jentry] = (df.Muon_combinedQuality_match2_pullY.iloc[0][mu[0]])
    df_fin['match2_pullDyDz_1'][jentry] = (df.Muon_combinedQuality_match2_pullDyDz.iloc[0][mu[0]])
    df_fin['isQValid2'][jentry] = (df.Muon_isQualityValid.iloc[0][mu[1]])
    df_fin['isTValid2'][jentry] = (df.Muon_isTimeValid.iloc[0][mu[1]])
    df_fin['isIsoValid2'][jentry] = (df.Muon_isIsolationValid.iloc[0][mu[1]])
    df_fin['GLnormChi2_mu2'][jentry] = (df.Muon_GLnormChi2.iloc[0][mu[1]])
    df_fin['GL_nValidMuHits2'][jentry] = (df.Muon_GLhitPattern_numberOfValidMuonHits.iloc[0][mu[1]])
    df_fin['trkLayersWMeas2'][jentry] = (df.Muon_trackerLayersWithMeasurement.iloc[0][mu[1]])
    df_fin['validMuonHitComb2'][jentry] = (df.Muon_validMuonHitComb.iloc[0][mu[1]])
    df_fin['nValidTrackerHits2'][jentry] = (df.Muon_Numberofvalidtrackerhits.iloc[0][mu[1]])
    df_fin['nValidPixelHits2'][jentry] = (df.Muon_Numberofvalidpixelhits.iloc[0][mu[1]])
    df_fin['outerTrk_P_2'][jentry] = (df.Muon_outerTrack_p.iloc[0][mu[1]])
    df_fin['outerTrk_Eta_2'][jentry] = (df.Muon_outerTrack_eta.iloc[0][mu[1]])
    df_fin['outerTrk_normChi2_2'][jentry] = (df.Muon_outerTrack_normalizedChi2.iloc[0][mu[1]])
    df_fin['outerTrk_muStValidHits_2'][jentry] = (df.Muon_outerTrack_muonStationsWithValidHits.iloc[0][mu[1]])
    df_fin['innerTrk_P_2'][jentry] = (df.Muon_innerTrack_p.iloc[0][mu[1]])
    df_fin['innerTrk_Eta_2'][jentry] = (df.Muon_innerTrack_eta.iloc[0][mu[1]])
    df_fin['innerTrk_normChi2_2'][jentry] = (df.Muon_innerTrack_normalizedChi2.iloc[0][mu[1]])
    df_fin['innerTrk_highPurity_2'][jentry] = (df.Muon_innerTrack_highPurity.iloc[0][mu[1]])
    df_fin['innerTrk_ValidFraction_2'][jentry] = (df.Muon_innerTrack_ValidFraction.iloc[0][mu[1]])
    df_fin['QInnerOuter_2'][jentry] = (df.Muon_QInnerOuter.iloc[0][mu[1]])
    df_fin['cQ_uS_2'][jentry] = (df.Muon_combinedQuality_updatedSta.iloc[0][mu[1]])
    df_fin['cQ_tK_2'][jentry] = (df.Muon_combinedQuality_trkKink.iloc[0][mu[1]])
    df_fin['cQ_gK_2'][jentry] = (df.Muon_combinedQuality_glbKink.iloc[0][mu[1]])
    df_fin['cQ_tRChi2_2'][jentry] = (df.Muon_combinedQuality_trkRelChi2.iloc[0][mu[1]])
    df_fin['cQ_sRChi2_2'][jentry] = (df.Muon_combinedQuality_staRelChi2.iloc[0][mu[1]])
    df_fin['cQ_Chi2LP_2'][jentry] = (df.Muon_combinedQuality_chi2LocalPosition.iloc[0][mu[1]])
    df_fin['cQ_Chi2LM_2'][jentry] = (df.Muon_combinedQuality_chi2LocalMomentum.iloc[0][mu[1]])
    df_fin['cQ_lD_2'][jentry] = (df.Muon_combinedQuality_localDistance.iloc[0][mu[1]])
    df_fin['cQ_gDEP_2'][jentry] = (df.Muon_combinedQuality_globalDeltaEtaPhi.iloc[0][mu[1]])
    df_fin['cQ_tM_2'][jentry] = (df.Muon_combinedQuality_tightMatch.iloc[0][mu[1]])
    df_fin['cQ_gTP_2'][jentry] = (df.Muon_combinedQuality_glbTrackProbability.iloc[0][mu[1]])
    df_fin['segmComp_2'][jentry] = (df.Muon_segmentCompatibility.iloc[0][mu[1]])
    df_fin['caloComp_2'][jentry] = (df.Muon_caloCompatibility.iloc[0][mu[1]])
    df_fin['match1_dX_2'][jentry] = (df.Muon_combinedQuality_match1_dX.iloc[0][mu[1]])
    df_fin['match1_pullX_2'][jentry] = (df.Muon_combinedQuality_match1_pullX.iloc[0][mu[1]])
    df_fin['match1_pullDxDz_2'][jentry] = (df.Muon_combinedQuality_match1_pullDxDz.iloc[0][mu[1]])
    df_fin['match1_dY_2'][jentry] = (df.Muon_combinedQuality_match1_dY.iloc[0][mu[1]])
    df_fin['match1_pullY_2'][jentry] = (df.Muon_combinedQuality_match1_pullY.iloc[0][mu[1]])
    df_fin['match1_pullDyDz_2'][jentry] = (df.Muon_combinedQuality_match1_pullDyDz.iloc[0][mu[1]])
    df_fin['match2_dX_2'][jentry] = (df.Muon_combinedQuality_match2_dX.iloc[0][mu[1]])
    df_fin['match2_pullX_2'][jentry] = (df.Muon_combinedQuality_match2_pullX.iloc[0][mu[1]])
    df_fin['match2_pullDxDz_2'][jentry] = (df.Muon_combinedQuality_match2_pullDxDz.iloc[0][mu[1]])
    df_fin['match2_dY_2'][jentry] = (df.Muon_combinedQuality_match2_dY.iloc[0][mu[1]])
    df_fin['match2_pullY_2'][jentry] = (df.Muon_combinedQuality_match2_pullY.iloc[0][mu[1]])
    df_fin['match2_pullDyDz_2'][jentry] = (df.Muon_combinedQuality_match2_pullDyDz.iloc[0][mu[1]])
    #)Mu3))
    ''')
    df_fin["isQValid3"][jentry] = ((isQValid3))
    df_fin["isTValid3"][jentry] = ((isTValid3))
    df_fin["isIsoValid3"][jentry] = ((isIsoValid3))
    df_fin["GLnormChi2_mu3"][jentry] = ((GLnormChi2_mu3))
    df_fin["GL_nValidMuHits3"][jentry] = ((GL_nValidMuHits3))
    df_fin["trkLayersWMeas3"][jentry] = ((trkLayersWMeas3))
    df_fin["validMuonHitComb3"][jentry] = ((validMuonHitComb3))
    df_fin["nValidTrackerHits3"][jentry] = ((nValidTrackerHits3))
    df_fin["nValidPixelHits3"][jentry] = ((nValidPixelHits3))
    df_fin["outerTrk_P_3"][jentry] = ((outerTrk_P_3))
    df_fin["outerTrk_Eta_3"][jentry] = ((outerTrk_Eta_3))
    df_fin["outerTrk_normChi2_3"][jentry] = ((outerTrk_normChi2_3))
    df_fin["outerTrk_muStValidHits_3"][jentry] = ((outerTrk_muStValidHits_3))
    df_fin["innerTrk_P_3"][jentry] = ((innerTrk_P_3))
    df_fin["innerTrk_Eta_3"][jentry] = ((innerTrk_Eta_3))
    df_fin["innerTrk_normChi2_3"][jentry] = ((innerTrk_normChi2_3))
    df_fin["innerTrk_highPurity_3"][jentry] = ((innerTrk_highPurity_3))
    df_fin["innerTrk_ValidFraction_3"][jentry] = ((innerTrk_ValidFraction_3))
    df_fin["QInnerOuter_3"][jentry] = ((QInnerOuter_3))
    df_fin["cQ_uS_3"][jentry] = ((cQ_uS_3))
    df_fin["cQ_tK_3"][jentry] = ((cQ_tK_3))
    df_fin["cQ_gK_3"][jentry] = ((cQ_gK_3))
    df_fin["cQ_tRChi2_3"][jentry] = ((cQ_tRChi2_3))
    df_fin["cQ_sRChi2_3"][jentry] = ((cQ_sRChi2_3))
    df_fin["cQ_Chi2LP_3"][jentry] = ((cQ_Chi2LP_3))
    df_fin["cQ_Chi2LM_3"][jentry] = ((cQ_Chi2LM_3))
    df_fin["cQ_lD_3"][jentry] = ((cQ_lD_3))
    df_fin["cQ_gDEP_3"][jentry] = ((cQ_gDEP_3))
    df_fin["cQ_tM_3"][jentry] = ((cQ_tM_3))
    df_fin["cQ_gTP_3"][jentry] = ((cQ_gTP_3))
    df_fin["segmComp_3"][jentry] = ((segmComp_3))
    df_fin["caloComp_3"][jentry] = ((caloComp_3))
    df_fin["match1_dX_3"][jentry] = ((match1_dX_3))
    df_fin["match1_pullX_3"][jentry] = ((match1_pullX_3))
    df_fin["match1_pullDxDz_3"][jentry] = ((match1_pullDxDz_3))
    df_fin["match1_dY_3"][jentry] = ((match1_dY_3))
    df_fin["match1_pullY_3"][jentry] = ((match1_pullY_3))
    df_fin["match1_pullDyDz_3"][jentry] = ((match1_pullDyDz_3))
    df_fin["match2_dX_3"][jentry] = ((match2_dX_3))
    df_fin["match2_pullX_3"][jentry] = ((match2_pullX_3))
    df_fin["match2_pullDxDz_3"][jentry] = ((match2_pullDxDz_3))
    df_fin["match2_dY_3"][jentry] = ((match2_dY_3))
    df_fin["match2_pullY_3"][jentry] = ((match2_pullY_3))
    df_fin["match2_pullDyDz_3"][jentry] = ((match2_pullDyDz_3))
    '''
    stop = time.time()
    dtime = stop - start
    print(f"Time: {dtime}")

    
def twoMuonsTrkFinder(sub_df_finder, sub_df):
    if sub_df_finder.index_triplet.iloc[0] == 0 or sub_df_finder.index_triplet.iloc[0] == 1:
        #print(sub_df_finder)
        index_of_particle = sub_df_finder.index_triplet.iloc[0]
        #print(index_of_particle)
        pt_triplet = sub_df_finder.pt.iloc[0]
        eta_triplet = sub_df_finder.eta.iloc[0]
        phi_triplet = sub_df_finder.phi.iloc[0]
        indeces = np.arange(len(sub_df.MuonPt.iloc[0]))
        #print(f"INDECES: {indeces}")
        # compute the number of muons that matches the considered one
        matching_condition = (sub_df.MuonPt.iloc[0] == pt_triplet) & (sub_df.MuonEta.iloc[0] == eta_triplet) & (sub_df.MuonPhi.iloc[0] == phi_triplet) 
        n = sum(matching_condition) 
        #print(n)
        badOuterChi2 = sum(sub_df.Muon_outerTrack_normalizedChi2.iloc[0] == -999)
        #MULTIPLE muons (There is more than 1 muon that matches the conditions)
        if n > 1:
            ####### CASE 0: there aren't muons w/ outerTrachChi2 != -999
            if (n-badOuterChi2) == 0:  
                # find the muon w/ the smallest innerTrackChi2
                Chi2InnerTrackmin = sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition][sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition]==min(sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition])]
                nMuonChi2InnerMin = len(Chi2InnerTrackmin)
                minimum_Chi2InnerTrackmin = sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition]==min(sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition])
                #only one
                if nMuonChi2InnerMin == 1:
                    sub_df_finder["mu_index"] = indeces[matching_condition][minimum_Chi2InnerTrackmin]
                    pt = sub_df.MuonPt.iloc[0][matching_condition][minimum_Chi2InnerTrackmin]
                    eta = sub_df.MuonEta.iloc[0][matching_condition][minimum_Chi2InnerTrackmin]
                    phi = sub_df.MuonPhi.iloc[0][matching_condition][minimum_Chi2InnerTrackmin]
                    return pt, eta, phi
                # more than one: find the muon with the biggest number of matches
                else:
                    maximum_n_of_matches = (sub_df.Muon_numberOfMatches.iloc[0][matching_condition]==min(sub_df.Muon_numberOfMatches.iloc[0][matching_condition]))
                    n_of_matches_max = sum(maximum_n_of_matches)
                    if n_of_matches_max == 1:
                        sub_df_finder["mu_index"] = indeces[matching_condition][minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                        pt = sub_df.MuonPt.iloc[0][matching_condition][minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                        eta = sub_df.MuonEta.iloc[0][matching_condition][minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                        phi = sub_df.MuonPhi.iloc[0][matching_condition][minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                        return pt, eta, phi
                    else:
                        print("multple muons with outerChi2 = -999!")
                        #return pt, eta and phi of the last one
                        sub_df_finder["mu_index"] = indeces[matching_condition][minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                        pt = sub_df.MuonPt.iloc[0][matching_condition][minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                        eta = sub_df.MuonEta.iloc[0][matching_condition][minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                        phi = sub_df.MuonPhi.iloc[0][matching_condition][minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                        return pt[-1], eta[-1], phi[-1]
            ####### CASE 1:  // There is ONLY 1 muon that has outerTrachChi2 != -999
            elif (n-badOuterChi2) == 1:
                sub_df_finder["mu_index"] = indeces[matching_condition & (sub_df.Muon_outerTrack_normalizedChi2.iloc[0]!= -999)]
                pt = sub_df.MuonPt.iloc[0][matching_condition & (sub_df.Muon_outerTrack_normalizedChi2.iloc[0]!= -999)]
                eta = sub_df.MuonEta.iloc[0][matching_condition & (sub_df.Muon_outerTrack_normalizedChi2.iloc[0]!= -999)]
                phi = sub_df.MuonPhi.iloc[0][matching_condition & (sub_df.Muon_outerTrack_normalizedChi2.iloc[0]!= -999)]
                return pt, eta, phi
            ####### CASE 2:  // There is more than 1 muon w/ outerTrachChi2 != -999
            elif (n-badOuterChi2) > 1:  
                # find the muon w/ the smallest outerTrackChi2
                Chi2OuterTrackmin = sub_df.Muon_outerTrack_normalizedChi2.iloc[0][matching_condition][sub_df.Muon_outerTrack_normalizedChi2.iloc[0][matching_condition]==min(sub_df.Muon_outerTrack_normalizedChi2.iloc[0][matching_condition])]
                nMuonChi2OuterMin = len(Chi2OuterTrackmin)
                minimum_Chi2OuterTrackmin = sub_df.Muon_outerTrack_normalizedChi2.iloc[0][matching_condition]==min(sub_df.Muon_outerTrack_normalizedChi2.iloc[0][matching_condition])
                #only one
                if nMuonChi2OuterMin == 1:
                    sub_df_finder["mu_index"] = indeces[matching_condition][minimum_Chi2OuterTrackmin]
                    pt = sub_df.MuonPt.iloc[0][matching_condition][minimum_Chi2OuterTrackmin]
                    eta = sub_df.MuonEta.iloc[0][matching_condition][minimum_Chi2OuterTrackmin]
                    phi = sub_df.MuonPhi.iloc[0][matching_condition][minimum_Chi2OuterTrackmin]
                    return pt, eta, phi
                # more than one: find the muon with the smallest chi2 inner
                else:
                    Chi2InnerTrackmin = sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition][sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition]==min(sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition])]
                    nMuonChi2InnerMin = len(Chi2InnerTrackmin)
                    minimum_Chi2InnerTrackmin = sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition]==min(sub_df.Muon_innerTrack_normalizedChi2.iloc[0][matching_condition])
                    #only one
                    if nMuonChi2InnerMin == 1:
                        sub_df_finder["mu_index"] = indeces[matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin]
                        pt = sub_df.MuonPt.iloc[0][matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin]
                        eta = sub_df.MuonEta.iloc[0][matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin]
                        phi = sub_df.MuonPhi.iloc[0][matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin]
                        return pt, eta, phi
                    # more than one: find the muon with the biggest number of matches
                    else:
                        maximum_n_of_matches = (sub_df.Muon_numberOfMatches.iloc[0][matching_condition]==min(sub_df.Muon_numberOfMatches.iloc[0][matching_condition]))
                        n_of_matches_max = sum(maximum_n_of_matches)
                        if n_of_matches_max == 1:
                            sub_df_finder["mu_index"] = indeces[matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                            pt = sub_df.MuonPt.iloc[0][matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                            eta = sub_df.MuonEta.iloc[0][matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                            phi = sub_df.MuonPhi.iloc[0][matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                            return pt, eta, phi
                        else:
                            print("multple muons with outerChi2 = -999!")
                            #return pt, eta and phi of the last one
                            sub_df_finder["mu_index"] = indeces[matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin & maximum_n_of_matches][-1]
                            pt = sub_df.MuonPt.iloc[0][matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                            eta = sub_df.MuonEta.iloc[0][matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                            phi = sub_df.MuonPhi.iloc[0][matching_condition][minimum_Chi2OuterTrackmin & minimum_Chi2InnerTrackmin & maximum_n_of_matches]
                            return pt[-1], eta[-1], phi[-1]
        elif n == 0:
            sub_df_finder["mu_index"] = None
        else:
            #print(sub_df.MuonPt.iloc[0][matching_condition])
            #print(sub_df.MuonPt.iloc[0])
            sub_df_finder["mu_index"] = indeces[matching_condition]
    elif sub_df_finder.index_triplet.iloc[0] == 2:
        #print(sub_df_finder)
        index_of_particle = sub_df_finder.index_triplet.iloc[0]
        #print(index_of_particle)
        pt_triplet = sub_df_finder.pt.iloc[0]
        eta_triplet = sub_df_finder.eta.iloc[0]
        phi_triplet = sub_df_finder.phi.iloc[0]
        indeces = np.arange(len(sub_df.Track_pt.iloc[0]))
        # compute the number of muons that matches the considered one
        matching_condition = (sub_df.Track_pt.iloc[0] == pt_triplet) & (sub_df.Track_eta.iloc[0] == eta_triplet) & (sub_df.Track_phi.iloc[0] == phi_triplet) 
        n = sum(matching_condition) 
        #print(n)
        badOuterChi2 = sum(sub_df.Muon_outerTrack_normalizedChi2.iloc[0] == -999)
        if n>1: print("Error: There is more than 1 track that matches the conditions!")
        elif n == 0: print("Error: There is NOT a track that matches the condition!")
        sub_df_finder["mu_index"] = indeces[matching_condition][-1]
        print(f"FIN QUI E': {sub_df.Mu01_Pt.iloc[0]}")
    return sub_df_finder

def goodTriplet_selection(sub_df_selection, sub_df, debugMode, triplEff_counter, HLT_obj_phi, HLT_obj_eta, HLT_obj_pt,  jentry, df_fin, isMC, ind_good, mu_Ind_good, mu_good, lumi_n, run_n, evt_n, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2,L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath):
    pt1 = (sub_df_selection.pt[sub_df_selection.index_triplet==0].iloc[0])
    pt2 = (sub_df_selection.pt[sub_df_selection.index_triplet==1].iloc[0])
    ptTr = (sub_df_selection.pt[sub_df_selection.index_triplet==2].iloc[0])
    eta1 = (sub_df_selection.eta[sub_df_selection.index_triplet==0].iloc[0])
    eta2 = (sub_df_selection.eta[sub_df_selection.index_triplet==1].iloc[0])
    etaTr = (sub_df_selection.eta[sub_df_selection.index_triplet==2].iloc[0])
    phi1 = (sub_df_selection.phi[sub_df_selection.index_triplet==0].iloc[0])
    phi2 = (sub_df_selection.phi[sub_df_selection.index_triplet==1].iloc[0])
    phiTr = (sub_df_selection.phi[sub_df_selection.index_triplet==2].iloc[0])
    FlightDistBS_SV_Significance = sub_df_selection.FlightDistBS_SV_Significance.iloc[0]
    Triplet2_Mass = sub_df_selection.Triplet2_Mass.iloc[0]
    #print(sub_df_selection.FlightDistBS_SV_Significance)
    experimental_limitations = pt1 >=2 and pt2 >=2 and abs(eta1)<=2.4 and abs(eta2)<=2.4 and ptTr>=2 and (etaTr)<=2.4
    mu1 = sub_df_selection.mu_index[sub_df_selection.index_triplet==0].iloc[0]
    mu2 = sub_df_selection.mu_index[sub_df_selection.index_triplet==1].iloc[0]
    Trk = sub_df_selection.mu_index[sub_df_selection.index_triplet==2].iloc[0]
    twoGlb_twoMd = sub_df.Muon_isGlobal.iloc[0][mu1] and sub_df.Muon_isMedium.iloc[0][mu1] and sub_df.Muon_isGlobal.iloc[0][mu2] and sub_df.Muon_isMedium.iloc[0][mu2]
    Trk_condition = (sub_df.Track_dz.iloc[0][Trk]) < 20 and sub_df.Track_dxy.iloc[0][Trk] <0.3
    not_duplicate = DuplicateFinder(sub_df, eta1, eta2, etaTr, phi1, phi2, phiTr, pt1, pt2, ptTr) and FlightDistBS_SV_Significance
    if not_duplicate and experimental_limitations and twoGlb_twoMd and Trk_condition:
        sub_df_selection["good_muonID"] = True
        triplEff_counter[3] = True
        if debugMode: print("goodMuonID\n")
    else:
        sub_df_selection["good_muonID"] = False
    # CUT 3 : OS DiMu mass in [0.98-1.06]
    DiMuMass = DimuonMass(sub_df, mu1, mu2) # diMuMass 12
    if (DiMuMass<=1.06 and DiMuMass>=0.98): 
        sub_df_selection["good_diMuMass"] = True
        triplEff_counter[4] = True
    else: sub_df_selection["good_diMuMass"] = False
    if (Triplet2_Mass<=2.1 and Triplet2_Mass>=1.62): 
        sub_df_selection["good_triMuMass"] = True
        triplEff_counter[5] = True
    else: sub_df_selection["good_triMuMass"] = False
    #print(HLT_obj_phi)
    if len(HLT_obj_phi)>0:
        dphi1 = abs(phi1 - HLT_obj_phi)
        #print(dphi1)
        deta1 = abs(eta1 - HLT_obj_eta)
        dpt1 = abs(pt1 - HLT_obj_pt)/pt1
        dphi2 = (abs(phi2 - HLT_obj_phi))
        deta2 = (abs(eta2 - HLT_obj_eta))
        dpt2 = (abs(pt2 - HLT_obj_pt)/pt2)
        dphi1[dphi1>math.pi] = dphi1[dphi1>math.pi] - 2*math.pi
        dphi2[dphi2>math.pi] = dphi1[dphi2>math.pi] - 2*math.pi
        #print(dphi1)
        triggerMatch = [False, False]
        #if (dphi1 > math.pi): dphi1 -= 2*math.pi
        dR1 = np.sqrt(np.power(dphi1,2) + np.power(deta1,2))
        dR_cut1 = (dR1<0.03)
        dpt_cut1 = (dpt1<0.1)
        #print(dR_cut1)
        dR_dpt_cuts1 = dpt_cut1 & dR_cut1
        #print(dR_dpt_cuts1)
        if dR_dpt_cuts1.any(): triggerMatch[0] = True 
        #if (dphi2 > math.pi): dphi2 -= 2*math.pi
        dR2 = np.sqrt(np.power(dphi2,2) + np.power(deta2,2))
        dR_cut2 = (dR2<0.03)
        dpt_cut2 = (dpt2<0.1)
        #print(dR_cut2)
        dR_dpt_cuts2 = dpt_cut2 & dR_cut2
        #print(dR_dpt_cuts1)
        if dR_dpt_cuts2.any(): triggerMatch[1] = True 
        if(triggerMatch[0] == True): 
            sub_df_selection["mu1_TrMatch"] = True
            triplEff_counter[6] = True
        else:
            sub_df_selection["mu1_TrMatch"] = False
        if(triggerMatch[0] == True and triggerMatch[1] == True):
            sub_df_selection["mu12_TrMatch"] = True
            sub_df_selection["mu123_TrMatch"] = True        
            triplEff_counter[7] = True
            triplEff_counter[8] = True 
        else:
            sub_df_selection["mu12_TrMatch"] = False
            sub_df_selection["mu123_TrMatch"] = False      
    else:
        #triplEff_counter[6] = False
        #triplEff_counter[7] = False
        #triplEff_counter[8] = False
        sub_df_selection["mu1_TrMatch"] = False
        sub_df_selection["mu12_TrMatch"] = False
        sub_df_selection["mu123_TrMatch"] = False  


    return sub_df_selection



def process_event(sub_df, debugMode, cutevt, df_fin, isMC):
    start1 = time.time()
    jentry = sub_df.index[0]
    #print(sub_df)
    L1seed = -99
    HLTpath = -99
    if (debugMode): print(f"\n++++Event n. {jentry}\n")
    triplEff_counter = [False]*NCUTS

    run_n = sub_df.run.iloc[0]
    lumi_n = sub_df.lumi.iloc[0]
    evt_n = sub_df.evt.iloc[0]

    triplEff_counter[0] = True
    ind_good = -99
    mu_good = []
    mu_Ind_good = []
    ind_good = -99
    for i in range(NMU):
        mu_good.append(ind_good)
        mu_Ind_good.append(ind_good)
    goodTriplInd = []

    #CUT 0 : Before cuts - skip event if no good triplets
    if (sub_df.NGoodTriplets.iloc[0][0] < 1):
        cutevt[0]+=1
        return None


    # CUT 1 : Check L1 and HLT decision
    L1_passed = False
    HLT_passed = False
    L1seed = 0
    HLTpath = 0
    L1_DoubleMu0_er1p5 = -99
    L1_DoubleMu0_er1p4= -99
    L1_DoubleMu4_dR1p2= -99
    L1_DoubleMu4p5_dR1p2= -99
    L1_DoubleMu0_er2p0= -99
    L1_DoubleMu0_er2p0_bk= -99
    # ha soddisfatto uno qualsiasi dei L1trigger
    L1_passed = any((("L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4" == sub_df.Trigger_l1name.iloc[0]) | ("L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4" == sub_df.Trigger_l1name.iloc[0]) | ("L1_DoubleMu4_SQ_OS_dR_Max1p2" == sub_df.Trigger_l1name.iloc[0]) | ("L1_DoubleMu4p5_SQ_OS_dR_Max1p2" == sub_df.Trigger_l1name.iloc[0]) | ("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p6" == sub_df.Trigger_l1name.iloc[0]) | ("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5" == sub_df.Trigger_l1name.iloc[0]) ) & (sub_df.Trigger_l1decision.iloc[0] == 1))
    #print(f"L1_passed(after)={L1_passed}")
    if L1_passed:
        L1seed = 1*sum(("L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4" == sub_df.Trigger_l1name.iloc[0]) & (sub_df.Trigger_l1decision.iloc[0] == 1))
        if L1seed >0: L1_DoubleMu0_er1p5=1
        L1seed += 10*sum(("L1_DoubleMu4_SQ_OS_dR_Max1p2" == sub_df.Trigger_l1name.iloc[0]) & (sub_df.Trigger_l1decision.iloc[0] == 1))
        if L1seed >9: L1_DoubleMu4_dR1p2=1
        L1seed += 1000*sum(("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p6" == sub_df.Trigger_l1name.iloc[0]) & (sub_df.Trigger_l1decision.iloc[0] == 1))
        if L1seed >999: L1_DoubleMu0_er2p0=1
        if any((("L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4" == sub_df.Trigger_l1name.iloc[0]) & (sub_df.Trigger_l1decision.iloc[0] == 1))): L1_DoubleMu0_er1p4 = 1
        if any((("L1_DoubleMu4p5_SQ_OS_dR_Max1p2" == sub_df.Trigger_l1name.iloc[0]) & (sub_df.Trigger_l1decision.iloc[0] == 1))): L1_DoubleMu4p5_dR1p2 = 1
        if any((("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5" == sub_df.Trigger_l1name.iloc[0]) & (sub_df.Trigger_l1decision.iloc[0] == 1))): L1_DoubleMu0_er2p0_bk=1
        if debugMode : print(f"L1_seed (after) = {L1seed}")
        triplEff_counter[1] = True
        if (debugMode): print(f"L1seed: {L1seed}\n")
    else:
        cutevt[0]+=1
        return None
    #check HLT
    HLT_string_DoubleMu3_Trk_Tau3mu_v = "HLT_DoubleMu3_Trk_Tau3mu_v"
    HLT_DoubleMu4_3_LowMass = "HLT_DoubleMu4_3_LowMass"
    HLT_DoubleMu4_LowMass_Displaced = "HLT_DoubleMu4_LowMass_Displaced"
    Trigger_hltname = pd.Series(sub_df.Trigger_hltname.iloc[0])
    HLT_passed = any(((Trigger_hltname.str.contains(HLT_string_DoubleMu3_Trk_Tau3mu_v)) ) & (sub_df.Trigger_hltdecision.iloc[0] == 1))
    if HLT_passed:
        HLTpath = 1*sum((Trigger_hltname.str.contains(HLT_string_DoubleMu3_Trk_Tau3mu_v)) & (sub_df.Trigger_hltdecision.iloc[0] == 1))
        HLTpath += 10*sum((Trigger_hltname.str.contains(HLT_DoubleMu4_3_LowMass)) & (sub_df.Trigger_hltdecision.iloc[0] == 1))
        HLTpath += 100*sum((Trigger_hltname.str.contains(HLT_DoubleMu4_LowMass_Displaced)) & (sub_df.Trigger_hltdecision.iloc[0] == 1))
        if debugMode : print(f"HLT_path (after) = {HLTpath}")
        triplEff_counter[1] = True
    else:
        for i in range(2):
            if (debugMode): print(f"triplEff_counter[{i}] = {triplEff_counter[i]}\n")
            if(triplEff_counter[i] == True):
                cutevt[i]+=1
                if(debugMode): print("It's true!")
        return None
    if debugMode: print(f"HLT_path (after) = {HLTpath}")

    HLT_obj_pt = []
    HLT_obj_eta = []
    HLT_obj_phi = []

    if (HLTpath==1 or HLTpath==11 or HLTpath==101 or HLTpath==111):
        print(f"HLT: {sub_df.MuonPt_HLT2017.iloc[0]}")
        print(HLT_obj_pt)
        HLT_obj_pt.append(sub_df.MuonPt_HLT2017.iloc[0])
        HLT_obj_eta.append(sub_df.MuonEta_HLT2017.iloc[0])
        HLT_obj_phi.append(sub_df.MuonPhi_HLT2017.iloc[0])
    else:
        if(HLTpath>=100):
            print(f"HLT2: {sub_df.MuonPt_HLT2017.iloc[0]}")
            HLT_obj_pt.append(sub_df.MuonPt_HLT_DiMu_Incl_displ.iloc[0])
            print(HLT_obj_pt)
            HLT_obj_eta.append(sub_df.MuonEta_HLT_DiMu_Incl_displ.iloc[0])
            HLT_obj_phi.append(sub_df.MuonPhi_HLT_DiMu_Incl_displ.iloc[0])
        else:
            print(f"HLT3: {sub_df.MuonPt_HLT2017.iloc[0]}")
            HLT_obj_pt.append(sub_df.MuonPt_HLT_DiMu_Incl.iloc[0])
            HLT_obj_eta.append(sub_df.MuonEta_HLT_DiMu_Incl.iloc[0])
            HLT_obj_phi.append(sub_df.MuonPhi_HLT_DiMu_Incl.iloc[0])
    #Loop over the TRIPLETS
    start_triplet = time.time()
    #print(sub_df.Mu01_Pt.iloc[0])
    nr_triplets = len(sub_df.Mu01_Pt.iloc[0])
    #print(f"number of triplets: {nr_triplets}")
    triplet_df = pd.DataFrame({"pt": sub_df.Mu01_Pt.iloc[0], "eta": sub_df.Mu01_Eta.iloc[0], "phi": sub_df.Mu01_Phi.iloc[0], "mu_ind_2": np.arange(len(sub_df.Mu01_Pt.iloc[0])), "FlightDistBS_SV_Significance": sub_df.FlightDistBS_SV_Significance.iloc[0],"Triplet2_Mass": sub_df.Triplet2_Mass.iloc[0],  "number_of_triplet": np.arange(nr_triplets),"index_triplet": 0, "mu_index":None})
    triplet_df = pd.concat([triplet_df, pd.DataFrame({"pt": sub_df.Mu02_Pt.iloc[0], "eta": sub_df.Mu02_Eta.iloc[0], "phi": sub_df.Mu02_Phi.iloc[0], "mu_ind_2": np.arange(len(sub_df.Mu02_Pt.iloc[0])),"FlightDistBS_SV_Significance": sub_df.FlightDistBS_SV_Significance.iloc[0],"Triplet2_Mass": sub_df.Triplet2_Mass.iloc[0], "number_of_triplet": np.arange(nr_triplets), "index_triplet": 1, "mu_index":None})], ignore_index = True)
    triplet_df = pd.concat([triplet_df, pd.DataFrame({"pt": sub_df.Tr_Pt.iloc[0], "eta": sub_df.Tr_Eta.iloc[0], "phi": sub_df.Tr_Phi.iloc[0], "mu_ind_2": np.arange(len(sub_df.Tr_Pt.iloc[0])),"FlightDistBS_SV_Significance": sub_df.FlightDistBS_SV_Significance.iloc[0],"Triplet2_Mass": sub_df.Triplet2_Mass.iloc[0],"number_of_triplet": np.arange(nr_triplets), "index_triplet": 2, "mu_index":None})], ignore_index = True)
    stop_triplet1 = time.time()
    print(F"dtime1 = {stop_triplet1-start_triplet}")
    triplet_df = triplet_df.groupby(triplet_df.index).apply(twoMuonsTrkFinder, sub_df)
    stop_triplet2 = time.time()
    print(F"dtime2 = {stop_triplet2-stop_triplet1}")
    # CUT 2 : 2 Glb and Medium mu
    triplet_df = triplet_df.groupby(triplet_df.number_of_triplet).apply(goodTriplet_selection, sub_df, debugMode, triplEff_counter, HLT_obj_phi, HLT_obj_eta, HLT_obj_pt,jentry, df_fin, isMC, ind_good, mu_Ind_good, mu_good, lumi_n, run_n, evt_n, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2,L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath)
    triplet_df = triplet_df[(triplet_df.good_muonID == True) & (triplet_df.good_diMuMass == True) & (triplet_df.good_triMuMass == True) & (triplet_df.mu1_TrMatch == True) & (triplet_df.mu12_TrMatch == True) & (triplet_df.mu123_TrMatch == True)]
    if len(triplet_df.number_of_triplet.unique())>1:
        #print(f"more than one good triplet {triplet_df.number_of_triplet.unique()}")
        #print(sub_df)
        ind_good = triplet_df.number_of_triplet.iloc[0]
        mu_good = list(triplet_df.mu_index[triplet_df.number_of_triplet == ind_good])
        mu_Ind_good = list(triplet_df.mu_ind_2[triplet_df.number_of_triplet == ind_good])
        TreeFin_Fill(sub_df, jentry, df_fin, debugMode, isMC, ind_good, mu_Ind_good, mu_good, lumi_n, run_n, evt_n, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2,L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath)#, lumi_n, run_n, evt_n, pileupFactor, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2, L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath, deltaR_max, deltaZ_max, Pmu3, cLP, tKink, segmComp, tripletMass, tripletMassReso, fv_nC, fv_dphi3D, fv_d3D, fv_d3Dsig, d0, nVtx, d0sig, MVA1, MVA2, MVA3, MVASoft1, MVASoft2, MVASoft3,  d0sig_max, mindca_iso, trkRel, Pmu1, Ptmu1, etamu1, phimu1, Pmu2, Ptmu2, etamu2, phimu2, Ptmu3, etamu3, phimu3, dispMu1, dispMu2, dispMu3, xydispMu1, xydispMu2, xydispMu3, P_trip, Pt_trip, eta_trip, nStationsMu1, nStationsMu2, nStationsMu3, Iso03Mu1, Iso03Mu2, Iso03Mu3, Iso05Mu1, Iso05Mu2, Iso05Mu3, nMatchesMu1, nMatchesMu2, nMatchesMu3, timeAtIpInOutMu_sig1, timeAtIpInOutMu_sig2, timeAtIpInOutMu_sig3, cQ_uS, cQ_tK, cQ_gK, cQ_tRChi2, cQ_sRChi2, cQ_Chi2LP, cQ_Chi2LM, cQ_lD, cQ_gDEP, cQ_tM, cQ_gTP, calEn_emMu1, calEn_emMu2, calEn_emMu3, calEn_hadMu1, calEn_hadMu2, calEn_hadMu3, caloComp, fliDistPVSV_Chi2, isMedium1, isMedium2, isGlb1, isTracker1, isLoose1,  isSoft1, isPF1, isRPC1, isSA1, isCalo1, isGlb2, isTracker2, isLoose2,  isSoft2, isPF2, isRPC2, isSA2, isCalo2, isGlb3, isTracker3, isLoose3,  isSoft3, isPF3, isRPC3, isSA3, isCalo3, vx1, vx2, vx3, vy1, vy2, vy3, vz1, vz2, vz3, Refvx1, Refvx2, Refvx3, Refvy1, Refvy2, Refvy3, Refvz1, Refvz2, Refvz3, SVx, SVy, SVz, had03, had05, nJets03, nJets05, nTracks03, nTracks05, sumPt03, sumPt05, hadVeto03, hadVeto05, emVeto03, emVeto05, trVeto03, trVeto05, EnMu1, EnMu2, EnMu3, ChargeMu1, ChargeMu2, ChargeMu3, isQValid1, isTValid1, isIsoValid1, GLnormChi2_mu1, GL_nValidMuHits1, trkLayersWMeas1, nValidPixelHits1, outerTrk_P_1, outerTrk_Eta_1, outerTrk_normChi2_1, outerTrk_muStValidHits_1, innerTrk_P_1, innerTrk_Eta_1, innerTrk_normChi2_1, QInnerOuter_1, cQ_uS_1, cQ_tK_1, cQ_gK_1, cQ_tRChi2_1, cQ_sRChi2_1, cQ_Chi2LP_1, cQ_Chi2LM_1, cQ_lD_1, cQ_gDEP_1, cQ_tM_1, cQ_gTP_1, segmComp_1, caloComp_1, isQValid2, isTValid2, isIsoValid2, GLnormChi2_mu2, GL_nValidMuHits2, trkLayersWMeas2, nValidPixelHits2, outerTrk_P_2, outerTrk_Eta_2, outerTrk_normChi2_2, outerTrk_muStValidHits_2, innerTrk_P_2, innerTrk_Eta_2, innerTrk_normChi2_2, QInnerOuter_2, cQ_uS_2, cQ_tK_2, cQ_gK_2, cQ_tRChi2_2, cQ_sRChi2_2, cQ_Chi2LP_2, cQ_Chi2LM_2, cQ_lD_2, cQ_gDEP_2, cQ_tM_2, cQ_gTP_2, segmComp_2, caloComp_2, isQValid3, isTValid3, isIsoValid3, GLnormChi2_mu3, GL_nValidMuHits3, trkLayersWMeas3, nValidPixelHits3, outerTrk_P_3, outerTrk_Eta_3, outerTrk_normChi2_3, outerTrk_muStValidHits_3, innerTrk_P_3, innerTrk_Eta_3, innerTrk_normChi2_3, QInnerOuter_3, cQ_uS_3, cQ_tK_3, cQ_gK_3, cQ_tRChi2_3, cQ_sRChi2_3, cQ_Chi2LP_3, cQ_Chi2LM_3, cQ_lD_3, cQ_gDEP_3, cQ_tM_3, cQ_gTP_3, segmComp_3, caloComp_3, match1_dX_1, match1_pullX_1, match1_pullDxDz_1, match1_dY_1, match1_pullY_1, match1_pullDyDz_1, match2_dX_1, match2_pullX_1, match2_pullDxDz_1, match2_dY_1, match2_pullY_1, match2_pullDyDz_1, match1_dX_2, match1_pullX_2, match1_pullDxDz_2, match1_dY_2, match1_pullY_2, match1_pullDyDz_2, match2_dX_2, match2_pullX_2, match2_pullDxDz_2, match2_dY_2, match2_pullY_2, match2_pullDyDz_2, match1_dX_3, match1_pullX_3, match1_pullDxDz_3, match1_dY_3, match1_pullY_3, match1_pullDyDz_3, match2_dX_3, match2_pullX_3, match2_pullDxDz_3, match2_dY_3, match2_pullY_3, match2_pullDyDz_3, innerTrk_highPurity_1, innerTrk_highPurity_2, innerTrk_highPurity_3, innerTrk_ValidFraction_1, innerTrk_ValidFraction_2, innerTrk_ValidFraction_3, nValidTrackerHits1, nValidTrackerHits2, nValidTrackerHits3, validMuonHitComb1, validMuonHitComb2, validMuonHitComb3)

    elif len(triplet_df.number_of_triplet.unique()) == 1:
        #print(f"good triplet {triplet_df.number_of_triplet.iloc[0]}")
        #print(sub_df)
        ind_good = triplet_df.number_of_triplet.iloc[0]
        mu_good = list(triplet_df.mu_index[triplet_df.number_of_triplet == ind_good])
        #print(mu_good)
        mu_Ind_good = list(triplet_df.mu_ind_2[triplet_df.number_of_triplet == ind_good])
        #print(mu_Ind_good)
        #print(sub_df.Mu01_Pt.iloc[0])
        TreeFin_Fill(sub_df, jentry, df_fin, debugMode, isMC, ind_good, mu_Ind_good, mu_good, lumi_n, run_n, evt_n, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2,L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath)#, lumi_n, run_n, evt_n, pileupFactor, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2, L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath, deltaR_max, deltaZ_max, Pmu3, cLP, tKink, segmComp, tripletMass, tripletMassReso, fv_nC, fv_dphi3D, fv_d3D, fv_d3Dsig, d0, nVtx, d0sig, MVA1, MVA2, MVA3, MVASoft1, MVASoft2, MVASoft3,  d0sig_max, mindca_iso, trkRel, Pmu1, Ptmu1, etamu1, phimu1, Pmu2, Ptmu2, etamu2, phimu2, Ptmu3, etamu3, phimu3, dispMu1, dispMu2, dispMu3, xydispMu1, xydispMu2, xydispMu3, P_trip, Pt_trip, eta_trip, nStationsMu1, nStationsMu2, nStationsMu3, Iso03Mu1, Iso03Mu2, Iso03Mu3, Iso05Mu1, Iso05Mu2, Iso05Mu3, nMatchesMu1, nMatchesMu2, nMatchesMu3, timeAtIpInOutMu_sig1, timeAtIpInOutMu_sig2, timeAtIpInOutMu_sig3, cQ_uS, cQ_tK, cQ_gK, cQ_tRChi2, cQ_sRChi2, cQ_Chi2LP, cQ_Chi2LM, cQ_lD, cQ_gDEP, cQ_tM, cQ_gTP, calEn_emMu1, calEn_emMu2, calEn_emMu3, calEn_hadMu1, calEn_hadMu2, calEn_hadMu3, caloComp, fliDistPVSV_Chi2, isMedium1, isMedium2, isGlb1, isTracker1, isLoose1,  isSoft1, isPF1, isRPC1, isSA1, isCalo1, isGlb2, isTracker2, isLoose2,  isSoft2, isPF2, isRPC2, isSA2, isCalo2, isGlb3, isTracker3, isLoose3,  isSoft3, isPF3, isRPC3, isSA3, isCalo3, vx1, vx2, vx3, vy1, vy2, vy3, vz1, vz2, vz3, Refvx1, Refvx2, Refvx3, Refvy1, Refvy2, Refvy3, Refvz1, Refvz2, Refvz3, SVx, SVy, SVz, had03, had05, nJets03, nJets05, nTracks03, nTracks05, sumPt03, sumPt05, hadVeto03, hadVeto05, emVeto03, emVeto05, trVeto03, trVeto05, EnMu1, EnMu2, EnMu3, ChargeMu1, ChargeMu2, ChargeMu3, isQValid1, isTValid1, isIsoValid1, GLnormChi2_mu1, GL_nValidMuHits1, trkLayersWMeas1, nValidPixelHits1, outerTrk_P_1, outerTrk_Eta_1, outerTrk_normChi2_1, outerTrk_muStValidHits_1, innerTrk_P_1, innerTrk_Eta_1, innerTrk_normChi2_1, QInnerOuter_1, cQ_uS_1, cQ_tK_1, cQ_gK_1, cQ_tRChi2_1, cQ_sRChi2_1, cQ_Chi2LP_1, cQ_Chi2LM_1, cQ_lD_1, cQ_gDEP_1, cQ_tM_1, cQ_gTP_1, segmComp_1, caloComp_1, isQValid2, isTValid2, isIsoValid2, GLnormChi2_mu2, GL_nValidMuHits2, trkLayersWMeas2, nValidPixelHits2, outerTrk_P_2, outerTrk_Eta_2, outerTrk_normChi2_2, outerTrk_muStValidHits_2, innerTrk_P_2, innerTrk_Eta_2, innerTrk_normChi2_2, QInnerOuter_2, cQ_uS_2, cQ_tK_2, cQ_gK_2, cQ_tRChi2_2, cQ_sRChi2_2, cQ_Chi2LP_2, cQ_Chi2LM_2, cQ_lD_2, cQ_gDEP_2, cQ_tM_2, cQ_gTP_2, segmComp_2, caloComp_2, isQValid3, isTValid3, isIsoValid3, GLnormChi2_mu3, GL_nValidMuHits3, trkLayersWMeas3, nValidPixelHits3, outerTrk_P_3, outerTrk_Eta_3, outerTrk_normChi2_3, outerTrk_muStValidHits_3, innerTrk_P_3, innerTrk_Eta_3, innerTrk_normChi2_3, QInnerOuter_3, cQ_uS_3, cQ_tK_3, cQ_gK_3, cQ_tRChi2_3, cQ_sRChi2_3, cQ_Chi2LP_3, cQ_Chi2LM_3, cQ_lD_3, cQ_gDEP_3, cQ_tM_3, cQ_gTP_3, segmComp_3, caloComp_3, match1_dX_1, match1_pullX_1, match1_pullDxDz_1, match1_dY_1, match1_pullY_1, match1_pullDyDz_1, match2_dX_1, match2_pullX_1, match2_pullDxDz_1, match2_dY_1, match2_pullY_1, match2_pullDyDz_1, match1_dX_2, match1_pullX_2, match1_pullDxDz_2, match1_dY_2, match1_pullY_2, match1_pullDyDz_2, match2_dX_2, match2_pullX_2, match2_pullDxDz_2, match2_dY_2, match2_pullY_2, match2_pullDyDz_2, match1_dX_3, match1_pullX_3, match1_pullDxDz_3, match1_dY_3, match1_pullY_3, match1_pullDyDz_3, match2_dX_3, match2_pullX_3, match2_pullDxDz_3, match2_dY_3, match2_pullY_3, match2_pullDyDz_3, innerTrk_highPurity_1, innerTrk_highPurity_2, innerTrk_highPurity_3, innerTrk_ValidFraction_1, innerTrk_ValidFraction_2, innerTrk_ValidFraction_3, nValidTrackerHits1, nValidTrackerHits2, nValidTrackerHits3, validMuonHitComb1, validMuonHitComb2, validMuonHitComb3)
    else:
        print("no good triplet")
    stop1 = time.time()
    dtime1 = stop1 -start1
    print(f"tempo impegato a processare un evento: {dtime1}")
        #print(f"event: {jentry}\n{df_fin}")

def process_df(df):   
    print(df)

def Loop_DsPhiPi(tree, type, datasetName, filename):
    df = tree
    #print(df)
    length = len(df)
    #print(length)
    if length==0: return
    nentries = length

    listCut = ["BeforeCuts", "L1_fired", "HLT_fired", "MuonID", "DiMu_mass", "TriMu_mass", "mu1_TrMatch", "mu12_TrMatch", "mu123_TrMatch"]
    debugMode = False
    headers = pd.read_csv("headers.csv")
    df_fin = pd.DataFrame(index = range(nentries), columns = headers.columns)

    if("2022" in datasetName or "2023" in datasetName): isMC=0
    else: isMC=5
    
    df.groupby(df.index).apply(process_event, debugMode, cutevt, df_fin, isMC)

    # Convert the DataFrame into a dictionary of arrays (one for each column)
    arrays = {col: df_fin[col].values for col in df_fin.columns}

    # Open a ROOT file and write the TTree
    with uproot.recreate(filename) as root_file:
        root_file["FinalTree"] = arrays  # Write the arrays to the tree
    #df_fin.Snapshot("FinalTree", filename)


