import ROOT
import math
import pandas as pd
import uproot

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
    print(len(nameCut))
    print(NCUTS)
    if len(nameCut) != NCUTS: 
        print("length of the cut names does not match number of cuts")
        return
    for i in range(NCUTS):
        listCut.append(nameCut[i])
    
def Draw_CutEffCanvas(df, canv, hist, cut, listCut):
    print(cut)
    for k in range(len(listCut)):
        hist.Fill(k+1, cut[k])
        hist.GetXaxis().SetBinLabel(k+1, listCut[k])
    hist.DrawCopy("HIST TEXT0")
    hist.Write()

    
def Get_MuonAndTrackVariables(df, mu_Ind, pt, eta, phi):
    pt[0] = df.Mu01_Pt.iloc[0][mu_Ind[0]]
    pt[1] = df.Mu02_Pt.iloc[0][mu_Ind[1]]
    pt[2] = df.Tr_Pt.iloc[0][mu_Ind[2]]
    eta[0] = df.Mu01_Eta.iloc[0][mu_Ind[0]]
    eta[1] = df.Mu02_Eta.iloc[0][mu_Ind[1]]
    eta[2] = df.Tr_Eta.iloc[0][mu_Ind[2]]
    phi[0] = df.Mu01_Phi.iloc[0][mu_Ind[0]]
    phi[1] = df.Mu02_Phi.iloc[0][mu_Ind[1]]
    phi[2] = df.Tr_Phi.iloc[0][mu_Ind[2]]

def MatchIndex(df, type, ind, mu_Ind, mu):
    mu_Ind[0] = ind
    mu_Ind[1] = ind
    mu_Ind[2] = ind
    if (mu_Ind[0] != ind or mu_Ind[1] != ind or mu_Ind[2] != ind):
        print("Error : Different triplet mu indices!")
    pt = []
    eta = []
    phi = []
    for i in range(NMU):
        pt.append(0)
        eta.append(0)
        phi.append(0)
    Get_MuonAndTrackVariables(df, mu_Ind, pt, eta, phi)
    if type == "ID":
        for k in range(NMU-1):
            mu[k] = MuonFinder(df, pt[k], eta[k], phi[k])
        mu[2] = TrackFinder(df, pt[2], eta[2], phi[2])

def MuonFinder(df, pt, eta, phi):
    # Given the characteristics of a muon (pt, eta, phi), the function returns the index of the corresponding muon in the event
    
    # PRIORITY [in case there is more than 1 muon that matches the conditions]
    
    # *** if (there aren't muons w/ outerTrachChi2 != -999)    ## CASE 0 ##
    #      -> consider the one w/ the smallest innerTrackChi2
    #      -> if innerTrackChi2 are equal:
    #          -> consider the one w/ the biggest number of matches
    #           (if they are equal, print an error message and return the index of the last one)
    #
    # *** if (outerTrack != -999)                              ## CASE 1,2 ##
    #      -> consider the one w/ the smallest outerTrackChi2
    #      -> if outerTrackChi2 are equal:
    #          -> consider the one w/ the smallest innerTrackChi2
    #              -> consider the one w/ the biggest number of matches
    #                   (if they are equal, print an error message and return the index of the last one)
    n = 0
    m = 0
    badOuterChi2 = 0
    for g in range(len(df.MuonPt.iloc[0])):
        if (pt == df.MuonPt.iloc[0][g] and eta == df.MuonEta.iloc[0][g] and phi == df.MuonPhi.iloc[0][g]):
            n+=1
            m = g
            if(df.Muon_outerTrack_normalizedChi2.iloc[0][g] == -999):
                badOuterChi2+=1
        
    
    #MULTIPLE muons (There is more than 1 muon that matches the conditions)
    if n>1:
        
        ####### CASE 0: there aren't muons w/ outerTrachChi2 != -999
        if (n-badOuterChi2) == 0:
            Chi2InnerTrackmin = [0,0] # Chi2InnerTrackmin[1] is the value of Chi2; Chi2InnerTrackmin[0] is the corresponding index
            Chi2InnerTrackmin[1] = 999
            # find the muon w/ the smallest innerTrackChi2
            for k in range(len(df.MuonPt.iloc[0])):
                if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and df.Muon_innerTrack_normalizedChi2.iloc[0][k] < Chi2InnerTrackmin[1]):
                    Chi2InnerTrackmin[1] = df.Muon_innerTrack_normalizedChi2.iloc[0][k]
                    Chi2InnerTrackmin[0] = k
            nMuonChi2InnerMin = 0
            for k in range(len(df.MuonPt.iloc[0])):
                if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and Chi2InnerTrackmin[1] == df.Muon_innerTrack_normalizedChi2.iloc[0][k]):
                    nMuonChi2InnerMin+=1
            if (nMuonChi2InnerMin == 1):
                return Chi2InnerTrackmin[0]
            # find the mu w/ the biggest number of matches
            else:
                NumberOfMatches = [0,0] #like Chi2InnerTrackmin[]
                for k in range(len(df.MuonPt.iloc[0])):
                    if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and Chi2InnerTrackmin[1] == df.Muon_innerTrack_normalizedChi2.iloc[0][k]):
                        if (df.Muon_numberOfMatches.iloc[0][k] > NumberOfMatches[1]):
                            NumberOfMatches[1] = df.Muon_numberOfMatches.iloc[0][k]
                            NumberOfMatches[0] = k

            nMuonMatchesMax = 0
            for k in range(len(df.MuonPt)):
                if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and Chi2InnerTrackmin[1] == df.Muon_innerTrack_normalizedChi2.iloc[0][k] and NumberOfMatches[1] == df.Muon_numberOfMatches.iloc[0][k]):
                    nMuonMatchesMax+=1
            if (nMuonMatchesMax == 1):
                return NumberOfMatches[0]
            # They are equal, therefore print an error message and return the index of the last one
            else:
                print("Multiple muons with outerChi2 = -999! ")
                return NumberOfMatches[0]
    
        ####### CASE 1:  // There is ONLY 1 muon that has outerTrachChi2 != -999
        elif ((n-badOuterChi2) == 1): 
            # Find this muon and return its index
            indexGoodMu = -1
            for k in range(len(df.MuonPt.iloc[0])):
                if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and df.Muon_outerTrack_normalizedChi2.iloc[0][k] != -999):
                    indexGoodMu = k
        
            if (indexGoodMu == -1):
                print("There is a BUG for sure !!!")

            return indexGoodMu
    
        ####### CASE 2:  // There is more than 1 muon w/ outerTrachChi2 != -999
        elif (n-badOuterChi2) > 1:
            Chi2OuterTrackmin = [0,0]
            Chi2OuterTrackmin[1] = 999
            # find the one w/ the smallest outerTrackChi2
            for k in range(len(df.MuonPt.iloc[0])):
                if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and df.Muon_outerTrack_normalizedChi2.iloc[0][k] < Chi2OuterTrackmin[1]):
                    Chi2OuterTrackmin[1] = df.Muon_outerTrack_normalizedChi2.iloc[0][k]
                    Chi2OuterTrackmin[0] = k
            nMuonChi2OuterMin = 0
            for k in range(len(df.MuonPt)):
                if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and Chi2OuterTrackmin[1] == df.Muon_outerTrack_normalizedChi2.iloc[0][k]):
                    nMuonChi2OuterMin+=1
            if(nMuonChi2OuterMin == 1):  return Chi2OuterTrackmin[0]
            # if outerTrackChi2 are equal
            else:
                # consider the one w/ the smallest innerTrackChi2
                Chi2InnerTrackmin = [0,0]
                Chi2InnerTrackmin[1] = 999
                for k in range(len(df.MuonPt.iloc[0])):
                    if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and df.Muon_outerTrack_normalizedChi2.iloc[0][k] == Chi2OuterTrackmin[1] and df.Muon_innerTrack_normalizedChi2.iloc[0][k] < Chi2InnerTrackmin[1]):
                        Chi2InnerTrackmin[1] = df.Muon_innerTrack_normalizedChi2.iloc[0][k]
                        Chi2InnerTrackmin[0] = k
            
                nMuonChi2InnerMin = 0
                for k in range(len(df.MuonPt.iloc[0])):
                    if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and df.Muon_outerTrack_normalizedChi2.iloc[0][k] == Chi2OuterTrackmin[1] and Chi2InnerTrackmin[1] == df.Muon_innerTrack_normalizedChi2.iloc[0][k]):
                        nMuonChi2InnerMin+=1
                if(nMuonChi2InnerMin == 1): return Chi2InnerTrackmin[0]
                # find the one w/ the biggest number of matches
                else:
                    NumberOfMatches = [0,0]
                    for k in range(len(df.MuonPt.iloc[0])):
                        if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and df.Muon_outerTrack_normalizedChi2.iloc[0][k] == Chi2OuterTrackmin[1] and Chi2InnerTrackmin[1] == df.Muon_innerTrack_normalizedChi2.iloc[0][k]):
                            if(df.Muon_numberOfMatches.iloc[0][k] > NumberOfMatches[1]):
                                NumberOfMatches[1] = df.Muon_numberOfMatches.iloc[0][k]
                                NumberOfMatches[0] = k
                    nMuonMatchesMax = 0
                    for k in range(len(df.MuonPt.iloc[0])):
                        if (pt == df.MuonPt.iloc[0][k] and eta == df.MuonEta.iloc[0][k] and phi == df.MuonPhi.iloc[0][k] and df.Muon_outerTrack_normalizedChi2.iloc[0][k] == Chi2OuterTrackmin[1] and Chi2InnerTrackmin[1] == df.Muon_innerTrack_normalizedChi2.iloc[0][k] and NumberOfMatches[1] == df.Muon_numberOfMatches.iloc[0][k]):
                            nMuonMatchesMax+=1
                    if (nMuonMatchesMax == 1): return NumberOfMatches[0]
                    # They are equal, therefore print an error message and return the index of the last one
                    else:
                        print("Multiple muons with outerChi2 != -999! ")
                        return NumberOfMatches[0]
        else: # Error
            print("ERROR in multiple muon number!")
            return m
    # end multiple muons section

    else:
        return m

def MuonP(df, pt, eta, phi):
    muon = ROOT.TVector3()
    muon.SetPtEtaPhi(pt, eta, phi)
    return muon.Mag()

def TrackFinder(df, pt, eta, phi):
    n = 0
    m = 0
    badChi2 = 0
    for g in range(len(df.Track_pt.iloc[0])):
        if pt == df.Track_pt.iloc[0][g] and eta == df.Track_eta.iloc[0][g] and phi == df.Track_phi.iloc[0][g]:
            n += 1
            m = g
            if df.Track_normalizedChi2.iloc[0][g] == -999:
                badChi2 += 1
    if n>1: print("Error: There is more than 1 track that matches the conditions!")
    elif n == 0: print("Error: There is NOT a track that matches the condition!")
    return m

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


def open_root_file(tree, fname):
    #if not tree:
        #return
    # Open a ROOT file and extract the tree
    '''
    file = uproot.open(fname)
    file.classnames()
    tree = file[""]

    # Convert the tree into a pandas DataFrame
    tree_dataframe = tree.arrays(library="pd")

    # Get the columns of the dataframe
    columns = tree_dataframe.columns
    print(columns)
    '''
    fCurrent = -1
    return tree_dataframe
    #self.fChain.SetMakeClass(1)

def TreeFin_Fill(df, jentry, df_fin, isMC, debugMode, ind, mu_Ind, mu, lumi, run, evt, puFactor, L1_DoubleMu0_er1p5,
                L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2, L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath, DeltaR_max,
                DeltaZ_max, Pmu3, cLP, tKink, segmComp, tripletMass, tripletMassReso, fv_nC, fv_dphi3D, fv_d3D,  fv_d3Dsig, d0, nVtx, d0sig, MVA1, MVA2,
                MVA3, MVASoft1, MVASoft2, MVASoft3, d0sig_max, mindca_iso, trkRel, Pmu1, Ptmu1, etamu1, phimu1, Pmu2, Ptmu2, etamu2, phimu2, Ptmu3, etamu3,
                phimu3, dispMu1, dispMu2, dispMu3, xydispMu1, xydispMu2, xydispMu3, P_trip, Pt_trip, eta_trip, nStationsMu1, nStationsMu2, nStationsMu3, 
                Iso03Mu1, Iso03Mu2, Iso03Mu3, Iso05Mu1, Iso05Mu2, Iso05Mu3, nMatchesMu1, nMatchesMu2, nMatchesMu3, timeAtIpInOut_sig1, timeAtIpInOut_sig2, 
                timeAtIpInOut_sig3, cQ_uS, cQ_tK, cQ_gK, cQ_tRChi2, cQ_sRChi2, cQ_Chi2LP, cQ_Chi2LM, cQ_lD, cQ_gDEP, cQ_tM, cQ_gTP, calEn_emMu1, calEn_emMu2, 
                calEn_emMu3, calEn_hadMu1, calEn_hadMu2, calEn_hadMu3, caloComp, fliDistPVSV_Chi2, isMedium1, isMedium2, isGlb1, isTracker1, isLoose1, isSoft1, 
                isPF1, isRPC1, isSA1, isCalo1, isGlb2, isTracker2, isLoose2, isSoft2, isPF2, isRPC2, isSA2, isCalo2, isGlb3, isTracker3, isLoose3, isSoft3, isPF3, isRPC3, 
                isSA3, isCalo3, Vx1, Vx2, Vx3, Vy1, Vy2, Vy3, Vz1, Vz2, Vz3, RefVx1, RefVx2, RefVx3, RefVy1, RefVy2, RefVy3, RefVz1, RefVz2, RefVz3, SVx, SVy, SVz, had03, 
                had05, nJets03, nJets05, nTracks03, nTracks05, sumPt03, sumPt05, hadVeto03, hadVeto05, emVeto03, emVeto05, trVeto03, trVeto05, EnMu1, EnMu2, EnMu3, ChargeMu1, 
                ChargeMu2, ChargeMu3, isQValid1, isTValid1, isIsoValid1, GLnormChi2_mu1, GL_nValidMuHits1, trkLayersWMeas1, nValidPixelHits1, outerTrk_P_1, outerTrk_Eta_1, 
                outerTrk_normChi2_1, outerTrk_muStValidHits_1, innerTrk_P_1, innerTrk_Eta_1, innerTrk_normChi2_1, QInnerOuter_1, cQ_uS_1, cQ_tK_1, cQ_gK_1, cQ_tRChi2_1, cQ_sRChi2_1, 
                cQ_Chi2LP_1, cQ_Chi2LM_1, cQ_lD_1, cQ_gDEP_1, cQ_tM_1, cQ_gTP_1, segmComp_1, caloComp_1, isQValid2, isTValid2, isIsoValid2, GLnormChi2_mu2, GL_nValidMuHits2,
                trkLayersWMeas2, nValidPixelHits2, outerTrk_P_2, outerTrk_Eta_2, outerTrk_normChi2_2, outerTrk_muStValidHits_2, innerTrk_P_2, innerTrk_Eta_2, innerTrk_normChi2_2, QInnerOuter_2,
                cQ_uS_2, cQ_tK_2, cQ_gK_2, cQ_tRChi2_2, cQ_sRChi2_2, cQ_Chi2LP_2, cQ_Chi2LM_2, cQ_lD_2, cQ_gDEP_2, cQ_tM_2, cQ_gTP_2, segmComp_2, caloComp_2, isQValid3, isTValid3, isIsoValid3,
                GLnormChi2_mu3, GL_nValidMuHits3, trkLayersWMeas3, nValidPixelHits3, outerTrk_P_3, outerTrk_Eta_3, outerTrk_normChi2_3, outerTrk_muStValidHits_3, innerTrk_P_3, innerTrk_Eta_3, 
                innerTrk_normChi2_3, QInnerOuter_3, cQ_uS_3, cQ_tK_3, cQ_gK_3, cQ_tRChi2_3, cQ_sRChi2_3, cQ_Chi2LP_3, cQ_Chi2LM_3, cQ_lD_3, cQ_gDEP_3, cQ_tM_3, 
                cQ_gTP_3, segmComp_3, caloComp_3, match1_dX_1, match1_pullX_1, match1_pullDxDz_1, match1_dY_1, match1_pullY_1, match1_pullDyDz_1, match2_dX_1, match2_pullX_1, 
                match2_pullDxDz_1, match2_dY_1, match2_pullY_1, match2_pullDyDz_1, match1_dX_2, match1_pullX_2, match1_pullDxDz_2, match1_dY_2, match1_pullY_2, match1_pullDyDz_2, match2_dX_2, 
                match2_pullX_2, match2_pullDxDz_2, match2_dY_2, match2_pullY_2, match2_pullDyDz_2, match1_dX_3, match1_pullX_3, match1_pullDxDz_3, match1_dY_3, match1_pullY_3, match1_pullDyDz_3, match2_dX_3, 
                match2_pullX_3, match2_pullDxDz_3, match2_dY_3, match2_pullY_3, match2_pullDyDz_3, innerTrk_highPurity_1, innerTrk_highPurity_2, innerTrk_highPurity_3, innerTrk_ValidFraction_1, innerTrk_ValidFraction_2, 
                innerTrk_ValidFraction_3, nValidTrackerHits1, nValidTrackerHits2, nValidTrackerHits3, validMuonHitComb1, validMuonHitComb2, validMuonHitComb3):
    print("il baco è qui")
    if debugMode:
        print("Ciao1")
    MatchIndex(df, "ID", ind, mu_Ind, mu)
    pt = []
    eta = []
    phi = []
    temp1 = []
    temp = []
    dR = []
    dZ = []
    for i in range(NMU):
        pt.append(0)
        eta.append(0)
        phi.append(0)
        temp1.append(0)
        temp.append(0)
        dR.append(0)
        dZ.append(0)
    Get_MuonAndTrackVariables(df, mu_Ind, pt, eta, phi)
    Pmu3 = MuonP(df, pt[2], eta[2], phi[2])
    cLP = -999
    tKink = -999
    segmComp = 999
    DeltaR_max = -999
    DeltaZ_max = -999
    temp1[0] = df.dxy_mu1.iloc[0][mu_Ind[0]]
    temp1[1] = df.dxy_mu2.iloc[0][mu_Ind[1]]
    temp1[2] = df.dxy_mu3.iloc[0][mu_Ind[2]]
    dR[0] = math.sqrt(pow((eta[0]-eta[1]),2)+pow((phi[0]-phi[1]),2))
    dR[1] = math.sqrt(pow((eta[0]-eta[2]),2)+pow((phi[0]-phi[2]),2))
    dR[2] = math.sqrt(pow((eta[2]-eta[1]),2)+pow((phi[2]-phi[1]),2))
    dZ[0] = abs(df.Muon_vz.iloc[0][mu[0]] - df.Muon_vz.iloc[0][mu[1]] )
    dZ[1] = abs(df.Muon_vz.iloc[0][mu[0]] - df.Track_vz.iloc[0][mu[2]] )
    dZ[2] = abs(df.Track_vz.iloc[0][mu[2]]  - df.Muon_vz.iloc[0][mu[1]] )
    d0 = 999
    temp[0] = abs(df.dxy_mu1.iloc[0][mu_Ind[0]]/ df.dxyErr_mu1.iloc[0][mu_Ind[0]])
    temp[1] = abs(df.dxy_mu2.iloc[0][mu_Ind[1]]/ df.dxyErr_mu2.iloc[0][mu_Ind[1]])
    temp[2] = abs(df.dxy_mu3.iloc[0][mu_Ind[2]]/ df.dxyErr_mu3.iloc[0][mu_Ind[2]])
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
    fv_nC = df.TripletVtx2_Chi2.iloc[0][ind]/3
    fv_dphi3D = TreeFin_Angle(df, ind)
    fv_d3Dsig = df.FlightDistPVSV2_Significance.iloc[0][ind]
    fv_d3D = df.FlightDistPVSV2.iloc[0][ind]
    mindca_iso = df.Triplet_mindca_iso.iloc[0][ind]
    trkRel = df.Triplet_relativeiso.iloc[0][ind]

    if(debugMode): print("Ciao4")


    # Other variables
    # Single mu variables
    if (debugMode): print("Ciao5")
    Pmu1 = MuonP(df, df.Mu01_Pt.iloc[0][mu_Ind[0]], df.Mu01_Eta.iloc[0][mu_Ind[0]], df.Mu01_Phi.iloc[0][mu_Ind[0]])
    Ptmu1 = df.Mu01_Pt.iloc[0][mu_Ind[0]]
    etamu1 = df.Mu01_Eta.iloc[0][mu_Ind[0]]
    phimu1 = df.Mu01_Phi.iloc[0][mu_Ind[0]]
    Pmu2 = MuonP(df, df.Mu02_Pt.iloc[0][mu_Ind[1]], df.Mu02_Eta.iloc[0][mu_Ind[1]], df.Mu02_Phi.iloc[0][mu_Ind[1]])
    Ptmu2 = df.Mu02_Pt.iloc[0][mu_Ind[1]]
    etamu2 = df.Mu02_Eta.iloc[0][mu_Ind[1]]
    phimu2 = df.Mu02_Phi.iloc[0][mu_Ind[1]]
    Ptmu3 = df.Tr_Pt.iloc[0][mu_Ind[2]]
    etamu3 = df.Tr_Eta.iloc[0][mu_Ind[2]]
    phimu3 = df.Tr_Phi.iloc[0][(mu_Ind[2])]

    dispMu1 = math.sqrt(pow(df.BS_x.iloc[0][mu_Ind[0]] - df.Muon_vx.iloc[0][mu[0]],2) + pow(df.BS_y.iloc[0][mu_Ind[0]] - df.Muon_vy.iloc[0][mu[0]],2) + pow(df.BS_z.iloc[0][mu_Ind[0]] - df.Muon_vz.iloc[0][mu[0]],2))
    dispMu2 = math.sqrt(pow(df.BS_x.iloc[0][mu_Ind[1]] - df.Muon_vx.iloc[0][mu[1]],2) + pow(df.BS_y.iloc[0][mu_Ind[1]] - df.Muon_vy.iloc[0][mu[1]],2) + pow(df.BS_z.iloc[0][mu_Ind[1]] - df.Muon_vz.iloc[0][mu[1]],2))
    #dispMu3 = TMath::Sqrt(TMath::Power(BS_x->at(mu_Ind[2]) - Muon_vx->at(mu[2]),2) + TMath::Power(BS_y->at(mu_Ind[2]) - Muon_vy->at(mu[2]),2) + TMath::Power(BS_z->at(mu_Ind[2]) - Muon_vz->at(mu[1]),2));
    xydispMu1 = math.sqrt(pow(df.BS_x.iloc[0][mu_Ind[0]] - df.Muon_vx.iloc[0][mu[0]],2) + pow(df.BS_y.iloc[0][mu_Ind[0]] - df.Muon_vy.iloc[0][mu[0]],2))
    xydispMu2 = math.sqrt(pow(df.BS_x.iloc[0][mu_Ind[1]] - df.Muon_vx.iloc[0][mu[1]],2) + pow(df.BS_y.iloc[0][mu_Ind[1]] - df.Muon_vy.iloc[0][mu[1]],2))
    #xydispMu3 = TMath::Sqrt(TMath::Power(BS_x->at(mu_Ind[2]) - Muon_vx->at(mu[2]),2) + TMath::Power(BS_y->at(mu_Ind[2]) - Muon_vy->at(mu[2]),2));

    if (debugMode): print("Ciao5_bis")
    nStationsMu1 = df.Muon_numberOfMatchedStations.iloc[0][mu[0]]
    nStationsMu2 = df.Muon_numberOfMatchedStations.iloc[0][mu[1]]
    if(debugMode): print("Ciao5_bis2")
    Iso03Mu1 = df.Mu1_NTracks03iso.iloc[0][mu_Ind[0]]
    Iso03Mu2 = df.Mu2_NTracks03iso.iloc[0][mu_Ind[1]]
    Iso03Mu3 = df.Tr_NTracks03iso.iloc[0][mu_Ind[2]]
    Iso05Mu1 = df.Muon_emEt05.iloc[0][mu[0]]
    Iso05Mu2 = df.Muon_emEt05.iloc[0][mu[1]]
    #Iso05Mu3 = Muon_emEt05->at(mu[2]);
    if(debugMode): print("Ciao5_bis3")
    # Triplet variables
    P_trip = MuonP(df, df.Triplet2_Pt.iloc[0][ind], df.Triplet2_Eta.iloc[0][ind], df.Triplet2_Phi.iloc[0][ind])
    Pt_trip = df.Triplet2_Pt.iloc[0][ind]
    eta_trip = df.Triplet2_Eta.iloc[0][ind]
    if(debugMode): print("Ciao6")
    nMatchesMu1 = df.Muon_numberOfMatches.iloc[0][mu[0]]
    nMatchesMu2 = df.Muon_numberOfMatches.iloc[0][mu[1]]
    #nMatchesMu3 = Muon_numberOfMatches->at(mu[2]);
    timeAtIpInOut_sig1 = df.Muon_timeAtIpInOut.iloc[0][mu[0]]/ df.Muon_timeAtIpInOutErr.iloc[0][mu[0]]
    timeAtIpInOut_sig2 = df.Muon_timeAtIpInOut.iloc[0][mu[1]]/ df.Muon_timeAtIpInOutErr.iloc[0][mu[1]]
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
    calEn_emMu1 = df.Muon_calEnergy_em.iloc[0][mu[0]]
    calEn_emMu2 = df.Muon_calEnergy_em.iloc[0][mu[1]]
    #calEn_emMu3 = Muon_calEnergy_em->at(mu[2]);
    calEn_hadMu1 = df.Muon_calEnergy_had.iloc[0][mu[0]]
    calEn_hadMu2 = df.Muon_calEnergy_had.iloc[0][mu[1]]
    #calEn_hadMu3 = Muon_calEnergy_had->at(mu[2]);
    #fliDistPVSV_Chi2 = FlightDistPVSV_chi2->at(ind);
    if(debugMode): print("Ciao7")
    nVtx = df.PVCollection_Size.iloc[0]
    ####muon ID
    isMedium1 = df.Muon_isMedium.iloc[0][mu[0]]
    isMedium2 = df.Muon_isMedium.iloc[0][mu[0]]
    isGlb1 = df.Muon_isGlobal.iloc[0][mu[0]]
    isTracker1 = df.Muon_isTrackerMuon.iloc[0][mu[0]]
    isLoose1 = df.Muon_isLoose.iloc[0][mu[0]]
    isSoft1 = df.Muon_isSoft.iloc[0][mu[0]]
    MVA1 = df.Muon_MVA.iloc[0][mu[0]]
    MVA2 = df.Muon_MVA.iloc[0][mu[1]]
    #MVA3 = Muon_MVA->at(mu[2]);
    MVA3 = 0.
    MVASoft1 = df.Muon_SoftMVA_Val.iloc[0][mu[0]]
    MVASoft2 = df.Muon_SoftMVA_Val.iloc[0][mu[1]]
    #MVASoft3 = Muon_SoftMVA_Val->at(mu[2]);
    MVASoft3 = 0.
    isPF1 = df.Muon_isPF.iloc[0][mu[0]]
    isRPC1 = df.Muon_isRPCMuon.iloc[0][mu[0]]
    isSA1 = df.Muon_isStandAloneMuon.iloc[0][mu[0]]
    isCalo1 = df.Muon_isCaloMuon.iloc[0][mu[0]]
    isGlb2 = df.Muon_isGlobal.iloc[0][mu[1]]
    isTracker2 = df.Muon_isTrackerMuon.iloc[0][mu[1]]
    isLoose2 = df.Muon_isLoose.iloc[0][mu[1]]
    isSoft2 = df.Muon_isSoft.iloc[0][mu[1]]
    isPF2 = df.Muon_isPF.iloc[0][mu[1]]
    isRPC2 = df.Muon_isRPCMuon.iloc[0][mu[1]]
    isSA2 = df.Muon_isStandAloneMuon.iloc[0][mu[1]]
    isCalo2 = df.Muon_isCaloMuon.iloc[0][mu[1]]
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
    if(debugMode): print("Ciao8")
    Vx1 = df.Muon_vx.iloc[0][mu[0]]
    Vx2 = df.Muon_vx.iloc[0][mu[1]]
    Vx3 = df.Track_vx.iloc[0][mu[2]]
    Vy1 = df.Muon_vy.iloc[0][mu[0]]
    Vy2 = df.Muon_vy.iloc[0][mu[1]]
    Vy3 = df.Track_vy.iloc[0][mu[2]]
    Vz1 = df.Muon_vz.iloc[0][mu[0]]
    Vz2 = df.Muon_vz.iloc[0][mu[1]]
    Vz3 = df.Track_vz.iloc[0][mu[2]]
    RefVx1 = df.RefittedPV2_x.iloc[0][ind]
    RefVy1 = df.RefittedPV2_y.iloc[0][ind]
    RefVz1 = df.RefittedPV2_z.iloc[0][ind]
    SVx = df.TripletVtx2_x.iloc[0][ind]
    SVy = df.TripletVtx2_y.iloc[0][ind]
    SVz = df.TripletVtx2_z.iloc[0][ind]
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
    if(debugMode): print("Ciao9")
    EnMu1 = df.MuonEnergy.iloc[0][mu[0]]
    EnMu2 = df.MuonEnergy.iloc[0][mu[1]]
    #EnMu3 = df.MuonEnergy.iloc[0][mu[2]]
    ChargeMu1 = df.MuonCharge.iloc[0][mu[0]]
    ChargeMu2 = df.MuonCharge.iloc[0][mu[1]]
    ChargeMu3 = df.Track_charge.iloc[0][mu[2]]
    #
    # mu1
    if(debugMode): print("Ciao10")
    isQValid1 = df.Muon_isQualityValid.iloc[0][mu[0]]
    isTValid1 = df.Muon_isTimeValid.iloc[0][mu[0]]
    isIsoValid1 = df.Muon_isIsolationValid.iloc[0][mu[0]]
    GLnormChi2_mu1 = df.Muon_GLnormChi2.iloc[0][mu[0]]
    GL_nValidMuHits1 = df.Muon_GLhitPattern_numberOfValidMuonHits.iloc[0][mu[0]]
    trkLayersWMeas1 = df.Muon_trackerLayersWithMeasurement.iloc[0][mu[0]]
    validMuonHitComb1 = df.Muon_validMuonHitComb.iloc[0][mu[0]]
    nValidTrackerHits1 = df.Muon_Numberofvalidtrackerhits.iloc[0][mu[0]]
    nValidPixelHits1 = df.Muon_Numberofvalidpixelhits.iloc[0][mu[0]]
    outerTrk_P_1 = df.Muon_outerTrack_p.iloc[0][mu[0]]
    outerTrk_Eta_1 = df.Muon_outerTrack_eta.iloc[0][mu[0]]
    outerTrk_normChi2_1 = df.Muon_outerTrack_normalizedChi2.iloc[0][mu[0]]
    outerTrk_muStValidHits_1 = df.Muon_outerTrack_muonStationsWithValidHits.iloc[0][mu[0]]
    innerTrk_P_1 = df.Muon_innerTrack_p.iloc[0][mu[0]]
    innerTrk_Eta_1 = df.Muon_innerTrack_eta.iloc[0][mu[0]]
    innerTrk_normChi2_1 = df.Muon_innerTrack_normalizedChi2.iloc[0][mu[0]]
    innerTrk_highPurity_1 = df.Muon_innerTrack_highPurity.iloc[0][mu[0]]
    innerTrk_ValidFraction_1 = df.Muon_innerTrack_ValidFraction.iloc[0][mu[0]]
    QInnerOuter_1 = df.Muon_QInnerOuter.iloc[0][mu[0]]
    cQ_uS_1 = df.Muon_combinedQuality_updatedSta.iloc[0][mu[0]]
    cQ_tK_1 = df.Muon_combinedQuality_trkKink.iloc[0][mu[0]]
    cQ_gK_1 = df.Muon_combinedQuality_glbKink.iloc[0][mu[0]]
    cQ_tRChi2_1 = df.Muon_combinedQuality_trkRelChi2.iloc[0][mu[0]]
    cQ_sRChi2_1 = df.Muon_combinedQuality_staRelChi2.iloc[0][mu[0]]
    cQ_Chi2LP_1 = df.Muon_combinedQuality_chi2LocalPosition.iloc[0][mu[0]]
    cQ_Chi2LM_1 = df.Muon_combinedQuality_chi2LocalMomentum.iloc[0][mu[0]]
    cQ_lD_1 = df.Muon_combinedQuality_localDistance.iloc[0][mu[0]]
    cQ_gDEP_1 = df.Muon_combinedQuality_globalDeltaEtaPhi.iloc[0][mu[0]]
    cQ_tM_1 = df.Muon_combinedQuality_tightMatch.iloc[0][mu[0]]
    cQ_gTP_1 = df.Muon_combinedQuality_glbTrackProbability.iloc[0][mu[0]]
    segmComp_1 = df.Muon_segmentCompatibility.iloc[0][mu[0]]
    caloComp_1 = df.Muon_caloCompatibility.iloc[0][mu[0]]
    match1_dX_1 = df.Muon_combinedQuality_match1_dX.iloc[0][mu[0]]
    match1_pullX_1 = df.Muon_combinedQuality_match1_pullX.iloc[0][mu[0]]
    match1_pullDxDz_1 = df.Muon_combinedQuality_match1_pullDxDz.iloc[0][mu[0]]
    match1_dY_1 = df.Muon_combinedQuality_match1_dY.iloc[0][mu[0]]
    match1_pullY_1 = df.Muon_combinedQuality_match1_pullY.iloc[0][mu[0]]
    match1_pullDyDz_1 = df.Muon_combinedQuality_match1_pullDyDz.iloc[0][mu[0]]
    match2_dX_1 = df.Muon_combinedQuality_match2_dX.iloc[0][mu[0]]
    match2_pullX_1 = df.Muon_combinedQuality_match2_pullX.iloc[0][mu[0]]
    match2_pullDxDz_1 = df.Muon_combinedQuality_match2_pullDxDz.iloc[0][mu[0]]
    match2_dY_1 = df.Muon_combinedQuality_match2_dY.iloc[0][mu[0]]
    match2_pullY_1 = df.Muon_combinedQuality_match2_pullY.iloc[0][mu[0]]
    match2_pullDyDz_1 = df.Muon_combinedQuality_match2_pullDyDz.iloc[0][mu[0]]
    if(debugMode): print("Ciao11")
    # mu2
    isQValid2 = df.Muon_isQualityValid.iloc[0][mu[1]]
    isTValid2 = df.Muon_isTimeValid.iloc[0][mu[1]]
    isIsoValid2 = df.Muon_isIsolationValid.iloc[0][mu[1]]
    GLnormChi2_mu2 = df.Muon_GLnormChi2.iloc[0][mu[1]]
    GL_nValidMuHits2 = df.Muon_GLhitPattern_numberOfValidMuonHits.iloc[0][mu[1]]
    trkLayersWMeas2 = df.Muon_trackerLayersWithMeasurement.iloc[0][mu[1]]
    validMuonHitComb2 = df.Muon_validMuonHitComb.iloc[0][mu[1]]
    nValidTrackerHits2 = df.Muon_Numberofvalidtrackerhits.iloc[0][mu[1]]
    nValidPixelHits2 = df.Muon_Numberofvalidpixelhits.iloc[0][mu[1]]
    outerTrk_P_2 = df.Muon_outerTrack_p.iloc[0][mu[1]]
    outerTrk_Eta_2 = df.Muon_outerTrack_eta.iloc[0][mu[1]]
    outerTrk_normChi2_2 = df.Muon_outerTrack_normalizedChi2.iloc[0][mu[1]]
    outerTrk_muStValidHits_2 = df.Muon_outerTrack_muonStationsWithValidHits.iloc[0][mu[1]]
    innerTrk_P_2 = df.Muon_innerTrack_p.iloc[0][mu[1]]
    innerTrk_Eta_2 = df.Muon_innerTrack_eta.iloc[0][mu[1]]
    innerTrk_normChi2_2 = df.Muon_innerTrack_normalizedChi2.iloc[0][mu[1]]
    innerTrk_highPurity_2 = df.Muon_innerTrack_highPurity.iloc[0][mu[1]]
    innerTrk_ValidFraction_2 = df.Muon_innerTrack_ValidFraction.iloc[0][mu[1]]
    QInnerOuter_2 = df.Muon_QInnerOuter.iloc[0][mu[1]]
    cQ_uS_2 = df.Muon_combinedQuality_updatedSta.iloc[0][mu[1]]
    cQ_tK_2 = df.Muon_combinedQuality_trkKink.iloc[0][mu[1]]
    cQ_gK_2 = df.Muon_combinedQuality_glbKink.iloc[0][mu[1]]
    cQ_tRChi2_2 = df.Muon_combinedQuality_trkRelChi2.iloc[0][mu[1]]
    cQ_sRChi2_2 = df.Muon_combinedQuality_staRelChi2.iloc[0][mu[1]]
    cQ_Chi2LP_2 = df.Muon_combinedQuality_chi2LocalPosition.iloc[0][mu[1]]
    cQ_Chi2LM_2 = df.Muon_combinedQuality_chi2LocalMomentum.iloc[0][mu[1]]
    cQ_lD_2 = df.Muon_combinedQuality_localDistance.iloc[0][mu[1]]
    cQ_gDEP_2 = df.Muon_combinedQuality_globalDeltaEtaPhi.iloc[0][mu[1]]
    cQ_tM_2 = df.Muon_combinedQuality_tightMatch.iloc[0][mu[1]]
    cQ_gTP_2 = df.Muon_combinedQuality_glbTrackProbability.iloc[0][mu[1]]
    segmComp_2 = df.Muon_segmentCompatibility.iloc[0][mu[1]]
    caloComp_2 = df.Muon_caloCompatibility.iloc[0][mu[1]]
    match1_dX_2 = df.Muon_combinedQuality_match1_dX.iloc[0][mu[1]]
    match1_pullX_2 = df.Muon_combinedQuality_match1_pullX.iloc[0][mu[1]]
    match1_pullDxDz_2 = df.Muon_combinedQuality_match1_pullDxDz.iloc[0][mu[1]]
    match1_dY_2 = df.Muon_combinedQuality_match1_dY.iloc[0][mu[1]]
    match1_pullY_2 = df.Muon_combinedQuality_match1_pullY.iloc[0][mu[1]]
    match1_pullDyDz_2 = df.Muon_combinedQuality_match1_pullDyDz.iloc[0][mu[1]]
    match2_dX_2 = df.Muon_combinedQuality_match2_dX.iloc[0][mu[1]]
    match2_pullX_2 = df.Muon_combinedQuality_match2_pullX.iloc[0][mu[1]]
    match2_pullDxDz_2 = df.Muon_combinedQuality_match2_pullDxDz.iloc[0][mu[1]]
    match2_dY_2 = df.Muon_combinedQuality_match2_dY.iloc[0][mu[1]]
    match2_pullY_2 = df.Muon_combinedQuality_match2_pullY.iloc[0][mu[1]]
    match2_pullDyDz_2 = df.Muon_combinedQuality_match2_pullDyDz.iloc[0][mu[1]]
    if(debugMode): print("Ciao12")
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
    if(debugMode): print("Ciao13")
    df_fin.at[jentry, "isMC"] = (isMC)
    df_fin.at[jentry, "lumi"] = (lumi)
    df_fin.at[jentry, "run"] = (run)
    df_fin.at[jentry, "evt"] = (evt)
    df_fin.at[jentry, "puFactor"] = (puFactor)
    df_fin.at[jentry, "L1_DoubleMu0_er1p5"] = (L1_DoubleMu0_er1p5)
    df_fin.at[jentry, "L1_DoubleMu0_er1p4"] = (L1_DoubleMu0_er1p4)
    df_fin.at[jentry, "L1_DoubleMu4_dR1p2"] = (L1_DoubleMu4_dR1p2)
    df_fin.at[jentry, "L1_DoubleMu4p5_dR1p2"] = (L1_DoubleMu4p5_dR1p2)
    df_fin.at[jentry, "L1_DoubleMu0_er2p0"] = (L1_DoubleMu0_er2p0)
    df_fin.at[jentry, "L1_DoubleMu0_er2p0_bk"] = (L1_DoubleMu0_er2p0_bk)
    df_fin.at[jentry, "L1seed"] = (L1seed)
    df_fin.at[jentry, "HLTpath"] = (HLTpath)
    df_fin.at[jentry, "DeltaR_max"] = (DeltaR_max)
    df_fin.at[jentry, "DeltaZ_max"] = (DeltaZ_max)
    df_fin.at[jentry, "Pmu3"] = (Pmu3)
    df_fin.at[jentry, "cLP"] = (cLP)
    df_fin.at[jentry, "tKink"] = (tKink)
    df_fin.at[jentry, "segmComp"] = (segmComp)
    df_fin.at[jentry, "tripletMass"] = (tripletMass)
    df_fin.at[jentry, "tripletMassReso"] = (tripletMassReso)
    df_fin.at[jentry, "fv_nC"] = (fv_nC)
    df_fin.at[jentry, "fv_dphi3D"] = (fv_dphi3D)
    df_fin.at[jentry, "fv_d3D"] = (fv_d3D)
    df_fin.at[jentry, "fv_d3Dsig"] = (fv_d3Dsig)
    df_fin.at[jentry, "d0"] = (d0)
    df_fin.at[jentry, "nVtx"] = (nVtx)
    df_fin.at[jentry, "d0sig"] = (d0sig)
    df_fin.at[jentry, "MVA1"] = (MVA1)
    df_fin.at[jentry, "MVA2"] = (MVA2)
    df_fin.at[jentry, "MVA3"] = (MVA3)
    df_fin.at[jentry, "MVASoft1"] = (MVASoft1)
    df_fin.at[jentry, "MVASoft2"] = (MVASoft2)
    df_fin.at[jentry, "MVASoft3"] = (MVASoft3)
    df_fin.at[jentry, "d0sig_max"] = (d0sig_max)
    df_fin.at[jentry, "mindca_iso"] = (mindca_iso)
    df_fin.at[jentry, "trkRel"] = (trkRel)
    df_fin.at[jentry, "Pmu1"] = (Pmu1)
    df_fin.at[jentry, "Ptmu1"] = (Ptmu1)
    df_fin.at[jentry, "Etamu1"] = (etamu1)
    df_fin.at[jentry, "Phimu1"] = (phimu1)
    df_fin.at[jentry, "Pmu2"] = (Pmu2)
    df_fin.at[jentry, "Ptmu2"] = (Ptmu2)
    df_fin.at[jentry, "Etamu2"] = (etamu2)
    df_fin.at[jentry, "Phimu2"] = (phimu2)
    df_fin.at[jentry, "Ptmu3"] = (Ptmu3)
    df_fin.at[jentry, "Etamu3"] = (etamu3)
    df_fin.at[jentry, "Phimu3"] = (phimu3)
    df_fin.at[jentry, "dispMu1"] = (dispMu1)
    df_fin.at[jentry, "dispMu2"] = (dispMu2)
    df_fin.at[jentry, "dispMu3"] = (dispMu3)
    df_fin.at[jentry, "xydispMu1"] = (xydispMu1)
    df_fin.at[jentry, "xydispMu2"] = (xydispMu2)
    df_fin.at[jentry, "xydispMu3"] = (xydispMu3)
    df_fin.at[jentry, "P_tripl"] = (P_trip)
    df_fin.at[jentry, "Pt_tripl"] = (Pt_trip)
    df_fin.at[jentry, "Eta_tripl"] = (eta_trip)
    df_fin.at[jentry, "nStMu1"] = (nStationsMu1)
    df_fin.at[jentry, "nStMu2"] = (nStationsMu2)
    df_fin.at[jentry, "nStMu3"] = (nStationsMu3)
    df_fin.at[jentry, "Iso03Mu1"] = (Iso03Mu1)
    df_fin.at[jentry, "Iso03Mu2"] = (Iso03Mu2)
    df_fin.at[jentry, "Iso03Mu3"] = (Iso03Mu3)
    df_fin.at[jentry, "Iso05Mu1"] = (Iso05Mu1)
    df_fin.at[jentry, "Iso05Mu2"] = (Iso05Mu2)
    df_fin.at[jentry, "Iso05Mu3"] = (Iso05Mu3)
    df_fin.at[jentry, "nMatchesMu1"] = (nMatchesMu1)
    df_fin.at[jentry, "nMatchesMu2"] = (nMatchesMu2)
    df_fin.at[jentry, "nMatchesMu3"] = (nMatchesMu3)
    df_fin.at[jentry, "timeAtIpInOut_sig1"] = (timeAtIpInOut_sig1)
    df_fin.at[jentry, "timeAtIpInOut_sig2"] = (timeAtIpInOut_sig2)
    df_fin.at[jentry, "timeAtIpInOut_sig3"] = (timeAtIpInOut_sig3)
    df_fin.at[jentry, "cQ_uS"] = (cQ_uS)
    df_fin.at[jentry, "cQ_tK"] = (cQ_tK)
    df_fin.at[jentry, "cQ_gK"] = (cQ_gK)
    df_fin.at[jentry, "cQ_tRChi2"] = (cQ_tRChi2)
    df_fin.at[jentry, "cQ_sRChi2"] = (cQ_sRChi2)
    df_fin.at[jentry, "cQ_Chi2LP"] = (cQ_Chi2LP)
    df_fin.at[jentry, "cQ_Chi2LM"] = (cQ_Chi2LM)
    df_fin.at[jentry, "cQ_lD"] = (cQ_lD)
    df_fin.at[jentry, "cQ_gDEP"] = (cQ_gDEP)
    df_fin.at[jentry, "cQ_tM"] = (cQ_tM)
    df_fin.at[jentry, "cQ_gTP"] = (cQ_gTP)
    df_fin.at[jentry, "calEn_emMu1"] = (calEn_emMu1)
    df_fin.at[jentry, "calEn_emMu2"] = (calEn_emMu2)
    df_fin.at[jentry, "calEn_emMu3"] = (calEn_emMu3)
    df_fin.at[jentry, "calEn_hadMu1"] = (calEn_hadMu1)
    df_fin.at[jentry, "calEn_hadMu2"] = (calEn_hadMu2)
    df_fin.at[jentry, "calEn_hadMu3"] = (calEn_hadMu3)
    df_fin.at[jentry, "caloComp"] = (caloComp)
    df_fin.at[jentry, "fliDistPVSV_Chi2"] = (fliDistPVSV_Chi2)
    df_fin.at[jentry, "isGlb1"] = (isGlb1)
    df_fin.at[jentry, "isMedium1"] = (isMedium1)
    df_fin.at[jentry, "isMedium2"] = (isMedium2)
    df_fin.at[jentry, "isTracker1"] = (isTracker1)
    df_fin.at[jentry, "isLoose1"] = (isLoose1)
    df_fin.at[jentry, "isSoft1"] = (isSoft1)
    df_fin.at[jentry, "isPF1"] = (isPF1)
    df_fin.at[jentry, "isRPC1"] = (isRPC1)
    df_fin.at[jentry, "isSA1"] = (isSA1)
    df_fin.at[jentry, "isCalo1"] = (isCalo1)
    df_fin.at[jentry, "isGlb2"] = (isGlb2)
    df_fin.at[jentry, "isTracker2"] = (isTracker2)
    df_fin.at[jentry, "isLoose2"] = (isLoose2)
    df_fin.at[jentry, "isSoft2"] = (isSoft2)
    df_fin.at[jentry, "isPF2"] = (isPF2)
    df_fin.at[jentry, "isRPC2"] = (isRPC2)
    df_fin.at[jentry, "isSA2"] = (isSA2)
    df_fin.at[jentry, "isCalo2"] = (isCalo2)
    df_fin.at[jentry, "isGlb3"] = (isGlb3)
    df_fin.at[jentry, "isTracker3"] = (isTracker3)
    df_fin.at[jentry, "isLoose3"] = (isLoose3)
    df_fin.at[jentry, "isSoft3"] = (isSoft3)
    df_fin.at[jentry, "isPF3"] = (isPF3)
    df_fin.at[jentry, "isRPC3"] = (isRPC3)
    df_fin.at[jentry, "isSA3"] = (isSA3)
    df_fin.at[jentry, "isCalo3"] = (isCalo3)
    df_fin.at[jentry, "Vx1"] = (Vx1)
    df_fin.at[jentry, "Vx2"] = (Vx2)
    df_fin.at[jentry, "Vx3"] = (Vx3)
    df_fin.at[jentry, "Vy1"] = (Vy1)
    df_fin.at[jentry, "Vy2"] = (Vy2)
    df_fin.at[jentry, "Vy3"] = (Vy3)
    df_fin.at[jentry, "Vz1"] = (Vz1)
    df_fin.at[jentry, "Vz2"] = (Vz2)
    df_fin.at[jentry, "Vz3"] = (Vz3)
    df_fin.at[jentry, "RefVx1"] = (RefVx1)
    df_fin.at[jentry, "RefVx2"] = (RefVx2)
    df_fin.at[jentry, "RefVx3"] = (RefVx3)
    df_fin.at[jentry, "RefVy1"] = (RefVy1)
    df_fin.at[jentry, "RefVy2"] = (RefVy2)
    df_fin.at[jentry, "RefVy3"] = (RefVy3)
    df_fin.at[jentry, "RefVz1"] = (RefVz1)
    df_fin.at[jentry, "RefVz2"] = (RefVz2)
    df_fin.at[jentry, "RefVz3"] = (RefVz3)
    df_fin.at[jentry, "SVx"] = (SVx)
    df_fin.at[jentry, "SVy"] = (SVy)
    df_fin.at[jentry, "SVz"] = (SVz)
    df_fin.at[jentry, "had03"] = (had03)
    df_fin.at[jentry, "had05"] = (had05)
    df_fin.at[jentry, "nJets03"] = (nJets03)
    df_fin.at[jentry, "nJets05"] = (nJets05)
    df_fin.at[jentry, "nTracks03"] = (nTracks03)
    df_fin.at[jentry, "nTracks05"] = (nTracks05)
    df_fin.at[jentry, "sumPt03"] = (sumPt03)
    df_fin.at[jentry, "sumPt05"] = (sumPt05)
    df_fin.at[jentry, "hadVeto03"] = (hadVeto03)
    df_fin.at[jentry, "hadVeto05"] = (hadVeto05)
    df_fin.at[jentry, "emVeto03"] = (emVeto03)
    df_fin.at[jentry, "emVeto05"] = (emVeto05)
    df_fin.at[jentry, "trVeto03"] = (trVeto03)
    df_fin.at[jentry, "trVeto05"] = (trVeto05)
    #)new)branches)
    df_fin.at[jentry, "EnMu1"] = (EnMu1)
    df_fin.at[jentry, "EnMu2"] = (EnMu2)
    df_fin.at[jentry, "EnMu3"] = (EnMu3)
    df_fin.at[jentry, "ChargeMu1"] = (ChargeMu1)
    df_fin.at[jentry, "ChargeMu2"] = (ChargeMu2)
    df_fin.at[jentry, "ChargeMu3"] = (ChargeMu3)
    #)Mu1)
    df_fin.at[jentry, "isQValid1"] = (isQValid1)
    df_fin.at[jentry, "isTValid1"] = (isTValid1)
    df_fin.at[jentry, "isIsoValid1"] = (isIsoValid1)
    df_fin.at[jentry, "GLnormChi2_mu1"] = (GLnormChi2_mu1)
    df_fin.at[jentry, "GL_nValidMuHits1"] = (GL_nValidMuHits1)
    df_fin.at[jentry, "trkLayersWMeas1"] = (trkLayersWMeas1)
    df_fin.at[jentry, "validMuonHitComb1"] = (validMuonHitComb1)
    df_fin.at[jentry, "nValidTrackerHits1"] = (nValidTrackerHits1)
    df_fin.at[jentry, "nValidPixelHits1"] = (nValidPixelHits1)
    df_fin.at[jentry, "outerTrk_P_1"] = (outerTrk_P_1)
    df_fin.at[jentry, "outerTrk_Eta_1"] = (outerTrk_Eta_1)
    df_fin.at[jentry, "outerTrk_normChi2_1"] = (outerTrk_normChi2_1)
    df_fin.at[jentry, "outerTrk_muStValidHits_1"] = (outerTrk_muStValidHits_1)
    df_fin.at[jentry, "innerTrk_P_1"] = (innerTrk_P_1)
    df_fin.at[jentry, "innerTrk_Eta_1"] = (innerTrk_Eta_1)
    df_fin.at[jentry, "innerTrk_normChi2_1"] = (innerTrk_normChi2_1)
    df_fin.at[jentry, "innerTrk_highPurity_1"] = (innerTrk_highPurity_1)
    df_fin.at[jentry, "innerTrk_ValidFraction_1"] = (innerTrk_ValidFraction_1)
    df_fin.at[jentry, "QInnerOuter_1"] = (QInnerOuter_1)
    df_fin.at[jentry, "cQ_uS_1"] = (cQ_uS_1)
    df_fin.at[jentry, "cQ_tK_1"] = (cQ_tK_1)
    df_fin.at[jentry, "cQ_gK_1"] = (cQ_gK_1)
    df_fin.at[jentry, "cQ_tRChi2_1"] = (cQ_tRChi2_1)
    df_fin.at[jentry, "cQ_sRChi2_1"] = (cQ_sRChi2_1)
    df_fin.at[jentry, "cQ_Chi2LP_1"] = (cQ_Chi2LP_1)
    df_fin.at[jentry, "cQ_Chi2LM_1"] = (cQ_Chi2LM_1)
    df_fin.at[jentry, "cQ_lD_1"] = (cQ_lD_1)
    df_fin.at[jentry, "cQ_gDEP_1"] = (cQ_gDEP_1)
    df_fin.at[jentry, "cQ_tM_1"] = (cQ_tM_1)
    df_fin.at[jentry, "cQ_gTP_1"] = (cQ_gTP_1)
    df_fin.at[jentry, "segmComp_1"] = (segmComp_1)
    df_fin.at[jentry, "caloComp_1"] = (caloComp_1)
    df_fin.at[jentry, "match1_dX_1"] = (match1_dX_1)
    df_fin.at[jentry, "match1_pullX_1"] = (match1_pullX_1)
    df_fin.at[jentry, "match1_pullDxDz_1"] = (match1_pullDxDz_1)
    df_fin.at[jentry, "match1_dY_1"] = (match1_dY_1)
    df_fin.at[jentry, "match1_pullY_1"] = (match1_pullY_1)
    df_fin.at[jentry, "match1_pullDyDz_1"] = (match1_pullDyDz_1)
    df_fin.at[jentry, "match2_dX_1"] = (match2_dX_1)
    df_fin.at[jentry, "match2_pullX_1"] = (match2_pullX_1)
    df_fin.at[jentry, "match2_pullDxDz_1"] = (match2_pullDxDz_1)
    df_fin.at[jentry, "match2_dY_1"] = (match2_dY_1)
    df_fin.at[jentry, "match2_pullY_1"] = (match2_pullY_1)
    df_fin.at[jentry, "match2_pullDyDz_1"] = (match2_pullDyDz_1)
    #)Mu2)
    df_fin.at[jentry, "isQValid2"] = (isQValid2)
    df_fin.at[jentry, "isTValid2"] = (isTValid2)
    df_fin.at[jentry, "isIsoValid2"] = (isIsoValid2)
    df_fin.at[jentry, "GLnormChi2_mu2"] = (GLnormChi2_mu2)
    df_fin.at[jentry, "GL_nValidMuHits2"] = (GL_nValidMuHits2)
    df_fin.at[jentry, "trkLayersWMeas2"] = (trkLayersWMeas2)
    df_fin.at[jentry, "validMuonHitComb2"] = (validMuonHitComb2)
    df_fin.at[jentry, "nValidTrackerHits2"] = (nValidTrackerHits2)
    df_fin.at[jentry, "nValidPixelHits2"] = (nValidPixelHits2)
    df_fin.at[jentry, "outerTrk_P_2"] = (outerTrk_P_2)
    df_fin.at[jentry, "outerTrk_Eta_2"] = (outerTrk_Eta_2)
    df_fin.at[jentry, "outerTrk_normChi2_2"] = (outerTrk_normChi2_2)
    df_fin.at[jentry, "outerTrk_muStValidHits_2"] = (outerTrk_muStValidHits_2)
    df_fin.at[jentry, "innerTrk_P_2"] = (innerTrk_P_2)
    df_fin.at[jentry, "innerTrk_Eta_2"] = (innerTrk_Eta_2)
    df_fin.at[jentry, "innerTrk_normChi2_2"] = (innerTrk_normChi2_2)
    df_fin.at[jentry, "innerTrk_highPurity_2"] = (innerTrk_highPurity_2)
    df_fin.at[jentry, "innerTrk_ValidFraction_2"] = (innerTrk_ValidFraction_2)
    df_fin.at[jentry, "QInnerOuter_2"] = (QInnerOuter_2)
    df_fin.at[jentry, "cQ_uS_2"] = (cQ_uS_2)
    df_fin.at[jentry, "cQ_tK_2"] = (cQ_tK_2)
    df_fin.at[jentry, "cQ_gK_2"] = (cQ_gK_2)
    df_fin.at[jentry, "cQ_tRChi2_2"] = (cQ_tRChi2_2)
    df_fin.at[jentry, "cQ_sRChi2_2"] = (cQ_sRChi2_2)
    df_fin.at[jentry, "cQ_Chi2LP_2"] = (cQ_Chi2LP_2)
    df_fin.at[jentry, "cQ_Chi2LM_2"] = (cQ_Chi2LM_2)
    df_fin.at[jentry, "cQ_lD_2"] = (cQ_lD_2)
    df_fin.at[jentry, "cQ_gDEP_2"] = (cQ_gDEP_2)
    df_fin.at[jentry, "cQ_tM_2"] = (cQ_tM_2)
    df_fin.at[jentry, "cQ_gTP_2"] = (cQ_gTP_2)
    df_fin.at[jentry, "segmComp_2"] = (segmComp_2)
    df_fin.at[jentry, "caloComp_2"] = (caloComp_2)
    df_fin.at[jentry, "match1_dX_2"] = (match1_dX_2)
    df_fin.at[jentry, "match1_pullX_2"] = (match1_pullX_2)
    df_fin.at[jentry, "match1_pullDxDz_2"] = (match1_pullDxDz_2)
    df_fin.at[jentry, "match1_dY_2"] = (match1_dY_2)
    df_fin.at[jentry, "match1_pullY_2"] = (match1_pullY_2)
    df_fin.at[jentry, "match1_pullDyDz_2"] = (match1_pullDyDz_2)
    df_fin.at[jentry, "match2_dX_2"] = (match2_dX_2)
    df_fin.at[jentry, "match2_pullX_2"] = (match2_pullX_2)
    df_fin.at[jentry, "match2_pullDxDz_2"] = (match2_pullDxDz_2)
    df_fin.at[jentry, "match2_dY_2"] = (match2_dY_2)
    df_fin.at[jentry, "match2_pullY_2"] = (match2_pullY_2)
    df_fin.at[jentry, "match2_pullDyDz_2"] = (match2_pullDyDz_2)
    #)Mu3)
    df_fin.at[jentry, "isQValid3"] = (isQValid3)
    df_fin.at[jentry, "isTValid3"] = (isTValid3)
    df_fin.at[jentry, "isIsoValid3"] = (isIsoValid3)
    df_fin.at[jentry, "GLnormChi2_mu3"] = (GLnormChi2_mu3)
    df_fin.at[jentry, "GL_nValidMuHits3"] = (GL_nValidMuHits3)
    df_fin.at[jentry, "trkLayersWMeas3"] = (trkLayersWMeas3)
    df_fin.at[jentry, "validMuonHitComb3"] = (validMuonHitComb3)
    df_fin.at[jentry, "nValidTrackerHits3"] = (nValidTrackerHits3)
    df_fin.at[jentry, "nValidPixelHits3"] = (nValidPixelHits3)
    df_fin.at[jentry, "outerTrk_P_3"] = (outerTrk_P_3)
    df_fin.at[jentry, "outerTrk_Eta_3"] = (outerTrk_Eta_3)
    df_fin.at[jentry, "outerTrk_normChi2_3"] = (outerTrk_normChi2_3)
    df_fin.at[jentry, "outerTrk_muStValidHits_3"] = (outerTrk_muStValidHits_3)
    df_fin.at[jentry, "innerTrk_P_3"] = (innerTrk_P_3)
    df_fin.at[jentry, "innerTrk_Eta_3"] = (innerTrk_Eta_3)
    df_fin.at[jentry, "innerTrk_normChi2_3"] = (innerTrk_normChi2_3)
    df_fin.at[jentry, "innerTrk_highPurity_3"] = (innerTrk_highPurity_3)
    df_fin.at[jentry, "innerTrk_ValidFraction_3"] = (innerTrk_ValidFraction_3)
    df_fin.at[jentry, "QInnerOuter_3"] = (QInnerOuter_3)
    df_fin.at[jentry, "cQ_uS_3"] = (cQ_uS_3)
    df_fin.at[jentry, "cQ_tK_3"] = (cQ_tK_3)
    df_fin.at[jentry, "cQ_gK_3"] = (cQ_gK_3)
    df_fin.at[jentry, "cQ_tRChi2_3"] = (cQ_tRChi2_3)
    df_fin.at[jentry, "cQ_sRChi2_3"] = (cQ_sRChi2_3)
    df_fin.at[jentry, "cQ_Chi2LP_3"] = (cQ_Chi2LP_3)
    df_fin.at[jentry, "cQ_Chi2LM_3"] = (cQ_Chi2LM_3)
    df_fin.at[jentry, "cQ_lD_3"] = (cQ_lD_3)
    df_fin.at[jentry, "cQ_gDEP_3"] = (cQ_gDEP_3)
    df_fin.at[jentry, "cQ_tM_3"] = (cQ_tM_3)
    df_fin.at[jentry, "cQ_gTP_3"] = (cQ_gTP_3)
    df_fin.at[jentry, "segmComp_3"] = (segmComp_3)
    df_fin.at[jentry, "caloComp_3"] = (caloComp_3)
    df_fin.at[jentry, "match1_dX_3"] = (match1_dX_3)
    df_fin.at[jentry, "match1_pullX_3"] = (match1_pullX_3)
    df_fin.at[jentry, "match1_pullDxDz_3"] = (match1_pullDxDz_3)
    df_fin.at[jentry, "match1_dY_3"] = (match1_dY_3)
    df_fin.at[jentry, "match1_pullY_3"] = (match1_pullY_3)
    df_fin.at[jentry, "match1_pullDyDz_3"] = (match1_pullDyDz_3)
    df_fin.at[jentry, "match2_dX_3"] = (match2_dX_3)
    df_fin.at[jentry, "match2_pullX_3"] = (match2_pullX_3)
    df_fin.at[jentry, "match2_pullDxDz_3"] = (match2_pullDxDz_3)
    df_fin.at[jentry, "match2_dY_3"] = (match2_dY_3)
    df_fin.at[jentry, "match2_pullY_3"] = (match2_pullY_3)
    df_fin.at[jentry, "match2_pullDyDz_3"] = (match2_pullDyDz_3)

def loop_events(sub_df, debugMode, cutevt, df_fin, isMC):
    jentry = sub_df.index[0]
    ientry = sub_df
    print(ientry)
    #if (ientry < 0): break
    #ientry.fChain.GetTree().GetEntry(ientry)
    # if (Cut(ientry) < 0) continue;
    L1seed = -99
    HLTpath = -99
    L1_DoubleMu0_er1p5 = 0
    L1_DoubleMu0_er1p4 = 0
    L1_DoubleMu4_dR1p2 = 0
    L1_DoubleMu4p5_dR1p2 = 0
    L1_DoubleMu0_er2p0 = 0
    L1_DoubleMu0_er2p0_bk = 0
    run_n = 0
    lumi_n = 0
    evt_n = 0
    L1 = 0
    nHLT = 0
    deltaR_max = 0
    deltaZ_max = 0
    Pmu3 = 0
    cLP = 0
    tKink = 0
    segmComp = 0
    tripletMass = 0
    tripletMassReso = 0
    fv_nC = 0
    fv_dphi3D = 0
    fv_d3D = 0
    fv_d3Dsig = 0
    d0 = 0
    nVtx=0
    d0sig = 0
    MVA1 = 0
    pileupFactor = 0; MVA2 = 0; MVA3 = 0; MVASoft1 = 0; MVASoft2 = 0; MVASoft3 = 0; d0sig_max = 0; mindca_iso = 0; trkRel = 0; Pmu1 = 0; Ptmu1 = 0; etamu1 = 0; phimu1 = 0; Pmu2 = 0; Ptmu2 = 0; etamu2 = 0; phimu2 = 0; Ptmu3 = 0; etamu3 = 0; phimu3 = 0; dispMu1 = 0; dispMu2 = 0; dispMu3 = 0; xydispMu1 = 0; xydispMu2 = 0; xydispMu3 = 0; P_trip = 0; Pt_trip = 0; eta_trip = 0; nStationsMu1 = 0; nStationsMu2 = 0; nStationsMu3 = 0; Iso03Mu1 = 0; Iso03Mu2 = 0; Iso03Mu3 = 0; Iso05Mu1 = 0; Iso05Mu2 = 0; Iso05Mu3 = 0; nMatchesMu1 = 0; nMatchesMu2 = 0; nMatchesMu3 = 0; timeAtIpInOutMu_sig1 = 0; timeAtIpInOutMu_sig2 = 0; timeAtIpInOutMu_sig3 = 0; cQ_uS = 0; cQ_tK = 0; cQ_gK = 0; cQ_tRChi2 = 0; cQ_sRChi2 = 0; cQ_Chi2LP = 0; cQ_Chi2LM = 0; cQ_lD = 0; cQ_gDEP = 0; cQ_tM = 0; cQ_gTP = 0; calEn_emMu1 = 0; calEn_emMu2 = 0; calEn_emMu3 = 0; calEn_hadMu1 = 0; calEn_hadMu2 = 0; calEn_hadMu3 = 0; caloComp = 0; fliDistPVSV_Chi2 = 0; isGlb1 = 0; isMedium1 = 0; isTracker1 = 0; isLoose1 = 0; isSoft1 = 0; SoftMVA1 = 0; isPF1 = 0; isRPC1 = 0; isSA1 = 0; isCalo1 = 0; isGlb2 = 0; isMedium2 = 0; isTracker2 = 0; isLoose2 = 0; isSoft2 = 0; SoftMVA2 = 0; isPF2 = 0; isRPC2 = 0; isSA2 = 0; isCalo2 = 0; isGlb3 = 0; isMedium3 = 0; isTracker3 = 0; isLoose3 = 0; isSoft3 = 0; SoftMVA3 = 0; isPF3 = 0; isRPC3 = 0; isSA3 = 0; isCalo3 = 0; vx1 = 0; vx2 = 0; vx3 = 0; vy1 = 0; vy2 = 0; vy3 = 0; vz1 = 0; vz2 = 0; vz3 = 0; Refvx1 = 0; Refvx2 = 0; Refvx3 = 0; Refvy1 = 0; Refvy2 = 0; Refvy3 = 0; Refvz1 = 0; Refvz2 = 0; Refvz3 = 0; SVx = 0; SVy = 0; SVz = 0; had03 = 0; had05 = 0; nJets03 = 0; nJets05 = 0; nTracks03 = 0; nTracks05 = 0; sumPt03 = 0; sumPt05 = 0; hadVeto03 = 0; hadVeto05 = 0; emVeto03 = 0; emVeto05 = 0; trVeto03 = 0; trVeto05 = 0; EnMu1 = 0; EnMu2 = 0; EnMu3 = 0; ChargeMu1 = 0; ChargeMu2 = 0; ChargeMu3 = 0; isQValid1 = 0; isTValid1 = 0; isIsoValid1 = 0; GLnormChi2_mu1 = 0; GL_nValidMuHits1 = 0; trkLayersWMeas1 = 0; nValidPixelHits1 = 0; outerTrk_P_1 = 0; outerTrk_Eta_1 = 0; outerTrk_normChi2_1 = 0; outerTrk_muStValidHits_1 = 0; innerTrk_P_1 = 0; innerTrk_Eta_1 = 0; innerTrk_normChi2_1 = 0; QInnerOuter_1 = 0; cQ_uS_1 = 0; cQ_tK_1 = 0; cQ_gK_1 = 0; cQ_tRChi2_1 = 0; cQ_sRChi2_1 = 0; cQ_Chi2LP_1 = 0; cQ_Chi2LM_1 = 0; cQ_lD_1 = 0; cQ_gDEP_1 = 0; cQ_tM_1 = 0; cQ_gTP_1 = 0; segmComp_1 = 0; caloComp_1 = 0; isQValid2 = 0; isTValid2 = 0; isIsoValid2 = 0; GLnormChi2_mu2 = 0; GL_nValidMuHits2 = 0; trkLayersWMeas2 = 0; nValidPixelHits2 = 0; outerTrk_P_2 = 0; outerTrk_Eta_2 = 0; outerTrk_normChi2_2 = 0; outerTrk_muStValidHits_2 = 0; innerTrk_P_2 = 0; innerTrk_Eta_2 = 0; innerTrk_normChi2_2 = 0; QInnerOuter_2 = 0; cQ_uS_2 = 0; cQ_tK_2 = 0; cQ_gK_2 = 0; cQ_tRChi2_2 = 0; cQ_sRChi2_2 = 0; cQ_Chi2LP_2 = 0; cQ_Chi2LM_2 = 0; cQ_lD_2 = 0; cQ_gDEP_2 = 0; cQ_tM_2 = 0; cQ_gTP_2 = 0; segmComp_2 = 0; caloComp_2 = 0; isQValid3 = 0; isTValid3 = 0; isIsoValid3 = 0; GLnormChi2_mu3 = 0; GL_nValidMuHits3 = 0; trkLayersWMeas3 = 0; nValidPixelHits3 = 0; outerTrk_P_3 = 0; outerTrk_Eta_3 = 0; outerTrk_normChi2_3 = 0; outerTrk_muStValidHits_3 = 0; innerTrk_P_3 = 0; innerTrk_Eta_3 = 0; innerTrk_normChi2_3 = 0; QInnerOuter_3 = 0; cQ_uS_3 = 0; cQ_tK_3 = 0; cQ_gK_3 = 0; cQ_tRChi2_3 = 0; cQ_sRChi2_3 = 0; cQ_Chi2LP_3 = 0; cQ_Chi2LM_3 = 0; cQ_lD_3 = 0; cQ_gDEP_3 = 0; cQ_tM_3 = 0; cQ_gTP_3 = 0; segmComp_3 = 0; caloComp_3 = 0; inTrk_highPurity_1 = 0; inTrk_ValidFraction_1 = 0; NvalidTrkHits_1 = 0; validMuHitComb_1 = 0; IP2D_BS_1 = 0; IP3D_BS_1 = 0; IP2D_PV_1 = 0; IP3D_PV_1 = 0; inTrk_highPurity_2 = 0; inTrk_ValidFraction_2 = 0; NvalidTrkHits_2 = 0; validMuHitComb_2 = 0; IP2D_BS_2 = 0; IP3D_BS_2 = 0; IP2D_PV_2 = 0; IP3D_PV_2 = 0; inTrk_highPurity_3 = 0; inTrk_ValidFraction_3 = 0; NvalidTrkHits_3 = 0; validMuHitComb_3 = 0; IP2D_BS_3 = 0; IP3D_BS_3 = 0; IP2D_PV_3 = 0; IP3D_PV_3 = 0; inTrk_highPurity_max = 0; inTrk_ValidFraction_max = 0; NvalidTrkHits_max = 0; validMuHitComb_max = 0; IP2D_BS_max = 0; IP3D_BS_max = 0; IP2D_PV_max = 0; IP3D_PV_max = 0; inTrk_highPurity_min = 0; inTrk_ValidFraction_min = 0; NvalidTrkHits_min = 0; validMuHitComb_min = 0; IP2D_BS_min = 0; IP3D_BS_min = 0; IP2D_PV_min = 0; IP3D_PV_min = 0; tripl_IsoMu1 = 0; tripl_IsoMu2 = 0; tripl_IsoMu3 = 0; DistXYPVSV = 0; DistXY_PVSV_sig = 0; FlightDistBSSV = 0; FlightDistBS_SV_sig = 0; diMu12_mass = 0; diMu23_mass = 0; diMu13_mass = 0; cTau = 0; cTau2 = 0; NMu_TrMatch = 0; IP1 = 0; IP2 = 0; IP3 = 0; IP1_sig = 0; IP2_sig = 0; IP3_sig = 0; muSimPdgId_1 = 0; muSimMotherPdgId_1 = 0; muSimPdgId_2 = 0; muSimMotherPdgId_2 = 0; muSimPdgId_3 = 0; muSimMotherPdgId_3 = 0; NTrk_RefittedPV = 0; RefittedPV_Chi2norm = 0; diMuVtx_dist_max = 0; diMuVtx_dist_min = 0; Chi2IP_max = 0;
        
    match1_dX_1=0; match1_pullX_1=0; match1_pullDxDz_1=0; match1_dY_1=0; match1_pullY_1=0; match1_pullDyDz_1=0; 
    match1_dX_2=0; match1_pullX_2=0; match1_pullDxDz_2=0; match1_dY_2=0; match1_pullY_2=0; match1_pullDyDz_2=0; 
    match1_dX_3=0; match1_pullX_3=0; match1_pullDxDz_3=0; match1_dY_3=0; match1_pullY_3=0; match1_pullDyDz_3=0; 
    match2_dX_1=0; match2_pullX_1=0; match2_pullDxDz_1=0; match2_dY_1=0; match2_pullY_1=0; match2_pullDyDz_1=0; 
    match2_dX_2=0; match2_pullX_2=0; match2_pullDxDz_2=0; match2_dY_2=0; match2_pullY_2=0; match2_pullDyDz_2=0; 
    match2_dX_3=0; match2_pullX_3=0; match2_pullDxDz_3=0; match2_dY_3=0; match2_pullY_3=0; match2_pullDyDz_3=0
        
    validMuonHitComb1=0
    validMuonHitComb2=0
    validMuonHitComb3=0
    nValidTrackerHits1=0
    nValidTrackerHits2=0
    nValidTrackerHits3=0

    innerTrk_ValidFraction_1=0
    innerTrk_ValidFraction_2=0
    innerTrk_ValidFraction_3=0
    innerTrk_highPurity_1=0
    innerTrk_highPurity_2=0
    innerTrk_highPurity_3=0


    if (debugMode): print(f"\n++++Event n. {jentry}\n")
    triplEff_counter = []
    for i in range(NCUTS):
        triplEff_counter.append(False)
    run_n = ientry.run.iloc[0]
    lumi_n = ientry.lumi.iloc[0]
    evt_n = ientry.evt.iloc[0]

    triplEff_counter[0] = True
    mu_good = []
    mu_Ind_good = []
    ind_good = -99
    for i in range(NMU):
        mu_good.append(ind_good)
        mu_Ind_good.append(ind_good)
    goodTriplInd = []

    #CUT 0 : Before cuts - skip event if no good triplets
    if (ientry.NGoodTriplets.iloc[0][0] < 1):
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
    print(len(ientry.Trigger_l1name.iloc[0]))
    for h in range(len(ientry.Trigger_l1name.iloc[0])):
        l1Name = ientry.Trigger_l1name.iloc[0][h]
        if ("L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4" in l1Name or "L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4" in l1Name or "L1_DoubleMu4_SQ_OS_dR_Max1p2" in l1Name or "L1_DoubleMu4p5_SQ_OS_dR_Max1p2" in l1Name or "L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p6" in l1Name or "L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5" in l1Name ) and ientry.Trigger_l1decision.iloc[0][h] == 1:
            L1_passed = True
            if(debugMode): print("L1 passed\n")
            if ("L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4" in l1Name and ientry.Trigger_l1decision.iloc[0][h] == 1):
                L1seed+=1
                L1_DoubleMu0_er1p5=1
            if ("L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4" in l1Name and ientry.Trigger_l1decision.iloc[0][h] == 1): L1_DoubleMu0_er1p4=1
            if ("L1_DoubleMu4_SQ_OS_dR_Max1p2" in l1Name and ientry.Trigger_l1decision.iloc[0][h] == 1):
                L1seed+=10
                L1_DoubleMu4_dR1p2=1
            if ("L1_DoubleMu4p5_SQ_OS_dR_Max1p2" in l1Name and ientry.Trigger_l1decision.iloc[0][h] == 1): L1_DoubleMu4p5_dR1p2=1
            if ("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p6" in l1Name and ientry.Trigger_l1decision.iloc[0][h] == 1):
                L1seed+=1000
                L1_DoubleMu0_er2p0=1
            if ("L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5" in l1Name and ientry.Trigger_l1decision.iloc[0][h] == 1): L1_DoubleMu0_er2p0_bk=1

    if (L1_passed): 
        triplEff_counter[1] = True
        if (debugMode): print(f"L1seed: {L1seed}\n")
    else:
        cutevt[0]+=1
        return None

    # Check HLT
    for h in range(len(ientry.Trigger_hltname.iloc[0])):
        hltName = ientry.Trigger_hltname.iloc[0][h]
        if ("HLT_DoubleMu3_Trk_Tau3mu_v" in hltName and ientry.Trigger_hltdecision.iloc[0][h] == 1):
        #if( (hltName.Contains("HLT_DoubleMu3_Trk_Tau3mu_v") || hltName.Contains("HLT_DoubleMu4_3_LowMass") || hltName.Contains("HLT_DoubleMu4_LowMass_Displaced") ) andand Trigger_hltdecision->at(h) == 1) {
            HLT_passed = True
            if ("HLT_DoubleMu3_Trk_Tau3mu_v" in hltName and ientry.Trigger_hltdecision.iloc[0][h] == 1): HLTpath += 1
            if ("HLT_DoubleMu4_3_LowMass" in hltName and ientry.Trigger_hltdecision.iloc[0][h] == 1): HLTpath += 10
            if ("HLT_DoubleMu4_LowMass_Displaced" in hltName and ientry.Trigger_hltdecision.iloc[0][h] == 1): HLTpath += 100
    if (HLT_passed): triplEff_counter[2] = True
    if (debugMode): print(f"HLT passed -> HLTpath = {HLTpath}\n")

    if not HLT_passed:
        for i in range(2):
            if (debugMode): print(f"triplEff_counter[{i}] = {triplEff_counter[i]}\n")
            if(triplEff_counter[i] == True):
                cutevt[i]+=1
                if(debugMode): print("It's true!")
        return None

    #Loop over the TRIPLETS
    for j in range(len(ientry.TripletVtx2_Chi2.iloc[0])):
        goodTripl = False
        if (debugMode):print(f"\nTriplet n. {j}\n")
        pt = []
        eta=[]
        phi=[]
        mu=[]
        mu_Ind=[]
        for i in range(NMU):
            pt.append(0)
            eta.append(0)
            phi.append(0)
            mu.append(0)
            mu_Ind.append(0)
        if (ientry.Tr_Pt.iloc[0][j] < 2): continue
        MatchIndex(ientry, "ID", j, mu_Ind, mu)
        Get_MuonAndTrackVariables(ientry, mu_Ind, pt, eta, phi)
    
        # CUT 2 : 2 Glb and Medium mu
        good_muonID = False
        if (ientry.Muon_isGlobal.iloc[0][mu[0]] == 1 and ientry.Muon_isMedium.iloc[0][mu[0]] == 1 
            and ientry.Muon_isGlobal.iloc[0][mu[1]] == 1 and ientry.Muon_isMedium.iloc[0][mu[1]] == 1 
            and ientry.Mu01_Pt.iloc[0][j] >= 2 and ientry.Mu02_Pt.iloc[0][j] >= 2 
            and abs(ientry.Mu01_Eta.iloc[0][j])<=2.4 and abs(ientry.Mu02_Eta.iloc[0][j])<=2.4 
            and ientry.Tr_Pt.iloc[0][j] >= 2 and abs(ientry.Tr_Eta.iloc[0][j])<=2.4 
            and (ientry.Track_dz.iloc[0][mu[2]]) < 20 and ientry.Track_dxy.iloc[0][mu[2]] <0.3): # check duplicates
            #if(Muon_isMedium->at(mu[0]) == 1 andand Muon_isMedium->at(mu[1]) == 1 andand Mu01_Pt->at(j) >= 2 andand Mu02_Pt->at(j) >= 2 andand abs(Mu01_Eta->at(j))<=2.4 andand abs(Mu02_Eta->at(j))<=2.4 andand Tr_Pt->at(j) >= 2 andand abs(Tr_Eta->at(j))<=2.4 andand (Track_dz->at(mu[2]) < 20 andand Track_dxy->at(mu[2]) <0.3)) { // check duplicates
            isDupl = DuplicateFinder(ientry, ientry.Mu01_Eta.iloc[0][j], ientry.Mu02_Eta.iloc[0][j], ientry.Tr_Eta.iloc[0][j], ientry.Mu01_Phi.iloc[0][j], ientry.Mu02_Phi.iloc[0][j], ientry.Tr_Phi.iloc[0][j], ientry.Mu01_Pt.iloc[0][j], ientry.Mu02_Pt.iloc[0][j], ientry.Tr_Pt.iloc[0][j])
            if (isDupl and ientry.FlightDistBS_SV_Significance.iloc[0][j] >= 3.5 ):
                good_muonID = True
                if(debugMode): print("goodMuonID\n")
            if not good_muonID: continue
            else: triplEff_counter[3] = True
        
        # CUT 3 : OS DiMu mass in [0.98-1.06]
        good_diMuMass = False
        DiMuMass = [0,0,0]
        DiMuMass[0] = DimuonMass(ientry, mu[0], mu[1]) # diMuMass 12
        if (DiMuMass[0]<=1.06 and DiMuMass[0]>=0.98): good_diMuMass = True
        if not good_diMuMass: continue
        else: triplEff_counter[4] = True
    
        # CUT 4 : TripletMass in [1.62-2] GeV
        good_triMuMass = False
        if (ientry.Triplet2_Mass.iloc[0][j]<=2.1 and ientry.Triplet2_Mass.iloc[0][j]>=1.62):
            good_triMuMass = True 
            if (debugMode): print("goodTriMuMass: {Triplet2_Mass[j]}\n")
        if not good_triMuMass: continue
        else: triplEff_counter[5] = True
    
        # CUT 5 : HLT Trigger Matching
        triggerMatch = [False, False]
        #vector<double> HLT_obj_pt, HLT_obj_eta, HLT_obj_phi;
        HLT_obj_pt = []
        HLT_obj_eta = []
        HLT_obj_phi = []

        if(HLTpath==1 or HLTpath==11 or HLTpath==101 or HLTpath==111):
            for i in range(len(ientry.MuonPt_HLT2017.iloc[0])):
                HLT_obj_pt.append(ientry.MuonPt_HLT2017.iloc[0][i])
                HLT_obj_eta.append(ientry.MuonEta_HLT2017.iloc[0][i])
                HLT_obj_phi.append(ientry.MuonPhi_HLT2017.iloc[0][i])
        else:
            if(HLTpath>=100):
                for i in range(len(ientry.MuonPt_HLT_DiMu_Incl_displ.iloc[0])):
                    HLT_obj_pt.append(ientry.MuonPt_HLT_DiMu_Incl_displ.iloc[0][i])
                    HLT_obj_eta.append(ientry.MuonEta_HLT_DiMu_Incl_displ.iloc[0][i])
                    HLT_obj_phi.append(ientry.MuonPhi_HLT_DiMu_Incl_displ.iloc[0][i])
            else:
                for i in range(len(ientry.MuonPt_HLT_DiMu_Incl.iloc[0])):
                    HLT_obj_pt.append(ientry.MuonPt_HLT_DiMu_Incl.iloc[0][i])
                    HLT_obj_eta.append(ientry.MuonEta_HLT_DiMu_Incl.iloc[0][i])
                    HLT_obj_phi.append(ientry.MuonPhi_HLT_DiMu_Incl.iloc[0][i])

    
        for f in range(2):
            for i in range(len(HLT_obj_pt)):
                dphi = abs(phi[f] - HLT_obj_phi[i])
                deta = abs(eta[f] - HLT_obj_eta[i])
                if (dphi > math.pi): dphi -= 2*math.pi
                dR = math.sqrt(dphi*dphi + deta*deta)
                dpt = abs(pt[f] - HLT_obj_pt[i])/pt[f]
                if (dR<0.03 and dpt<0.1): triggerMatch[f] = True
        if(triggerMatch[0] == True): triplEff_counter[6] = True
        if(triggerMatch[0] == True and triggerMatch[1] == True):
            triplEff_counter[7] = True
            triplEff_counter[8] = True

        if (triggerMatch[0] != True or triggerMatch[1] != True): continue
        else:
            if (debugMode): print("Good trigger Matching\n")
    
        if (good_muonID == True and good_diMuMass == True and good_triMuMass == True and triggerMatch[0] == True and triggerMatch[1] == True):
            goodTripl = True
            if (debugMode): 
                print("Questo tripletto è buono!!!\n")
                goodTriplInd.append(j)
            for i in range(NMU):
                mu_Ind_good[i] = mu_Ind[i]
                mu_good[i] = mu[i]
        else:
            if (debugMode): print("C'è un baco!!!\n")
# end loop on triplet

    for i in range(NCUTS):
        if (debugMode): print(f"triplEff_counter[{i}] = {triplEff_counter[i]}")
        if (triplEff_counter[i] == True):
            if (debugMode):
                print("It's true!")
                cutevt[i]+=1

    if (debugMode): print("Lista di tripletti buoni nell'evento: ")
    for i in range(len(goodTriplInd)):
        if (debugMode): print(goodTriplInd[i])
    
    
    if(len(goodTriplInd)>0):
        ind_good = BestTripletFinder(ientry, goodTriplInd)
        if(debugMode):
            print(f"\nQuesto è il tripletto buono: {ind_good}\nN tripletti buoni: {len(goodTriplInd)}")
            print("\nFound a good triplet\n")
        MatchIndex(ientry, "ID", ind_good, mu_Ind_good, mu_good)
        TreeFin_Fill(ientry, jentry, df_fin, isMC, debugMode, ind_good, mu_Ind_good, mu_good, lumi_n, run_n, evt_n, pileupFactor, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2, L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath, deltaR_max, deltaZ_max, Pmu3, cLP, tKink, segmComp, tripletMass, tripletMassReso, fv_nC, fv_dphi3D, fv_d3D, fv_d3Dsig, d0, nVtx, d0sig, MVA1, MVA2, MVA3, MVASoft1, MVASoft2, MVASoft3,  d0sig_max, mindca_iso, trkRel, Pmu1, Ptmu1, etamu1, phimu1, Pmu2, Ptmu2, etamu2, phimu2, Ptmu3, etamu3, phimu3, dispMu1, dispMu2, dispMu3, xydispMu1, xydispMu2, xydispMu3, P_trip, Pt_trip, eta_trip, nStationsMu1, nStationsMu2, nStationsMu3, Iso03Mu1, Iso03Mu2, Iso03Mu3, Iso05Mu1, Iso05Mu2, Iso05Mu3, nMatchesMu1, nMatchesMu2, nMatchesMu3, timeAtIpInOutMu_sig1, timeAtIpInOutMu_sig2, timeAtIpInOutMu_sig3, cQ_uS, cQ_tK, cQ_gK, cQ_tRChi2, cQ_sRChi2, cQ_Chi2LP, cQ_Chi2LM, cQ_lD, cQ_gDEP, cQ_tM, cQ_gTP, calEn_emMu1, calEn_emMu2, calEn_emMu3, calEn_hadMu1, calEn_hadMu2, calEn_hadMu3, caloComp, fliDistPVSV_Chi2, isMedium1, isMedium2, isGlb1, isTracker1, isLoose1,  isSoft1, isPF1, isRPC1, isSA1, isCalo1, isGlb2, isTracker2, isLoose2,  isSoft2, isPF2, isRPC2, isSA2, isCalo2, isGlb3, isTracker3, isLoose3,  isSoft3, isPF3, isRPC3, isSA3, isCalo3, vx1, vx2, vx3, vy1, vy2, vy3, vz1, vz2, vz3, Refvx1, Refvx2, Refvx3, Refvy1, Refvy2, Refvy3, Refvz1, Refvz2, Refvz3, SVx, SVy, SVz, had03, had05, nJets03, nJets05, nTracks03, nTracks05, sumPt03, sumPt05, hadVeto03, hadVeto05, emVeto03, emVeto05, trVeto03, trVeto05, EnMu1, EnMu2, EnMu3, ChargeMu1, ChargeMu2, ChargeMu3, isQValid1, isTValid1, isIsoValid1, GLnormChi2_mu1, GL_nValidMuHits1, trkLayersWMeas1, nValidPixelHits1, outerTrk_P_1, outerTrk_Eta_1, outerTrk_normChi2_1, outerTrk_muStValidHits_1, innerTrk_P_1, innerTrk_Eta_1, innerTrk_normChi2_1, QInnerOuter_1, cQ_uS_1, cQ_tK_1, cQ_gK_1, cQ_tRChi2_1, cQ_sRChi2_1, cQ_Chi2LP_1, cQ_Chi2LM_1, cQ_lD_1, cQ_gDEP_1, cQ_tM_1, cQ_gTP_1, segmComp_1, caloComp_1, isQValid2, isTValid2, isIsoValid2, GLnormChi2_mu2, GL_nValidMuHits2, trkLayersWMeas2, nValidPixelHits2, outerTrk_P_2, outerTrk_Eta_2, outerTrk_normChi2_2, outerTrk_muStValidHits_2, innerTrk_P_2, innerTrk_Eta_2, innerTrk_normChi2_2, QInnerOuter_2, cQ_uS_2, cQ_tK_2, cQ_gK_2, cQ_tRChi2_2, cQ_sRChi2_2, cQ_Chi2LP_2, cQ_Chi2LM_2, cQ_lD_2, cQ_gDEP_2, cQ_tM_2, cQ_gTP_2, segmComp_2, caloComp_2, isQValid3, isTValid3, isIsoValid3, GLnormChi2_mu3, GL_nValidMuHits3, trkLayersWMeas3, nValidPixelHits3, outerTrk_P_3, outerTrk_Eta_3, outerTrk_normChi2_3, outerTrk_muStValidHits_3, innerTrk_P_3, innerTrk_Eta_3, innerTrk_normChi2_3, QInnerOuter_3, cQ_uS_3, cQ_tK_3, cQ_gK_3, cQ_tRChi2_3, cQ_sRChi2_3, cQ_Chi2LP_3, cQ_Chi2LM_3, cQ_lD_3, cQ_gDEP_3, cQ_tM_3, cQ_gTP_3, segmComp_3, caloComp_3, match1_dX_1, match1_pullX_1, match1_pullDxDz_1, match1_dY_1, match1_pullY_1, match1_pullDyDz_1, match2_dX_1, match2_pullX_1, match2_pullDxDz_1, match2_dY_1, match2_pullY_1, match2_pullDyDz_1, match1_dX_2, match1_pullX_2, match1_pullDxDz_2, match1_dY_2, match1_pullY_2, match1_pullDyDz_2, match2_dX_2, match2_pullX_2, match2_pullDxDz_2, match2_dY_2, match2_pullY_2, match2_pullDyDz_2, match1_dX_3, match1_pullX_3, match1_pullDxDz_3, match1_dY_3, match1_pullY_3, match1_pullDyDz_3, match2_dX_3, match2_pullX_3, match2_pullDxDz_3, match2_dY_3, match2_pullY_3, match2_pullDyDz_3, innerTrk_highPurity_1, innerTrk_highPurity_2, innerTrk_highPurity_3, innerTrk_ValidFraction_1, innerTrk_ValidFraction_2, innerTrk_ValidFraction_3, nValidTrackerHits1, nValidTrackerHits2, nValidTrackerHits3, validMuonHitComb1, validMuonHitComb2, validMuonHitComb3)



def Loop_DsPhiPi(tree, type, datasetName, filename):
    df = tree
    print(df)
    length = len(df)
    print(length)
    if length==0: return
    nentries = length

    # Variables definition and init
    cutevt = []
    for i in range(NCUTS):
        cutevt.append(0)
    listCut = []
    Fill_CutName(df,listCut)
    debugMode = True

    '''
    # Creation of the output file
    root_fileName = filename
    fout = ROOT.TFile(root_fileName, "RECREATE")
    fout.cd()
    tree = ROOT.TTree("FinalTree","FinalTree")
    '''
    #TreeFin_Init(tree, isMC, lumi_n, run_n, evt_n, pileupFactor, L1_DoubleMu0_er1p5, L1_DoubleMu0_er1p4, L1_DoubleMu4_dR1p2, L1_DoubleMu4p5_dR1p2, L1_DoubleMu0_er2p0, L1_DoubleMu0_er2p0_bk, L1seed, HLTpath, deltaR_max, deltaZ_max, Pmu3, cLP, tKink, segmComp, tripletMass, tripletMassReso, fv_nC, fv_dphi3D, fv_d3D, fv_d3Dsig, d0, nVtx, d0sig, MVA1, MVA2, MVA3, MVASoft1, MVASoft2, MVASoft3, d0sig_max, mindca_iso, trkRel, Pmu1, Ptmu1, etamu1, phimu1, Pmu2, Ptmu2, etamu2, phimu2, Ptmu3, etamu3, phimu3, dispMu1, dispMu2, dispMu3, xydispMu1, xydispMu2, xydispMu3, P_trip, Pt_trip, eta_trip, nStationsMu1, nStationsMu2, nStationsMu3, Iso03Mu1, Iso03Mu2, Iso03Mu3, Iso05Mu1, Iso05Mu2, Iso05Mu3, nMatchesMu1, nMatchesMu2, nMatchesMu3, timeAtIpInOutMu_sig1, timeAtIpInOutMu_sig2, timeAtIpInOutMu_sig3, cQ_uS, cQ_tK, cQ_gK, cQ_tRChi2, cQ_sRChi2, cQ_Chi2LP, cQ_Chi2LM, cQ_lD, cQ_gDEP, cQ_tM, cQ_gTP, calEn_emMu1, calEn_emMu2, calEn_emMu3, calEn_hadMu1, calEn_hadMu2, calEn_hadMu3, caloComp, fliDistPVSV_Chi2, isMedium1, isMedium2, isGlb1, isTracker1, isLoose1,  isSoft1, isPF1, isRPC1, isSA1, isCalo1, isGlb2, isTracker2, isLoose2,  isSoft2, isPF2, isRPC2, isSA2, isCalo2, isGlb3, isTracker3, isLoose3,  isSoft3, isPF3, isRPC3, isSA3, isCalo3, vx1, vx2, vx3, vy1, vy2, vy3, vz1, vz2, vz3, Refvx1, Refvx2, Refvx3, Refvy1, Refvy2, Refvy3, Refvz1, Refvz2, Refvz3, SVx, SVy, SVz, had03, had05, nJets03, nJets05, nTracks03, nTracks05, sumPt03, sumPt05, hadVeto03, hadVeto05, emVeto03, emVeto05, trVeto03, trVeto05, EnMu1, EnMu2, EnMu3, ChargeMu1, ChargeMu2, ChargeMu3, isQValid1, isTValid1, isIsoValid1, GLnormChi2_mu1, GL_nValidMuHits1, trkLayersWMeas1, nValidPixelHits1, outerTrk_P_1, outerTrk_Eta_1, outerTrk_normChi2_1, outerTrk_muStValidHits_1, innerTrk_P_1, innerTrk_Eta_1, innerTrk_normChi2_1, QInnerOuter_1, cQ_uS_1, cQ_tK_1, cQ_gK_1, cQ_tRChi2_1, cQ_sRChi2_1, cQ_Chi2LP_1, cQ_Chi2LM_1, cQ_lD_1, cQ_gDEP_1, cQ_tM_1, cQ_gTP_1, segmComp_1, caloComp_1, isQValid2, isTValid2, isIsoValid2, GLnormChi2_mu2, GL_nValidMuHits2, trkLayersWMeas2, nValidPixelHits2, outerTrk_P_2, outerTrk_Eta_2, outerTrk_normChi2_2, outerTrk_muStValidHits_2, innerTrk_P_2, innerTrk_Eta_2, innerTrk_normChi2_2, QInnerOuter_2, cQ_uS_2, cQ_tK_2, cQ_gK_2, cQ_tRChi2_2, cQ_sRChi2_2, cQ_Chi2LP_2, cQ_Chi2LM_2, cQ_lD_2, cQ_gDEP_2, cQ_tM_2, cQ_gTP_2, segmComp_2, caloComp_2, isQValid3, isTValid3, isIsoValid3, GLnormChi2_mu3, GL_nValidMuHits3, trkLayersWMeas3, nValidPixelHits3, outerTrk_P_3, outerTrk_Eta_3, outerTrk_normChi2_3, outerTrk_muStValidHits_3, innerTrk_P_3, innerTrk_Eta_3, innerTrk_normChi2_3, QInnerOuter_3, cQ_uS_3, cQ_tK_3, cQ_gK_3, cQ_tRChi2_3, cQ_sRChi2_3, cQ_Chi2LP_3, cQ_Chi2LM_3, cQ_lD_3, cQ_gDEP_3, cQ_tM_3, cQ_gTP_3, segmComp_3, caloComp_3, match1_dX_1, match1_pullX_1, match1_pullDxDz_1, match1_dY_1, match1_pullY_1, match1_pullDyDz_1, match2_dX_1, match2_pullX_1, match2_pullDxDz_1, match2_dY_1, match2_pullY_1, match2_pullDyDz_1, match1_dX_2, match1_pullX_2, match1_pullDxDz_2, match1_dY_2, match1_pullY_2, match1_pullDyDz_2, match2_dX_2, match2_pullX_2, match2_pullDxDz_2, match2_dY_2, match2_pullY_2, match2_pullDyDz_2, match1_dX_3, match1_pullX_3, match1_pullDxDz_3, match1_dY_3, match1_pullY_3, match1_pullDyDz_3, match2_dX_3, match2_pullX_3, match2_pullDxDz_3, match2_dY_3, match2_pullY_3, match2_pullDyDz_3, innerTrk_highPurity_1, innerTrk_highPurity_2, innerTrk_highPurity_3, innerTrk_ValidFraction_1, innerTrk_ValidFraction_2, innerTrk_ValidFraction_3, nValidTrackerHits1, nValidTrackerHits2, nValidTrackerHits3, validMuonHitComb1, validMuonHitComb2, validMuonHitComb3)
    headers = pd.read_csv("headers.csv")
    df_fin = pd.DataFrame(index = range(nentries), columns = headers)
    print(df_fin)
    hCutEffEvt = ROOT.TH1I("CutEff_NEvents", "CutEff_NEvents", NCUTS, 0.5, (NCUTS+0.5))

    print(f"datasetName: {datasetName}\n")
    if("2022" in datasetName or "2023" in datasetName): isMC=0
    else: isMC=5
    
    df.groupby(df.index).apply(loop_events, debugMode, cutevt, df_fin, isMC)

    #for  jentry in range(nentries):

    #Histo of cuts Efficiency
    canvEvt = ROOT.TCanvas("CutEfficiency_Nevents", "CutEfficiency_Nevents", 0, 0, 1200, 1000)
    Draw_CutEffCanvas(df, canvEvt, hCutEffEvt, cutevt, listCut)

    # Convert the DataFrame into a dictionary of arrays (one for each column)
    arrays = {col: df_fin[col].values for col in df_fin.columns}

    # Open a ROOT file and write the TTree
    with uproot.recreate(filename) as root_file:
        root_file["FinalTree"] = arrays  # Write the arrays to the tree
    #df_fin.Snapshot("FinalTree", filename)


