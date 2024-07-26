#define myAnalyzer_cxx
#define NCUTS 9
#define NMU 3
#define mumass 0.1056583715 // Muon mass in GeV
#define PhiMass 1.019461 // Phi mass in GeV
#define sigmaPhiMass 0.011 //sigma of Phi mass in GeV 
#define OmegaMass 0.78265 // Omega mass in GeV
#define sigmaOmegaMass 0.0085 //sigma of Omega mass in GeV
#define ptmin 2.0

#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include "TMath.h"
#include <TMVA/Reader.h>

std::vector<double> pileup_weight;
double pileupFactor = 1;

Int_t myAnalizer::BestTripletFinder(vector<int> triplIndex){
    // Given the index of all the triplets of an event that passed all the cuts, it returns the index of the one with the smallest Chi2 of the vertex
   //cout << "++++ N. good triplets: " << triplIndex.size() << endl;
   int index = -99; double bestChi2 = 15000000000;
   index = triplIndex.at(0);
    for(int i=0; i<triplIndex.size(); i++){
     //   cout << "Good triplet n. " << i << " | Index: " << triplIndex.at(i) << " | Chi2: " << TripletVtx_Chi2->at(triplIndex.at(i)) << endl;
        if(TripletVtx_Chi2->at(triplIndex.at(i)) < bestChi2){
            bestChi2 = TripletVtx_Chi2->at(triplIndex.at(i));
            index = triplIndex.at(i);
        }
    }
    //cout << "Triplet chosen: " << index << endl;
    return index;
}

Double_t myAnalizer::deltaR(Double_t eta1, Double_t eta2, Double_t phi1, Double_t phi2){
    auto dp = std::abs(phi1 - phi2);
    auto deta = std::abs(eta1 - eta2);
    if (dp > Double_t(M_PI))
        dp -= Double_t(2 * M_PI);
    Double_t n = TMath::Sqrt(dp*dp + deta*deta);
    return n;
}

Double_t myAnalizer::DimuonMass(Int_t mu_index1, Int_t mu_index2){
    // Given the characteristics of 2 muons, if their charge is opposite the function returns their invariant mass, otherwise it returns 0
    double inv = 0;
    double charge1 = MuonCharge->at(mu_index1);
    double charge2 = MuonCharge->at(mu_index2);
    double pt1 = MuonPt->at(mu_index1);
    double pt2 = MuonPt->at(mu_index2);
    double eta1 = MuonEta->at(mu_index1);
    double eta2 = MuonEta->at(mu_index2);
    double phi1 = MuonPhi->at(mu_index1);
    double phi2 = MuonPhi->at(mu_index2);
    double en1 = MuonEnergy->at(mu_index1);
    double en2 = MuonEnergy->at(mu_index2);
    if(charge1 + charge2 != 0)  return inv;
    else {
        TLorentzVector mu1, mu2, mutot;
        mu1.SetPtEtaPhiE(pt1, eta1, phi1, en1);
        mu2.SetPtEtaPhiE(pt2, eta2, phi2, en2);
        mutot = mu1 + mu2;
        return mutot.M();
    }
}

void myAnalizer::Fill_CutName(TString listCut[NCUTS]){
    // Init a vector of strings w/ the names of the cuts
    listCut[0] = "BeforeCuts";
    listCut[1] = "L1_fired";
    listCut[2] = "HLT_fired";
    listCut[3] = "MuonID";
    listCut[4] = "BS-SV sign, deltaR-Z";
    listCut[5] = "TriMu_mass";
    listCut[6] = "mu1_TrMatch";
    listCut[7] = "mu12_TrMatch";
    listCut[8] = "mu123_TrMatch";
}

void myAnalizer::Draw_CutEffCanvas(TCanvas *canv, TH1I *hist, Int_t cut[NCUTS], TString listCut[NCUTS]){
    // This function writes on the canvas the histo of the cuts efficiency
    for(int k=0; k<NCUTS; k++){
        hist->Fill(k+1, cut[k]);
        hist->GetXaxis()->SetBinLabel(k+1, listCut[k]);
    }
//    canv->SetLogy();
    hist->DrawCopy("HIST TEXT0");
    hist->Write();
//    canv->Write();
//    canv->Close();
}

void myAnalizer::Get_MuonVariables(Int_t mu_Ind[NMU], Double_t pt[NMU], Double_t eta[NMU], Double_t phi[NMU]){
    // Fills vectors w/ the variables of the muons of the triplet
    pt[0] = Mu1_Pt->at(mu_Ind[0]);
    pt[1] = Mu2_Pt->at(mu_Ind[1]);
    pt[2] = Mu3_Pt->at(mu_Ind[2]);
    eta[0] = Mu1_Eta->at(mu_Ind[0]);
    eta[1] = Mu2_Eta->at(mu_Ind[1]);
    eta[2] = Mu3_Eta->at(mu_Ind[2]);
    phi[0] = Mu1_Phi->at(mu_Ind[0]);
    phi[1] = Mu2_Phi->at(mu_Ind[1]);
    phi[2] = Mu3_Phi->at(mu_Ind[2]);
}

Bool_t myAnalizer::isPairDeltaRGood(Int_t ntriplet, Double_t DeltaRmax){
    // The function returns 'true' if all of the 3 possible pairs of muons have dR<DeltaRmax
    Double_t dR12 = deltaR(Mu1_Eta->at(ntriplet), Mu2_Eta->at(ntriplet), Mu1_Phi->at(ntriplet), Mu2_Phi->at(ntriplet));
    Double_t dR13 = deltaR(Mu1_Eta->at(ntriplet), Mu3_Eta->at(ntriplet), Mu1_Phi->at(ntriplet), Mu3_Phi->at(ntriplet));
    Double_t dR23 = deltaR(Mu2_Eta->at(ntriplet), Mu3_Eta->at(ntriplet), Mu2_Phi->at(ntriplet), Mu3_Phi->at(ntriplet));
 
    if (dR12<DeltaRmax && dR13<DeltaRmax && dR23<DeltaRmax) return true;
    else return false;
}

Bool_t myAnalizer::isPairDeltaZGood(Double_t vz1, Double_t vz2, Double_t vz3, Double_t DeltaZmax){
    // The function returns 'true' if all of the 3 possible pairs of muons have dZ<DeltaZmax
    Double_t dZ12 = TMath::Abs(vz2 - vz1);
    Double_t dZ13 = TMath::Abs(vz3 - vz1);
    Double_t dZ23 = TMath::Abs(vz3 - vz2);
    
    if (dZ12<DeltaZmax && dZ13<DeltaZmax && dZ23<DeltaZmax) return true;
    else return false;
}

void myAnalizer::MatchIndex(TString type, Int_t ind, Int_t mu_Ind[NMU], Int_t mu[NMU]){
    // This function matches the index of muons in different cases (ID or GEN muons)
    mu_Ind[0] = ind;
    mu_Ind[1] = ind;
    mu_Ind[2] = ind;
    if (mu_Ind[0] != ind || mu_Ind[1] != ind || mu_Ind[2] != ind) cout << "Error : Different triplet mu indices!" << endl;
    double pt[NMU] = {0}, eta[NMU] = {0}, phi[NMU] = {0};
    Get_MuonVariables(mu_Ind, pt, eta, phi);
    for(int k=0; k<NMU; k++){
        if (strcmp(type, "ID") == 0)    mu[k] = MuonFinder(pt[k], eta[k], phi[k]);
        //if (strcmp(type, "Gen") == 0)   mu[k] = MuonFinderGen(k+1, pt[k], eta[k], phi[k]);
    }
}


Double_t myAnalizer::MuonFinder(Double_t pt, Double_t eta, Double_t phi){
    // Given the characteristics of a muon (pt, eta, phi), the function returns the index of the corresponding muon in the event
    
    // PRIORITY [in case there is more than 1 muon that matches the conditions]
    
    // *** if (there aren't muons w/ outerTrachChi2 != -999)    ## CASE 0 ##
    //      -> consider the one w/ the smallest innerTrackChi2
    //      -> if innerTrackChi2 are equal:
    //          -> consider the one w/ the biggest number of matches
    //              (if they are equal, print an error message and return the index of the last one)
    //
    // *** if (outerTrack != -999)                              ## CASE 1,2 ##
    //      -> consider the one w/ the smallest outerTrackChi2
    //      -> if outerTrackChi2 are equal:
    //          -> consider the one w/ the smallest innerTrackChi2
    //              -> consider the one w/ the biggest number of matches
    //                   (if they are equal, print an error message and return the index of the last one)
    
    int n=0, m=0, badOuterChi2=0;
    for(int g=0; g<MuonPt->size(); g++){
        if(pt == MuonPt->at(g) && eta == MuonEta->at(g) && phi == MuonPhi->at(g)){
            n++;
            m = g;
            if(Muon_outerTrack_normalizedChi2->at(g) == -999)
                badOuterChi2++;
        }
    }
    
    // MULTIPLE muons (There is more than 1 muon that matches the conditions)
    if(n>1) {
        
        // ####### CASE 0: there aren't muons w/ outerTrachChi2 != -999
        if((n-badOuterChi2) == 0){
            double Chi2InnerTrackmin[2] = {0}; // Chi2InnerTrackmin[1] is the value of Chi2; Chi2InnerTrackmin[0] is the corresponding index
            Chi2InnerTrackmin[1] = 999;
            // find the muon w/ the smallest innerTrackChi2
            for (int k=0; k<MuonPt->size(); k++){
                if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Muon_innerTrack_normalizedChi2->at(k) < Chi2InnerTrackmin[1]){
                    Chi2InnerTrackmin[1] = Muon_innerTrack_normalizedChi2->at(k);
                    Chi2InnerTrackmin[0] = k;
                }
            }
            int nMuonChi2InnerMin = 0;
            for (int k=0; k<MuonPt->size(); k++){
                if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Chi2InnerTrackmin[1] == Muon_innerTrack_normalizedChi2->at(k)){
                    nMuonChi2InnerMin++;
                }
            }
            if(nMuonChi2InnerMin == 1){
                return Chi2InnerTrackmin[0];
            }
            // find the mu w/ the biggest number of matches
            else {
                double NumberOfMatches[2] = {0}; // like Chi2InnerTrackmin[]
                for (int k=0; k<MuonPt->size(); k++){
                    if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Chi2InnerTrackmin[1] == Muon_innerTrack_normalizedChi2->at(k)){
                        if(Muon_numberOfMatches->at(k) > NumberOfMatches[1]){
                            NumberOfMatches[1] = Muon_numberOfMatches->at(k);
                            NumberOfMatches[0] = k;
                        }
                    }
                }
                int nMuonMatchesMax = 0;
                for (int k=0; k<MuonPt->size(); k++){
                    if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Chi2InnerTrackmin[1] == Muon_innerTrack_normalizedChi2->at(k) && NumberOfMatches[1] == Muon_numberOfMatches->at(k)){
                        nMuonMatchesMax++;
                    }
                }
                if(nMuonMatchesMax == 1){
                    return NumberOfMatches[0];
                }
                // They are equal, therefore print an error message and return the index of the last one
                else{
                    cout << "Multiple muons with outerChi2 = -999! " << endl;
                    return NumberOfMatches[0];
                }
            }
        }
        
        // ####### CASE 1:  // There is ONLY 1 muon that has outerTrachChi2 != -999
        else if((n-badOuterChi2) == 1){
            // Find this muon and return its index
            int indexGoodMu = -1;
            for (int k=0; k<MuonPt->size(); k++){
                if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Muon_outerTrack_normalizedChi2->at(k) != -999)
                    indexGoodMu = k;
            }
            if (indexGoodMu == -1)  cout << "There is a BUG for sure !!!" << endl;
            return indexGoodMu;
        }
        
        // ####### CASE 2:  // There is more than 1 muon w/ outerTrachChi2 != -999
        else if((n-badOuterChi2) > 1){
            double Chi2OuterTrackmin[2] = {0}; Chi2OuterTrackmin[1] = 999;
            // find the one w/ the smallest outerTrackChi2
            for (int k=0; k<MuonPt->size(); k++){
                if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Muon_outerTrack_normalizedChi2->at(k) < Chi2OuterTrackmin[1]){
                    Chi2OuterTrackmin[1] = Muon_outerTrack_normalizedChi2->at(k);
                    Chi2OuterTrackmin[0] = k;
                }
            }
            int nMuonChi2OuterMin = 0;
            for (int k=0; k<MuonPt->size(); k++){
                if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Chi2OuterTrackmin[1] == Muon_outerTrack_normalizedChi2->at(k))
                    nMuonChi2OuterMin++;
            }
            if(nMuonChi2OuterMin == 1)  return Chi2OuterTrackmin[0];
            // if outerTrackChi2 are equal
            else{
                // consider the one w/ the smallest innerTrackChi2
                double Chi2InnerTrackmin[2] = {0};
                Chi2InnerTrackmin[1] = 999;
                for (int k=0; k<MuonPt->size(); k++){
                    if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Muon_outerTrack_normalizedChi2->at(k) == Chi2OuterTrackmin[1] && Muon_innerTrack_normalizedChi2->at(k) < Chi2InnerTrackmin[1]){
                        Chi2InnerTrackmin[1] = Muon_innerTrack_normalizedChi2->at(k);
                        Chi2InnerTrackmin[0] = k;
                    }
                }
                int nMuonChi2InnerMin = 0;
                for (int k=0; k<MuonPt->size(); k++){
                    if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Muon_outerTrack_normalizedChi2->at(k) == Chi2OuterTrackmin[1] && Chi2InnerTrackmin[1] == Muon_innerTrack_normalizedChi2->at(k))
                        nMuonChi2InnerMin++;
                }
                if(nMuonChi2InnerMin == 1)  return Chi2InnerTrackmin[0];
                // find the one w/ the biggest number of matches
                else {
                    double NumberOfMatches[2] = {0};
                    for (int k=0; k<MuonPt->size(); k++){
                        if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Muon_outerTrack_normalizedChi2->at(k) == Chi2OuterTrackmin[1] && Chi2InnerTrackmin[1] == Muon_innerTrack_normalizedChi2->at(k)){
                            if(Muon_numberOfMatches->at(k) > NumberOfMatches[1]){
                                NumberOfMatches[1] = Muon_numberOfMatches->at(k);
                                NumberOfMatches[0] = k;
                            }
                        }
                    }
                    int nMuonMatchesMax = 0;
                    for (int k=0; k<MuonPt->size(); k++){
                        if(pt == MuonPt->at(k) && eta == MuonEta->at(k) && phi == MuonPhi->at(k) && Muon_outerTrack_normalizedChi2->at(k) == Chi2OuterTrackmin[1] && Chi2InnerTrackmin[1] == Muon_innerTrack_normalizedChi2->at(k) && NumberOfMatches[1] == Muon_numberOfMatches->at(k))
                            nMuonMatchesMax++;
                    }
                    if(nMuonMatchesMax == 1)    return NumberOfMatches[0];
                    // They are equal, therefore print an error message and return the index of the last one
                    else{
                        cout << "Multiple muons with outerChi2 != -999! " << endl;
                        return NumberOfMatches[0];
                    }
                }
            }
        }
        else {  // Error
            cout << "ERROR in multiple muon number!" << endl;
            return m;
        }
    }   // end multiple muons section
    
    else
        return m;
}

Double_t myAnalizer::MuonP(Double_t pt, Double_t eta, Double_t phi){
    // Given eta, phi of a muon, the function returns the momentum of the muon
    TVector3 muon;
    muon.SetPtEtaPhi(pt, eta, phi);
    return muon.Mag();
}
    

Double_t myAnalizer::ResoTriplMass(Int_t mu_Ind[NMU], Int_t mu[NMU]){
    // It computes the triplet mass resolution
    double pt[NMU] = {0}, ptNO[NMU] = {0}, eta[NMU] = {0}, phi[NMU] = {0}, pt_res[NMU] = {0}, pt_bis[NMU] = {0}, dm_pt[NMU] = {0}, dm_eta[NMU] = {0}, dm_phi[NMU] = {0};
    TLorentzVector muon[NMU], muon_deltaPt[NMU], muon_deltaEta[NMU], muon_deltaPhi[NMU];
    TLorentzVector tau, tau_PtUp[NMU], tau_EtaUp[NMU], tau_PhiUp[NMU];
    
    Get_MuonVariables(mu_Ind, pt, eta, phi);
    for(int k=0; k<NMU; k++){
        //pt[k] = Muon_BestTrackPt->at(mu[k]);
        //pt_bis[k] = pt[k] + Muon_BestTrackPtErr->at(mu[k]);
        muon[k].SetPtEtaPhiE(MuonPt->at(mu[k]), MuonEta->at(mu[k]), MuonPhi->at(mu[k]) , MuonEnergy->at(mu[k]));
        muon_deltaPt[k].SetPtEtaPhiM(pt[k] + Muon_BestTrackPtErr->at(mu[k]), eta[k], phi[k], muon[k].M());
        muon_deltaEta[k].SetPtEtaPhiM(pt[k], eta[k] + Muon_BestTrackEtaErr->at(mu[k]), phi[k], muon[k].M());
        muon_deltaPhi[k].SetPtEtaPhiM(pt[k], eta[k], phi[k] + Muon_BestTrackPhiErr->at(mu[k]), muon[k].M());
        //cout<<"MuonPt->at(mu["<<k<<"]) "<<MuonPt->at(mu[k])<<" MuonEta->at(mu["<<k<<"]) "<<MuonEta->at(mu[k])<<" MuonPhi->at(mu["<<k<<"]) "<<MuonPhi->at(mu[k])<<" MuonEnergy->at(mu["<<k<<"]) "<<MuonEnergy->at(mu[k])<<endl;
    }
    tau = muon[0] + muon[1] + muon[2];
    //cout<<" tau.Pt() "<<tau.Pt()<<" tau.Eta() "<<tau.Eta()<<" tau.Phi() "<<tau.Phi()<<" tau.E() "<<tau.E()<<endl;
    tau_PtUp[0] = muon_deltaPt[0] + muon[1] + muon[2];
    tau_PtUp[1] = muon[0] + muon_deltaPt[1] + muon[2];
    tau_PtUp[2] = muon[0] + muon[1] + muon_deltaPt[2];
    tau_EtaUp[0] = muon_deltaEta[0] + muon[1] + muon[2];
    tau_EtaUp[1] = muon[0] + muon_deltaEta[1] + muon[2];
    tau_EtaUp[2] = muon[0] + muon[1] + muon_deltaEta[2];
    tau_PhiUp[0] = muon_deltaPhi[0] + muon[1] + muon[2];
    tau_PhiUp[1] = muon[0] + muon_deltaPhi[1] + muon[2];
    tau_PhiUp[2] = muon[0] + muon[1] + muon_deltaPhi[2];
    for(int k=0; k<NMU; k++){
        dm_pt[k] = tau_PtUp[k].M() - tau.M();
        dm_eta[k] = tau_EtaUp[k].M() - tau.M();
        dm_phi[k] = tau_PhiUp[k].M() - tau.M();
    }
    double trimassReso_pt = sqrt(pow(dm_pt[0],2)+pow(dm_pt[1],2)+pow(dm_pt[2],2))/tau.M();
    double trimassReso_ptetaphi = sqrt(pow(dm_pt[0],2)+pow(dm_pt[1],2)+pow(dm_pt[2],2)+
                                       pow(dm_pt[0],2)+pow(dm_eta[1],2)+pow(dm_eta[2],2)+
                                       pow(dm_pt[0],2)+pow(dm_phi[1],2)+pow(dm_phi[2],2))/tau.M();
    return trimassReso_pt;
}


Double_t myAnalizer::TreeFin_Angle(Int_t ind){
    // Computes the angle between the momentum vector of the 3mu triplet (b) and the vector from the primary vertex (a)
    double a_x = TripletVtx_x->at(ind) - RefittedPV_x->at(ind);
    double a_y = TripletVtx_y->at(ind) - RefittedPV_y->at(ind);
    double a_z = TripletVtx_z->at(ind) - RefittedPV_z->at(ind);
    TVector3 b;
    b.SetPtEtaPhi(Triplet_Pt->at(ind), Triplet_Eta->at(ind), Triplet_Phi->at(ind));
    double b_x = b.Px();
    double b_y = b.Py();
    double b_z = b.Pz();
    double a_mod = abs(FlightDistPVSV->at(ind));
    double b_mod = abs(b.Mag());
    double cos_ang = ((a_x*b_x)+(a_y*b_y)+(a_z*b_z))/(a_mod*b_mod);
    double angle = acos(min(max(cos_ang,-1.0),1.0));
    return angle;
}

void myAnalizer::TreeFin_Fill(TTree *tree, Double_t isMC, Int_t ind, Int_t mu_Ind[NMU], Int_t mu[NMU], Double_t &lumi, Double_t &run, Double_t &evt, Double_t &puFactor, Double_t &category, Int_t &L1_DoubleMu0_er1p5, Int_t &L1_DoubleMu0_er1p4, Int_t &L1_DoubleMu4_dR1p2, Int_t &L1_DoubleMu4p5_dR1p2, Int_t &L1_DoubleMu0_er2p0, Int_t &L1_DoubleMu0_er2p0_bk, Int_t &L1_TripleMu_5SQ_3SQ_0, Int_t &L1_TripleMu_5SQ_3SQ_0OQ, Int_t &L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12, Int_t &L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12, Int_t &L1seed, Int_t &HLTpath, Double_t &DeltaR_max, Double_t &DeltaZ_max, Double_t &Pmu3, Double_t &cLP, Double_t &tKink, Double_t &segmComp, Double_t &tripletMass, Double_t &tripletMassReso, Double_t &fv_nC, Double_t &fv_dphi3D, Double_t &fv_d3D,  Double_t &fv_d3Dsig, Double_t &d0, Double_t &nVtx, Double_t &d0sig, Double_t &MVA1, Double_t &MVA2, Double_t &MVA3, Double_t &MVASoft1, Double_t &MVASoft2, Double_t &MVASoft3,  Double_t &d0sig_max, Double_t &mindca_iso, Double_t &trkRel, Double_t &Pmu1, Double_t &Ptmu1, Double_t &etamu1, Double_t &phimu1, Double_t &Pmu2, Double_t &Ptmu2, Double_t &etamu2, Double_t &phimu2, Double_t &Ptmu3, Double_t &etamu3, Double_t &phimu3, Double_t &dispMu1, Double_t &dispMu2, Double_t &dispMu3, Double_t &xydispMu1, Double_t &xydispMu2, Double_t &xydispMu3, Double_t &P_trip, Double_t &Pt_trip, Double_t &eta_trip, Double_t &nStationsMu1, Double_t &nStationsMu2, Double_t &nStationsMu3, Double_t &Iso03Mu1, Double_t &Iso03Mu2, Double_t &Iso03Mu3, Double_t &Iso05Mu1, Double_t &Iso05Mu2, Double_t &Iso05Mu3, Double_t &nMatchesMu1, Double_t &nMatchesMu2, Double_t &nMatchesMu3, Double_t &timeAtIpInOut_sig1, Double_t &timeAtIpInOut_sig2, Double_t &timeAtIpInOut_sig3, Double_t &cQ_uS, Double_t &cQ_tK, Double_t &cQ_gK, Double_t &cQ_tRChi2, Double_t &cQ_sRChi2, Double_t &cQ_Chi2LP, Double_t &cQ_Chi2LM, Double_t &cQ_lD, Double_t &cQ_gDEP, Double_t &cQ_tM, Double_t &cQ_gTP, Double_t &calEn_emMu1, Double_t &calEn_emMu2, Double_t &calEn_emMu3, Double_t &calEn_hadMu1, Double_t &calEn_hadMu2, Double_t &calEn_hadMu3, Double_t &caloComp, Double_t &fliDistPVSV_Chi2, Double_t &isMedium1, Double_t &isMedium2, Double_t &isMedium3, Double_t &isGlb1, Double_t &isTracker1, Double_t &isLoose1, Double_t &isSoft1, Double_t &isPF1, Double_t &isRPC1, Double_t &isSA1, Double_t &isCalo1, Double_t &isGlb2, Double_t &isTracker2, Double_t &isLoose2, Double_t &isSoft2, Double_t &isPF2, Double_t &isRPC2, Double_t &isSA2, Double_t &isCalo2, Double_t &isGlb3, Double_t &isTracker3, Double_t &isLoose3, Double_t &isSoft3, Double_t &isPF3, Double_t &isRPC3, Double_t &isSA3, Double_t &isCalo3, Double_t &Vx1, Double_t &Vx2, Double_t &Vx3, Double_t &Vy1, Double_t &Vy2, Double_t &Vy3, Double_t &Vz1, Double_t &Vz2, Double_t &Vz3, Double_t &RefVx1, Double_t &RefVx2, Double_t &RefVx3, Double_t &RefVy1, Double_t &RefVy2, Double_t &RefVy3, Double_t &RefVz1, Double_t &RefVz2, Double_t &RefVz3, Double_t &SVx, Double_t &SVy, Double_t &SVz, Double_t &had03, Double_t &had05, Double_t &nJets03, Double_t &nJets05, Double_t &nTracks03_mu1, Double_t &nTracks03_mu2, Double_t &nTracks03_mu3, Double_t &nTracks05_mu1, Double_t &nTracks05_mu2, Double_t &nTracks05_mu3, Double_t &sumPt03_mu1, Double_t &sumPt03_mu2, Double_t &sumPt03_mu3, Double_t &sumPt05_mu1, Double_t &sumPt05_mu2, Double_t &sumPt05_mu3, Double_t &hadVeto03, Double_t &hadVeto05, Double_t &emVeto03, Double_t &emVeto05, Double_t &trVeto03, Double_t &trVeto05, Double_t &EnMu1, Double_t &EnMu2, Double_t &EnMu3, Double_t &ChargeMu1, Double_t &ChargeMu2, Double_t &ChargeMu3, Double_t &isQValid1, Double_t &isTValid1, Double_t &isIsoValid1, Double_t &GLnormChi2_mu1, Double_t &GL_nValidMuHits1, Double_t &trkLayersWMeas1, Double_t &nValidPixelHits1, Double_t &outerTrk_P_1, Double_t &outerTrk_Eta_1, Double_t &outerTrk_normChi2_1, Double_t &outerTrk_muStValidHits_1, Double_t &innerTrk_P_1, Double_t &innerTrk_Eta_1, Double_t &innerTrk_normChi2_1, Double_t &QInnerOuter_1, Double_t &cQ_uS_1, Double_t &cQ_tK_1, Double_t &cQ_gK_1, Double_t &cQ_tRChi2_1, Double_t &cQ_sRChi2_1, Double_t &cQ_Chi2LP_1, Double_t &cQ_Chi2LM_1, Double_t &cQ_lD_1, Double_t &cQ_gDEP_1, Double_t &cQ_tM_1, Double_t &cQ_gTP_1, Double_t &segmComp_1, Double_t &caloComp_1, Double_t &isQValid2, Double_t &isTValid2, Double_t &isIsoValid2, Double_t &GLnormChi2_mu2, Double_t &GL_nValidMuHits2, Double_t &trkLayersWMeas2, Double_t &nValidPixelHits2, Double_t &outerTrk_P_2, Double_t &outerTrk_Eta_2, Double_t &outerTrk_normChi2_2, Double_t &outerTrk_muStValidHits_2, Double_t &innerTrk_P_2, Double_t &innerTrk_Eta_2, Double_t &innerTrk_normChi2_2, Double_t &QInnerOuter_2, Double_t &cQ_uS_2, Double_t &cQ_tK_2, Double_t &cQ_gK_2, Double_t &cQ_tRChi2_2, Double_t &cQ_sRChi2_2, Double_t &cQ_Chi2LP_2, Double_t &cQ_Chi2LM_2, Double_t &cQ_lD_2, Double_t &cQ_gDEP_2, Double_t &cQ_tM_2, Double_t &cQ_gTP_2, Double_t &segmComp_2, Double_t &caloComp_2, Double_t &isQValid3, Double_t &isTValid3, Double_t &isIsoValid3, Double_t &GLnormChi2_mu3, Double_t &GL_nValidMuHits3, Double_t &trkLayersWMeas3, Double_t &nValidPixelHits3, Double_t &outerTrk_P_3, Double_t &outerTrk_Eta_3, Double_t &outerTrk_normChi2_3, Double_t &outerTrk_muStValidHits_3, Double_t &innerTrk_P_3, Double_t &innerTrk_Eta_3, Double_t &innerTrk_normChi2_3, Double_t &QInnerOuter_3, Double_t &cQ_uS_3, Double_t &cQ_tK_3, Double_t &cQ_gK_3, Double_t &cQ_tRChi2_3, Double_t &cQ_sRChi2_3, Double_t &cQ_Chi2LP_3, Double_t &cQ_Chi2LM_3, Double_t &cQ_lD_3, Double_t &cQ_gDEP_3, Double_t &cQ_tM_3, Double_t &cQ_gTP_3, Double_t &segmComp_3, Double_t &caloComp_3, Double_t &dimu_OS1, Double_t &dimu_OS2, Double_t &match1_dX_1, Double_t &match1_pullX_1, Double_t &match1_pullDxDz_1, Double_t &match1_dY_1, Double_t &match1_pullY_1, Double_t &match1_pullDyDz_1, Double_t &match2_dX_1, Double_t &match2_pullX_1, Double_t &match2_pullDxDz_1, Double_t &match2_dY_1, Double_t &match2_pullY_1, Double_t &match2_pullDyDz_1, Double_t &match1_dX_2, Double_t &match1_pullX_2, Double_t &match1_pullDxDz_2, Double_t &match1_dY_2, Double_t &match1_pullY_2, Double_t &match1_pullDyDz_2, Double_t &match2_dX_2, Double_t &match2_pullX_2, Double_t &match2_pullDxDz_2, Double_t &match2_dY_2, Double_t &match2_pullY_2, Double_t &match2_pullDyDz_2, Double_t &match1_dX_3, Double_t &match1_pullX_3, Double_t &match1_pullDxDz_3, Double_t &match1_dY_3, Double_t &match1_pullY_3, Double_t &match1_pullDyDz_3, Double_t &match2_dX_3, Double_t &match2_pullX_3, Double_t &match2_pullDxDz_3, Double_t &match2_dY_3, Double_t &match2_pullY_3, Double_t &match2_pullDyDz_3, Double_t &innerTrk_highPurity_1, Double_t &innerTrk_highPurity_2, Double_t &innerTrk_highPurity_3, Double_t &innerTrk_ValidFraction_1, Double_t &innerTrk_ValidFraction_2, Double_t &innerTrk_ValidFraction_3, Double_t &nValidTrackerHits1, Double_t &nValidTrackerHits2, Double_t &nValidTrackerHits3, Double_t &validMuonHitComb1, Double_t &validMuonHitComb2, Double_t &validMuonHitComb3){
    // Fills the tree branches
    //cout << "Ciao1" << endl;
    // 2016 variables
    double pt[NMU] = {0}, eta[NMU] = {0}, phi[NMU] = {0};
    Get_MuonVariables(mu_Ind, pt, eta, phi); //fill vectors with kin. var. of the three muons
    Pmu3 = MuonP(Mu3_Pt->at(mu_Ind[2]), Mu3_Eta->at(mu_Ind[2]), Mu3_Phi->at(mu_Ind[2]));
    cLP = -999; tKink = -999; segmComp = 999; DeltaR_max = -999; DeltaZ_max = -999; 
    double temp1[NMU] = {0}, temp[NMU] = {0}, dR[NMU] = {0}, dZ[NMU] = {0};
    temp1[0] = dxy_mu1->at(mu_Ind[0]);
    temp1[1] = dxy_mu2->at(mu_Ind[1]);
    temp1[2] = dxy_mu3->at(mu_Ind[2]);
    dR[0] = deltaR(eta[0], eta[1], phi[0], phi[1]);
    dR[1] = deltaR(eta[0], eta[2], phi[0], phi[2]);
    dR[2] = deltaR(eta[1], eta[2], phi[1], phi[2]);
    dZ[0] = abs(Muon_vz->at(mu[0]) - Muon_vz->at(mu[1]));
    dZ[1] = abs(Muon_vz->at(mu[0]) - Muon_vz->at(mu[2]));
    dZ[2] = abs(Muon_vz->at(mu[2]) - Muon_vz->at(mu[1]));
    d0 = 999;
    temp[0] = abs(dxy_mu1->at(mu_Ind[0])/ dxyErr_mu1->at(mu_Ind[0]));
    temp[1] = abs(dxy_mu2->at(mu_Ind[1])/ dxyErr_mu2->at(mu_Ind[1]));
    temp[2] = abs(dxy_mu3->at(mu_Ind[2])/ dxyErr_mu3->at(mu_Ind[2]));
    d0sig = 999; d0sig_max = -999;
    //cout << "Ciao2" << endl;
    
    for (int k=0; k<NMU; k++){
        //  * cLP MAX
        //  * kink MAX
        //  * segmComp MIN
        //  * d0sig MIN
	//  * d0sig MAX
        //  * DeltaR MAX
        //  * DeltaZ MAX
        if (Muon_combinedQuality_chi2LocalPosition->at(mu[k]) > cLP) cLP = Muon_combinedQuality_chi2LocalPosition->at(mu[k]);
        if (Muon_combinedQuality_trkKink->at(mu[k]) > tKink) tKink = Muon_combinedQuality_trkKink->at(mu[k]);
        if (Muon_segmentCompatibility->at(mu[k]) < segmComp) segmComp = Muon_segmentCompatibility->at(mu[k]);
        if (temp1[k] < d0) d0 = temp1[k];
        if (temp[k] < d0sig) d0sig = temp[k];
	if (temp[k] > d0sig_max) d0sig_max = temp[k];
	if (dR[k] > DeltaR_max) DeltaR_max = dR[k];
	if (dZ[k] > DeltaZ_max) DeltaZ_max = dZ[k];
    }
  
    //cout << "Ciao3" << endl;
    
    if(isMC!=0) puFactor = nPileUpInt;
    else puFactor = pileupFactor;
    tripletMass = Triplet_Mass->at(ind);
    tripletMassReso = ResoTriplMass(mu_Ind, mu);
    if(tripletMassReso>0 && tripletMassReso<=0.007) category = 0;
    if(tripletMassReso>0.007 && tripletMassReso<=0.0105) category = 1;
    if(tripletMassReso>0.0105 && tripletMassReso<= 0.02) category = 2;
    if(tripletMassReso>0.02 || tripletMassReso<0) category = -99;
    
    fv_nC = TripletVtx_Chi2->at(ind)/3;
    fv_dphi3D = TreeFin_Angle(ind);
    fv_d3Dsig = FlightDistPVSV_Significance->at(ind);
    fv_d3D = FlightDistPVSV->at(ind);
    mindca_iso = Triplet_mindca_iso->at(ind);
    trkRel = Triplet_relativeiso->at(ind);
    
    //cout << "Ciao4" << endl;
    
    // Other variables
        // Single mu variables
    //cout << "Ciao5" << endl;
    Pmu1 = MuonP(Mu1_Pt->at(mu_Ind[0]), Mu1_Eta->at(mu_Ind[0]), Mu1_Phi->at(mu_Ind[0]));
    Ptmu1 = Mu1_Pt->at(mu_Ind[0]);
    etamu1 = Mu1_Eta->at(mu_Ind[0]);
    phimu1 = Mu1_Phi->at(mu_Ind[0]);
    Pmu2 = MuonP(Mu2_Pt->at(mu_Ind[1]), Mu2_Eta->at(mu_Ind[1]), Mu2_Phi->at(mu_Ind[1]));
    Ptmu2 = Mu2_Pt->at(mu_Ind[1]);
    etamu2 = Mu2_Eta->at(mu_Ind[1]);
    phimu2 = Mu2_Phi->at(mu_Ind[1]);
    Pmu3 = MuonP(Mu3_Pt->at(mu_Ind[2]), Mu3_Eta->at(mu_Ind[2]), Mu3_Phi->at(mu_Ind[2]));
    Ptmu3 = Mu3_Pt->at(mu_Ind[2]);
    etamu3 = Mu3_Eta->at(mu_Ind[2]);
    phimu3 = Mu3_Phi->at(mu_Ind[2]);
    dispMu1 = TMath::Sqrt(TMath::Power(BS_x->at(mu_Ind[0]) - Muon_vx->at(mu[0]),2) + TMath::Power(BS_y->at(mu_Ind[0]) - Muon_vy->at(mu[0]),2) + TMath::Power(BS_z->at(mu_Ind[0]) - Muon_vz->at(mu[0]),2));
    dispMu2 = TMath::Sqrt(TMath::Power(BS_x->at(mu_Ind[1]) - Muon_vx->at(mu[1]),2) + TMath::Power(BS_y->at(mu_Ind[1]) - Muon_vy->at(mu[1]),2) + TMath::Power(BS_z->at(mu_Ind[1]) - Muon_vz->at(mu[1]),2));
    dispMu3 = TMath::Sqrt(TMath::Power(BS_x->at(mu_Ind[2]) - Muon_vx->at(mu[2]),2) + TMath::Power(BS_y->at(mu_Ind[2]) - Muon_vy->at(mu[2]),2) + TMath::Power(BS_z->at(mu_Ind[2]) - Muon_vz->at(mu[1]),2));
    xydispMu1 = TMath::Sqrt(TMath::Power(BS_x->at(mu_Ind[0]) - Muon_vx->at(mu[0]),2) + TMath::Power(BS_y->at(mu_Ind[0]) - Muon_vy->at(mu[0]),2));
    xydispMu2 = TMath::Sqrt(TMath::Power(BS_x->at(mu_Ind[1]) - Muon_vx->at(mu[1]),2) + TMath::Power(BS_y->at(mu_Ind[1]) - Muon_vy->at(mu[1]),2));
    xydispMu3 = TMath::Sqrt(TMath::Power(BS_x->at(mu_Ind[2]) - Muon_vx->at(mu[2]),2) + TMath::Power(BS_y->at(mu_Ind[2]) - Muon_vy->at(mu[2]),2));
    //cout << "Ciao5_bis" << endl;
    nStationsMu1 = Muon_numberOfMatchedStations->at(mu[0]);
    nStationsMu2 = Muon_numberOfMatchedStations->at(mu[1]);
    nStationsMu3 = Muon_numberOfMatchedStations->at(mu[2]);
    //cout << "Ciao5_bis2" << endl;
    //Iso03Mu1 = Mu1_NTracks03iso->at(mu_Ind[0]);
    //Iso03Mu2 = Mu2_NTracks03iso->at(mu_Ind[1]);
    //Iso03Mu3 = Mu3_NTracks03iso->at(mu_Ind[2]);
    //Iso05Mu1 = Muon_emEt05->at(mu[0]);
    //Iso05Mu2 = Muon_emEt05->at(mu[1]);
    //Iso05Mu3 = Muon_emEt05->at(mu[2]);
    //cout << "Ciao5_bis3" << endl;
         // Triplet variables
    P_trip = MuonP(Triplet_Pt->at(ind), Triplet_Eta->at(ind), Triplet_Phi->at(ind));
    Pt_trip = Triplet_Pt->at(ind);
    eta_trip = Triplet_Eta->at(ind);
    //cout << "Ciao6" << endl;
        //
    nMatchesMu1 = Muon_numberOfMatches->at(mu[0]);
    nMatchesMu2 = Muon_numberOfMatches->at(mu[1]);
    nMatchesMu3 = Muon_numberOfMatches->at(mu[2]);
    timeAtIpInOut_sig1 = Muon_timeAtIpInOut->at(mu[0])/ Muon_timeAtIpInOutErr->at(mu[0]);
    timeAtIpInOut_sig2 = Muon_timeAtIpInOut->at(mu[1])/ Muon_timeAtIpInOutErr->at(mu[1]);
    timeAtIpInOut_sig3 = Muon_timeAtIpInOut->at(mu[2])/ Muon_timeAtIpInOutErr->at(mu[2]);
    cQ_uS = 0; cQ_tK = 0; cQ_gK = 0; cQ_tRChi2 = 0; cQ_sRChi2 = 0; cQ_Chi2LM = 0; cQ_Chi2LP = 0; cQ_lD = 0; cQ_gDEP = 0;
    cQ_tM = 0; cQ_gTP = 0; caloComp = 999;
    for (int k=0; k<NMU; k++){
        //  * cQ_* MAX
        if (Muon_combinedQuality_updatedSta->at(mu[k]) > cQ_uS) cQ_uS = Muon_combinedQuality_updatedSta->at(mu[k]);
        if (Muon_combinedQuality_trkKink->at(mu[k]) > cQ_tK) cQ_tK = Muon_combinedQuality_trkKink->at(mu[k]);
        if (Muon_combinedQuality_glbKink->at(mu[k]) > cQ_gK) cQ_gK = Muon_combinedQuality_glbKink->at(mu[k]);
        if (Muon_combinedQuality_trkRelChi2->at(mu[k]) > cQ_tRChi2) cQ_tRChi2 = Muon_combinedQuality_trkRelChi2->at(mu[k]);
        if (Muon_combinedQuality_staRelChi2->at(mu[k]) > cQ_sRChi2) cQ_sRChi2 = Muon_combinedQuality_staRelChi2->at(mu[k]);
        if (Muon_combinedQuality_chi2LocalPosition->at(mu[k]) > cQ_Chi2LP) cQ_Chi2LP = Muon_combinedQuality_chi2LocalPosition->at(mu[k]);
        if (Muon_combinedQuality_chi2LocalMomentum->at(mu[k]) > cQ_Chi2LM) cQ_Chi2LM = Muon_combinedQuality_chi2LocalMomentum->at(mu[k]);
        if (Muon_combinedQuality_localDistance->at(mu[k]) > cQ_lD) cQ_lD = Muon_combinedQuality_localDistance->at(mu[k]);
        if (Muon_combinedQuality_globalDeltaEtaPhi->at(mu[k]) > cQ_gDEP) cQ_gDEP = Muon_combinedQuality_globalDeltaEtaPhi->at(mu[k]);
        if (Muon_combinedQuality_tightMatch->at(mu[k]) > cQ_tM) cQ_tM = Muon_combinedQuality_tightMatch->at(mu[k]);
        if (Muon_combinedQuality_glbTrackProbability->at(mu[k]) > cQ_gTP) cQ_gTP = Muon_combinedQuality_glbTrackProbability->at(mu[k]);
        if (Muon_caloCompatibility->at(mu[k]) < caloComp) caloComp = Muon_caloCompatibility->at(mu[k]);
    }
    calEn_emMu1 = Muon_calEnergy_em->at(mu[0]);
    calEn_emMu2 = Muon_calEnergy_em->at(mu[1]);
    calEn_emMu3 = Muon_calEnergy_em->at(mu[2]);
    calEn_hadMu1 = Muon_calEnergy_had->at(mu[0]);
    calEn_hadMu2 = Muon_calEnergy_had->at(mu[1]);
    calEn_hadMu3 = Muon_calEnergy_had->at(mu[2]);
    //fliDistPVSV_Chi2 = FlightDistPVSV_chi2->at(ind);
    //cout << "Ciao7" << endl;
    nVtx = PVCollection_Size;
    //muon ID
    isGlb1 = Muon_isGlobal->at(mu[0]);
    MVA1 = Muon_isMVA->at(mu[0]);
    MVA2 = Muon_isMVA->at(mu[1]);
    MVA3 = Muon_isMVA->at(mu[2]);
    isMedium1 = Muon_isMedium->at(mu[0]);
    isMedium2 = Muon_isMedium->at(mu[1]);
    isMedium3 = Muon_isMedium->at(mu[2]);
    MVASoft1 = Muon_isMVASoft->at(mu[0]);
    MVASoft2 = Muon_isMVASoft->at(mu[1]);
    MVASoft3 = Muon_isMVASoft->at(mu[2]);
    isTracker1 = Muon_isTrackerMuon->at(mu[0]);
    isLoose1 = Muon_isLoose->at(mu[0]);
    isSoft1 = Muon_isSoft->at(mu[0]);
    isPF1 = Muon_isPF->at(mu[0]);
    isRPC1 = Muon_isRPCMuon->at(mu[0]);
    isSA1 = Muon_isStandAloneMuon->at(mu[0]);
    isCalo1 = Muon_isCaloMuon->at(mu[0]);
    isGlb2 = Muon_isGlobal->at(mu[1]);
    isTracker2 = Muon_isTrackerMuon->at(mu[1]);
    isLoose2 = Muon_isLoose->at(mu[1]);
    isSoft2 = Muon_isSoft->at(mu[1]);
    isPF2 = Muon_isPF->at(mu[1]);
    isRPC2 = Muon_isRPCMuon->at(mu[1]);
    isSA2 = Muon_isStandAloneMuon->at(mu[1]);
    isCalo2 = Muon_isCaloMuon->at(mu[1]);
    isGlb3 = Muon_isGlobal->at(mu[2]);
    isTracker3 = Muon_isTrackerMuon->at(mu[2]);
    isLoose3 = Muon_isLoose->at(mu[2]);
    isSoft3 = Muon_isSoft->at(mu[2]);
    isPF3 = Muon_isPF->at(mu[2]);
    isRPC3 = Muon_isRPCMuon->at(mu[2]);
    isSA3 = Muon_isStandAloneMuon->at(mu[2]);
    isCalo3 = Muon_isCaloMuon->at(mu[2]);
    //cout << "Ciao8" << endl;
    //
    Vx1 = Muon_vx->at(mu[0]);
    Vx2 = Muon_vx->at(mu[1]);
    Vx3 = Muon_vx->at(mu[2]);
    Vy1 = Muon_vy->at(mu[0]);
    Vy2 = Muon_vy->at(mu[1]);
    Vy3 = Muon_vy->at(mu[2]);
    Vz1 = Muon_vz->at(mu[0]);
    Vz2 = Muon_vz->at(mu[1]);
    Vz3 = Muon_vz->at(mu[2]);
    RefVx1 = RefittedPV_x->at(ind);
    RefVy1 = RefittedPV_y->at(ind);
    RefVz1 = RefittedPV_z->at(ind);
    SVx = TripletVtx_x->at(ind);
    SVy = TripletVtx_y->at(ind);
    SVz = TripletVtx_z->at(ind);
    had03 = Muon_hadEt03->at(mu[2]);
    had05 = Muon_hadEt05->at(mu[2]);
    nJets03 = Muon_nJets03->at(mu[2]);
    nJets05 = Muon_nJets05->at(mu[2]);
    nTracks03_mu1 = Muon_nTracks03->at(mu[0]);
    nTracks03_mu2 = Muon_nTracks03->at(mu[1]);
    nTracks03_mu3 = Muon_nTracks03->at(mu[2]);
    nTracks05_mu1 = Muon_nTracks05->at(mu[0]);
    nTracks05_mu2 = Muon_nTracks05->at(mu[1]);
    nTracks05_mu3 = Muon_nTracks05->at(mu[2]);
    sumPt03_mu1 = Muon_sumPt03->at(mu[0]);
    sumPt03_mu2 = Muon_sumPt03->at(mu[1]);
    sumPt03_mu3 = Muon_sumPt03->at(mu[2]);
    sumPt05_mu1 = Muon_sumPt05->at(mu[0]);
    sumPt05_mu2 = Muon_sumPt05->at(mu[1]);
    sumPt05_mu3 = Muon_sumPt05->at(mu[2]);
    hadVeto03 = Muon_hadVetoEt03->at(mu[2]);
    hadVeto05 = Muon_hadVetoEt05->at(mu[2]);
    emVeto03 = Muon_emVetoEt03->at(mu[2]);
    emVeto05 = Muon_emVetoEt05->at(mu[2]);
    trVeto03 = Muon_trackerVetoPt03->at(mu[2]);
    trVeto05 = Muon_trackerVetoPt05->at(mu[2]);
    //
    //cout << "Ciao9" << endl;
    //
    EnMu1 = MuonEnergy->at(mu[0]);
    EnMu2 = MuonEnergy->at(mu[1]);
    EnMu3 = MuonEnergy->at(mu[2]);
    ChargeMu1 = MuonCharge->at(mu[0]);
    ChargeMu2 = MuonCharge->at(mu[1]);
    ChargeMu3 = MuonCharge->at(mu[2]);
    //
    // mu1
    //cout << "Ciao10" << endl;
    isQValid1 = Muon_isQualityValid->at(mu[0]);
    isTValid1 = Muon_isTimeValid->at(mu[0]);
    isIsoValid1 = Muon_isIsolationValid->at(mu[0]);
    GLnormChi2_mu1 = Muon_GLnormChi2->at(mu[0]);
    GL_nValidMuHits1 = Muon_GLhitPattern_numberOfValidMuonHits->at(mu[0]);
    trkLayersWMeas1 = Muon_trackerLayersWithMeasurement->at(mu[0]);
    validMuonHitComb1 = Muon_validMuonHitComb->at(mu[0]);
    nValidTrackerHits1 = Muon_Numberofvalidtrackerhits->at(mu[0]);
    nValidPixelHits1 = Muon_Numberofvalidpixelhits->at(mu[0]);
    outerTrk_P_1 = Muon_outerTrack_p->at(mu[0]);
    outerTrk_Eta_1 = Muon_outerTrack_eta->at(mu[0]);
    outerTrk_normChi2_1 = Muon_outerTrack_normalizedChi2->at(mu[0]);
    outerTrk_muStValidHits_1 = Muon_outerTrack_muonStationsWithValidHits->at(mu[0]);
    innerTrk_P_1 = Muon_innerTrack_p->at(mu[0]);
    innerTrk_Eta_1 = Muon_innerTrack_eta->at(mu[0]);
    innerTrk_normChi2_1 = Muon_innerTrack_normalizedChi2->at(mu[0]);
    innerTrk_highPurity_1 = Muon_innerTrack_highPurity->at(mu[0]);
    innerTrk_ValidFraction_1 = Muon_innerTrack_ValidFraction->at(mu[0]);
    QInnerOuter_1 = Muon_QInnerOuter->at(mu[0]);
    cQ_uS_1 = Muon_combinedQuality_updatedSta->at(mu[0]);
    cQ_tK_1 = Muon_combinedQuality_trkKink->at(mu[0]);
    cQ_gK_1 = Muon_combinedQuality_glbKink->at(mu[0]);
    cQ_tRChi2_1 = Muon_combinedQuality_trkRelChi2->at(mu[0]);
    cQ_sRChi2_1 = Muon_combinedQuality_staRelChi2->at(mu[0]);
    cQ_Chi2LP_1 = Muon_combinedQuality_chi2LocalPosition->at(mu[0]);
    cQ_Chi2LM_1 = Muon_combinedQuality_chi2LocalMomentum->at(mu[0]);
    cQ_lD_1 = Muon_combinedQuality_localDistance->at(mu[0]);
    cQ_gDEP_1 = Muon_combinedQuality_globalDeltaEtaPhi->at(mu[0]);
    cQ_tM_1 = Muon_combinedQuality_tightMatch->at(mu[0]);
    cQ_gTP_1 = Muon_combinedQuality_glbTrackProbability->at(mu[0]);
    segmComp_1 = Muon_segmentCompatibility->at(mu[0]);
    caloComp_1 = Muon_caloCompatibility->at(mu[0]);
    match1_dX_1 = Muon_combinedQuality_match1_dX->at(mu[0]);
    match1_pullX_1 = Muon_combinedQuality_match1_pullX->at(mu[0]);
    match1_pullDxDz_1 = Muon_combinedQuality_match1_pullDxDz->at(mu[0]);
    match1_dY_1 = Muon_combinedQuality_match1_dY->at(mu[0]);
    match1_pullY_1 = Muon_combinedQuality_match1_pullY->at(mu[0]);
    match1_pullDyDz_1 = Muon_combinedQuality_match1_pullDyDz->at(mu[0]);
    match2_dX_1 = Muon_combinedQuality_match2_dX->at(mu[0]);
    match2_pullX_1 = Muon_combinedQuality_match2_pullX->at(mu[0]);
    match2_pullDxDz_1 = Muon_combinedQuality_match2_pullDxDz->at(mu[0]);
    match2_dY_1 = Muon_combinedQuality_match2_dY->at(mu[0]);
    match2_pullY_1 = Muon_combinedQuality_match2_pullY->at(mu[0]);
    match2_pullDyDz_1 = Muon_combinedQuality_match2_pullDyDz->at(mu[0]);
    //cout << "Ciao11" << endl;
    //
    // mu2
    isQValid2 = Muon_isQualityValid->at(mu[1]);
    isTValid2 = Muon_isTimeValid->at(mu[1]);
    isIsoValid2 = Muon_isIsolationValid->at(mu[1]);
    GLnormChi2_mu2 = Muon_GLnormChi2->at(mu[1]);
    GL_nValidMuHits2 = Muon_GLhitPattern_numberOfValidMuonHits->at(mu[1]);
    trkLayersWMeas2 = Muon_trackerLayersWithMeasurement->at(mu[1]);
    validMuonHitComb2 = Muon_validMuonHitComb->at(mu[1]);
    nValidTrackerHits2 = Muon_Numberofvalidtrackerhits->at(mu[1]);
    nValidPixelHits2 = Muon_Numberofvalidpixelhits->at(mu[1]);
    outerTrk_P_2 = Muon_outerTrack_p->at(mu[1]);
    outerTrk_Eta_2 = Muon_outerTrack_eta->at(mu[1]);
    outerTrk_normChi2_2 = Muon_outerTrack_normalizedChi2->at(mu[1]);
    outerTrk_muStValidHits_2 = Muon_outerTrack_muonStationsWithValidHits->at(mu[1]);
    innerTrk_P_2 = Muon_innerTrack_p->at(mu[1]);
    innerTrk_Eta_2 = Muon_innerTrack_eta->at(mu[1]);
    innerTrk_normChi2_2 = Muon_innerTrack_normalizedChi2->at(mu[1]);
    innerTrk_highPurity_2 = Muon_innerTrack_highPurity->at(mu[1]);
    innerTrk_ValidFraction_2 = Muon_innerTrack_ValidFraction->at(mu[1]);
    QInnerOuter_2 = Muon_QInnerOuter->at(mu[1]);
    cQ_uS_2 = Muon_combinedQuality_updatedSta->at(mu[1]);
    cQ_tK_2 = Muon_combinedQuality_trkKink->at(mu[1]);
    cQ_gK_2 = Muon_combinedQuality_glbKink->at(mu[1]);
    cQ_tRChi2_2 = Muon_combinedQuality_trkRelChi2->at(mu[1]);
    cQ_sRChi2_2 = Muon_combinedQuality_staRelChi2->at(mu[1]);
    cQ_Chi2LP_2 = Muon_combinedQuality_chi2LocalPosition->at(mu[1]);
    cQ_Chi2LM_2 = Muon_combinedQuality_chi2LocalMomentum->at(mu[1]);
    cQ_lD_2 = Muon_combinedQuality_localDistance->at(mu[1]);
    cQ_gDEP_2 = Muon_combinedQuality_globalDeltaEtaPhi->at(mu[1]);
    cQ_tM_2 = Muon_combinedQuality_tightMatch->at(mu[1]);
    cQ_gTP_2 = Muon_combinedQuality_glbTrackProbability->at(mu[1]);
    segmComp_2 = Muon_segmentCompatibility->at(mu[1]);
    caloComp_2 = Muon_caloCompatibility->at(mu[1]);
    match1_dX_2 = Muon_combinedQuality_match1_dX->at(mu[1]);
    match1_pullX_2 = Muon_combinedQuality_match1_pullX->at(mu[1]);
    match1_pullDxDz_2 = Muon_combinedQuality_match1_pullDxDz->at(mu[1]);
    match1_dY_2 = Muon_combinedQuality_match1_dY->at(mu[1]);
    match1_pullY_2 = Muon_combinedQuality_match1_pullY->at(mu[1]);
    match1_pullDyDz_2 = Muon_combinedQuality_match1_pullDyDz->at(mu[1]);
    match2_dX_2 = Muon_combinedQuality_match2_dX->at(mu[1]);
    match2_pullX_2 = Muon_combinedQuality_match2_pullX->at(mu[1]);
    match2_pullDxDz_2 = Muon_combinedQuality_match2_pullDxDz->at(mu[1]);
    match2_dY_2 = Muon_combinedQuality_match2_dY->at(mu[1]);
    match2_pullY_2 = Muon_combinedQuality_match2_pullY->at(mu[1]);
    match2_pullDyDz_2 = Muon_combinedQuality_match2_pullDyDz->at(mu[1]);
    //cout << "Ciao12" << endl;
    // mu3
    isQValid3 = Muon_isQualityValid->at(mu[2]);
    isTValid3 = Muon_isTimeValid->at(mu[2]);
    isIsoValid3 = Muon_isIsolationValid->at(mu[2]);
    GLnormChi2_mu3 = Muon_GLnormChi2->at(mu[2]);
    GL_nValidMuHits3 = Muon_GLhitPattern_numberOfValidMuonHits->at(mu[2]);
    trkLayersWMeas3 = Muon_trackerLayersWithMeasurement->at(mu[2]);
    validMuonHitComb3 = Muon_validMuonHitComb->at(mu[2]);
    nValidTrackerHits3 = Muon_Numberofvalidtrackerhits->at(mu[2]);
    nValidPixelHits3 = Muon_Numberofvalidpixelhits->at(mu[2]);
    outerTrk_P_3 = Muon_outerTrack_p->at(mu[2]);
    outerTrk_Eta_3 = Muon_outerTrack_eta->at(mu[2]);
    outerTrk_normChi2_3 = Muon_outerTrack_normalizedChi2->at(mu[2]);
    outerTrk_muStValidHits_3 = Muon_outerTrack_muonStationsWithValidHits->at(mu[2]);
    innerTrk_P_3 = Muon_innerTrack_p->at(mu[2]);
    innerTrk_Eta_3 = Muon_innerTrack_eta->at(mu[2]);
    innerTrk_normChi2_3 = Muon_innerTrack_normalizedChi2->at(mu[2]);
    innerTrk_highPurity_3 = Muon_innerTrack_highPurity->at(mu[2]);
    innerTrk_ValidFraction_3 = Muon_innerTrack_ValidFraction->at(mu[2]);
    QInnerOuter_3 = Muon_QInnerOuter->at(mu[2]);
    cQ_uS_3 = Muon_combinedQuality_updatedSta->at(mu[2]);
    cQ_tK_3 = Muon_combinedQuality_trkKink->at(mu[2]);
    cQ_gK_3 = Muon_combinedQuality_glbKink->at(mu[2]);
    cQ_tRChi2_3 = Muon_combinedQuality_trkRelChi2->at(mu[2]);
    cQ_sRChi2_3 = Muon_combinedQuality_staRelChi2->at(mu[2]);
    cQ_Chi2LP_3 = Muon_combinedQuality_chi2LocalPosition->at(mu[2]);
    cQ_Chi2LM_3 = Muon_combinedQuality_chi2LocalMomentum->at(mu[2]);
    cQ_lD_3 = Muon_combinedQuality_localDistance->at(mu[2]);
    cQ_gDEP_3 = Muon_combinedQuality_globalDeltaEtaPhi->at(mu[2]);
    cQ_tM_3 = Muon_combinedQuality_tightMatch->at(mu[2]);
    cQ_gTP_3 = Muon_combinedQuality_glbTrackProbability->at(mu[2]);
    segmComp_3 = Muon_segmentCompatibility->at(mu[2]);
    caloComp_3 = Muon_caloCompatibility->at(mu[2]);
    match1_dX_3 = Muon_combinedQuality_match1_dX->at(mu[2]);
    match1_pullX_3 = Muon_combinedQuality_match1_pullX->at(mu[2]);
    match1_pullDxDz_3 = Muon_combinedQuality_match1_pullDxDz->at(mu[2]);
    match1_dY_3 = Muon_combinedQuality_match1_dY->at(mu[2]);
    match1_pullY_3 = Muon_combinedQuality_match1_pullY->at(mu[2]);
    match1_pullDyDz_3 = Muon_combinedQuality_match1_pullDyDz->at(mu[2]);
    match2_dX_3 = Muon_combinedQuality_match2_dX->at(mu[2]);
    match2_pullX_3 = Muon_combinedQuality_match2_pullX->at(mu[2]);
    match2_pullDxDz_3 = Muon_combinedQuality_match2_pullDxDz->at(mu[2]);
    match2_dY_3 = Muon_combinedQuality_match2_dY->at(mu[2]);
    match2_pullY_3 = Muon_combinedQuality_match2_pullY->at(mu[2]);
    match2_pullDyDz_3 = Muon_combinedQuality_match2_pullDyDz->at(mu[2]);
    //cout << "Ciao13" << endl;
    double dimu12 = DimuonMass(mu[0], mu[1]);
    double dimu23 = DimuonMass(mu[1], mu[2]);
    double dimu13 = DimuonMass(mu[0], mu[2]);
    double dR_12 = deltaR(Mu1_Eta->at(mu_Ind[0]), Mu2_Eta->at(mu_Ind[1]), Mu1_Phi->at(mu_Ind[0]), Mu2_Phi->at(mu_Ind[1]));
    double dR_13 = deltaR(Mu1_Eta->at(mu_Ind[0]), Mu3_Eta->at(mu_Ind[2]), Mu1_Phi->at(mu_Ind[0]), Mu3_Phi->at(mu_Ind[2]));
    double dR_23 = deltaR(Mu2_Eta->at(mu_Ind[1]), Mu3_Eta->at(mu_Ind[2]), Mu2_Phi->at(mu_Ind[1]), Mu3_Phi->at(mu_Ind[2]));
    dimu_OS1 = 0;
    dimu_OS2 = 0;

    if(dimu12>0 && dimu23>0){ //2 pairs OS
        if(dR_12 < dR_23){
            dimu_OS1 = dimu12; dimu_OS2 = dimu23;
        }else{
            dimu_OS2 = dimu12; dimu_OS1 = dimu23;
        }
    }
    if(dimu12>0 && dimu13>0){ //2 pairs OS
        if(dR_12 < dR_13){
            dimu_OS1 = dimu12; dimu_OS2 = dimu13;
        }else{
            dimu_OS2 = dimu12; dimu_OS1 = dimu13;
        }
    }
    if(dimu13>0 && dimu23>0){ //2 pairs OS
        if(dR_13 < dR_23){
            dimu_OS1 = dimu13; dimu_OS2 = dimu23;
        }else{
            dimu_OS2 = dimu13; dimu_OS1 = dimu23;
        }
    }
    
    tree->Fill();
}

void myAnalizer::TreeFin_Init(TTree *&tree, Double_t &isMC, Double_t &lumi, Double_t &run, Double_t &evt, Double_t &puFactor, Double_t &category, Int_t &L1_DoubleMu0_er1p5, Int_t &L1_DoubleMu0_er1p4, Int_t &L1_DoubleMu4_dR1p2, Int_t &L1_DoubleMu4p5_dR1p2, Int_t &L1_DoubleMu0_er2p0, Int_t &L1_DoubleMu0_er2p0_bk, Int_t &L1_TripleMu_5SQ_3SQ_0, Int_t &L1_TripleMu_5SQ_3SQ_0OQ, Int_t &L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12, Int_t &L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12, Int_t &L1seed, Int_t &HLTpath, Double_t &DeltaR_max, Double_t &DeltaZ_max, Double_t &Pmu3, Double_t &cLP, Double_t &tKink, Double_t &segmComp, Double_t &tripletMass, Double_t &tripletMassReso, Double_t &fv_nC, Double_t &fv_dphi3D, Double_t &fv_d3D,  Double_t &fv_d3Dsig, Double_t &d0, Double_t &nVtx, Double_t &d0sig, Double_t &MVA1, Double_t &MVA2, Double_t &MVA3, Double_t &MVASoft1, Double_t &MVASoft2, Double_t &MVASoft3,  Double_t &d0sig_max, Double_t &mindca_iso, Double_t &trkRel, Double_t &Pmu1, Double_t &Ptmu1, Double_t &etamu1, Double_t &phimu1, Double_t &Pmu2, Double_t &Ptmu2, Double_t &etamu2, Double_t &phimu2, Double_t &Ptmu3, Double_t &etamu3, Double_t &phimu3, Double_t &dispMu1, Double_t &dispMu2, Double_t &dispMu3, Double_t &xydispMu1, Double_t &xydispMu2, Double_t &xydispMu3, Double_t &P_trip, Double_t &Pt_trip, Double_t &eta_trip, Double_t &nStationsMu1, Double_t &nStationsMu2, Double_t &nStationsMu3, Double_t &Iso03Mu1, Double_t &Iso03Mu2, Double_t &Iso03Mu3, Double_t &Iso05Mu1, Double_t &Iso05Mu2, Double_t &Iso05Mu3, Double_t &nMatchesMu1, Double_t &nMatchesMu2, Double_t &nMatchesMu3, Double_t &timeAtIpInOut_sig1, Double_t &timeAtIpInOut_sig2, Double_t &timeAtIpInOut_sig3, Double_t &cQ_uS, Double_t &cQ_tK, Double_t &cQ_gK, Double_t &cQ_tRChi2, Double_t &cQ_sRChi2, Double_t &cQ_Chi2LP, Double_t &cQ_Chi2LM, Double_t &cQ_lD, Double_t &cQ_gDEP, Double_t &cQ_tM, Double_t &cQ_gTP, Double_t &calEn_emMu1, Double_t &calEn_emMu2, Double_t &calEn_emMu3, Double_t &calEn_hadMu1, Double_t &calEn_hadMu2, Double_t &calEn_hadMu3, Double_t &caloComp, Double_t &fliDistPVSV_Chi2, Double_t &isMedium1, Double_t &isMedium2, Double_t &isMedium3, Double_t &isGlb1, Double_t &isTracker1, Double_t &isLoose1, Double_t &isSoft1, Double_t &isPF1, Double_t &isRPC1, Double_t &isSA1, Double_t &isCalo1, Double_t &isGlb2, Double_t &isTracker2, Double_t &isLoose2, Double_t &isSoft2, Double_t &isPF2, Double_t &isRPC2, Double_t &isSA2, Double_t &isCalo2, Double_t &isGlb3, Double_t &isTracker3, Double_t &isLoose3, Double_t &isSoft3, Double_t &isPF3, Double_t &isRPC3, Double_t &isSA3, Double_t &isCalo3, Double_t &Vx1, Double_t &Vx2, Double_t &Vx3, Double_t &Vy1, Double_t &Vy2, Double_t &Vy3, Double_t &Vz1, Double_t &Vz2, Double_t &Vz3, Double_t &RefVx1, Double_t &RefVx2, Double_t &RefVx3, Double_t &RefVy1, Double_t &RefVy2, Double_t &RefVy3, Double_t &RefVz1, Double_t &RefVz2, Double_t &RefVz3, Double_t &SVx, Double_t &SVy, Double_t &SVz, Double_t &had03, Double_t &had05, Double_t &nJets03, Double_t &nJets05, Double_t &nTracks03_mu1, Double_t &nTracks03_mu2, Double_t &nTracks03_mu3, Double_t &nTracks05_mu1, Double_t &nTracks05_mu2, Double_t &nTracks05_mu3, Double_t &sumPt03_mu1, Double_t &sumPt03_mu2, Double_t &sumPt03_mu3, Double_t &sumPt05_mu1, Double_t &sumPt05_mu2, Double_t &sumPt05_mu3, Double_t &hadVeto03, Double_t &hadVeto05, Double_t &emVeto03, Double_t &emVeto05, Double_t &trVeto03, Double_t &trVeto05, Double_t &EnMu1, Double_t &EnMu2, Double_t &EnMu3, Double_t &ChargeMu1, Double_t &ChargeMu2, Double_t &ChargeMu3, Double_t &isQValid1, Double_t &isTValid1, Double_t &isIsoValid1, Double_t &GLnormChi2_mu1, Double_t &GL_nValidMuHits1, Double_t &trkLayersWMeas1, Double_t &nValidPixelHits1, Double_t &outerTrk_P_1, Double_t &outerTrk_Eta_1, Double_t &outerTrk_normChi2_1, Double_t &outerTrk_muStValidHits_1, Double_t &innerTrk_P_1, Double_t &innerTrk_Eta_1, Double_t &innerTrk_normChi2_1, Double_t &QInnerOuter_1, Double_t &cQ_uS_1, Double_t &cQ_tK_1, Double_t &cQ_gK_1, Double_t &cQ_tRChi2_1, Double_t &cQ_sRChi2_1, Double_t &cQ_Chi2LP_1, Double_t &cQ_Chi2LM_1, Double_t &cQ_lD_1, Double_t &cQ_gDEP_1, Double_t &cQ_tM_1, Double_t &cQ_gTP_1, Double_t &segmComp_1, Double_t &caloComp_1, Double_t &isQValid2, Double_t &isTValid2, Double_t &isIsoValid2, Double_t &GLnormChi2_mu2, Double_t &GL_nValidMuHits2, Double_t &trkLayersWMeas2, Double_t &nValidPixelHits2, Double_t &outerTrk_P_2, Double_t &outerTrk_Eta_2, Double_t &outerTrk_normChi2_2, Double_t &outerTrk_muStValidHits_2, Double_t &innerTrk_P_2, Double_t &innerTrk_Eta_2, Double_t &innerTrk_normChi2_2, Double_t &QInnerOuter_2, Double_t &cQ_uS_2, Double_t &cQ_tK_2, Double_t &cQ_gK_2, Double_t &cQ_tRChi2_2, Double_t &cQ_sRChi2_2, Double_t &cQ_Chi2LP_2, Double_t &cQ_Chi2LM_2, Double_t &cQ_lD_2, Double_t &cQ_gDEP_2, Double_t &cQ_tM_2, Double_t &cQ_gTP_2, Double_t &segmComp_2, Double_t &caloComp_2, Double_t &isQValid3, Double_t &isTValid3, Double_t &isIsoValid3, Double_t &GLnormChi2_mu3, Double_t &GL_nValidMuHits3, Double_t &trkLayersWMeas3, Double_t &nValidPixelHits3, Double_t &outerTrk_P_3, Double_t &outerTrk_Eta_3, Double_t &outerTrk_normChi2_3, Double_t &outerTrk_muStValidHits_3, Double_t &innerTrk_P_3, Double_t &innerTrk_Eta_3, Double_t &innerTrk_normChi2_3, Double_t &QInnerOuter_3, Double_t &cQ_uS_3, Double_t &cQ_tK_3, Double_t &cQ_gK_3, Double_t &cQ_tRChi2_3, Double_t &cQ_sRChi2_3, Double_t &cQ_Chi2LP_3, Double_t &cQ_Chi2LM_3, Double_t &cQ_lD_3, Double_t &cQ_gDEP_3, Double_t &cQ_tM_3, Double_t &cQ_gTP_3, Double_t &segmComp_3, Double_t &caloComp_3, Double_t &dimu_OS1, Double_t &dimu_OS2, Double_t &match1_dX_1, Double_t &match1_pullX_1, Double_t &match1_pullDxDz_1, Double_t &match1_dY_1, Double_t &match1_pullY_1, Double_t &match1_pullDyDz_1, Double_t &match2_dX_1, Double_t &match2_pullX_1, Double_t &match2_pullDxDz_1, Double_t &match2_dY_1, Double_t &match2_pullY_1, Double_t &match2_pullDyDz_1, Double_t &match1_dX_2, Double_t &match1_pullX_2, Double_t &match1_pullDxDz_2, Double_t &match1_dY_2, Double_t &match1_pullY_2, Double_t &match1_pullDyDz_2, Double_t &match2_dX_2, Double_t &match2_pullX_2, Double_t &match2_pullDxDz_2, Double_t &match2_dY_2, Double_t &match2_pullY_2, Double_t &match2_pullDyDz_2, Double_t &match1_dX_3, Double_t &match1_pullX_3, Double_t &match1_pullDxDz_3, Double_t &match1_dY_3, Double_t &match1_pullY_3, Double_t &match1_pullDyDz_3, Double_t &match2_dX_3, Double_t &match2_pullX_3, Double_t &match2_pullDxDz_3, Double_t &match2_dY_3, Double_t &match2_pullY_3, Double_t &match2_pullDyDz_3, Double_t &innerTrk_highPurity_1, Double_t &innerTrk_highPurity_2, Double_t &innerTrk_highPurity_3, Double_t &innerTrk_ValidFraction_1, Double_t &innerTrk_ValidFraction_2, Double_t &innerTrk_ValidFraction_3, Double_t &nValidTrackerHits1, Double_t &nValidTrackerHits2, Double_t &nValidTrackerHits3, Double_t &validMuonHitComb1, Double_t &validMuonHitComb2, Double_t &validMuonHitComb3){
    // Set tree branches
    tree->Branch("isMC", &isMC);
    tree->Branch("lumi", &lumi);
    tree->Branch("run", &run);
    tree->Branch("evt", &evt);
    tree->Branch("puFactor", &puFactor);
    tree->Branch("category", &category);
    tree->Branch("L1_DoubleMu0_er1p5", &L1_DoubleMu0_er1p5);
    tree->Branch("L1_DoubleMu0_er1p4", &L1_DoubleMu0_er1p4);
    tree->Branch("L1_DoubleMu4_dR1p2", &L1_DoubleMu4_dR1p2);
    tree->Branch("L1_DoubleMu4p5_dR1p2", &L1_DoubleMu4p5_dR1p2);
    tree->Branch("L1_DoubleMu0_er2p0", &L1_DoubleMu0_er2p0);
    tree->Branch("L1_DoubleMu0_er2p0_bk", &L1_DoubleMu0_er2p0_bk);
    tree->Branch("L1_TripleMu_5SQ_3SQ_0", &L1_TripleMu_5SQ_3SQ_0);
    tree->Branch("L1_TripleMu_5SQ_3SQ_0OQ", &L1_TripleMu_5SQ_3SQ_0OQ);
    tree->Branch("L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12", &L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12);
    tree->Branch("L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12", &L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12);
    tree->Branch("L1seed", &L1seed);
    tree->Branch("HLTpath", &HLTpath);
    tree->Branch("DeltaR_max", &DeltaR_max);
    tree->Branch("DeltaZ_max", &DeltaZ_max);
    tree->Branch("Pmu3", &Pmu3);
    tree->Branch("cLP", &cLP);
    tree->Branch("tKink", &tKink);
    tree->Branch("segmComp", &segmComp);
    tree->Branch("tripletMass", &tripletMass);
    tree->Branch("tripletMassReso", &tripletMassReso);
    tree->Branch("fv_nC", &fv_nC);
    tree->Branch("fv_dphi3D", &fv_dphi3D);
    tree->Branch("fv_d3D", &fv_d3D);
    tree->Branch("fv_d3Dsig", &fv_d3Dsig);
    tree->Branch("d0", &d0);
    tree->Branch("nVtx", &nVtx);
    tree->Branch("d0sig", &d0sig);
    tree->Branch("d0sig_max", &d0sig_max);
    tree->Branch("mindca_iso", &mindca_iso);
    tree->Branch("trkRel", &trkRel);
    tree->Branch("Pmu1", &Pmu1);
    tree->Branch("Ptmu1", &Ptmu1);
    tree->Branch("Etamu1", &etamu1);
    tree->Branch("Phimu1", &phimu1);
    tree->Branch("Pmu2", &Pmu2);
    tree->Branch("Ptmu2", &Ptmu2);
    tree->Branch("Etamu2", &etamu2);
    tree->Branch("Phimu2", &phimu2);
    tree->Branch("Ptmu3", &Ptmu3);
    tree->Branch("Etamu3", &etamu3);
    tree->Branch("Phimu3", &phimu3);

    tree->Branch("dispMu1", &dispMu1);
    tree->Branch("dispMu2", &dispMu2);
    tree->Branch("dispMu3", &dispMu3);
    tree->Branch("xydispMu1", &xydispMu1);
    tree->Branch("xydispMu2", &xydispMu2);
    tree->Branch("xydispMu3", &xydispMu3);

    tree->Branch("P_tripl", &P_trip);
    tree->Branch("Pt_tripl", &Pt_trip);
    tree->Branch("Eta_tripl", &eta_trip);
    tree->Branch("nStMu1", &nStationsMu1);
    tree->Branch("nStMu2", &nStationsMu2);
    tree->Branch("nStMu3", &nStationsMu3);
    tree->Branch("Iso03Mu1", &Iso03Mu1);
    tree->Branch("Iso03Mu2", &Iso03Mu2);
    tree->Branch("Iso03Mu3", &Iso03Mu3);
    tree->Branch("Iso05Mu1", &Iso05Mu1);
    tree->Branch("Iso05Mu2", &Iso05Mu2);
    tree->Branch("Iso05Mu3", &Iso05Mu3);
    tree->Branch("nMatchesMu1", &nMatchesMu1);
    tree->Branch("nMatchesMu2", &nMatchesMu2);
    tree->Branch("nMatchesMu3", &nMatchesMu3);
    tree->Branch("timeAtIpInOut_sig1", &timeAtIpInOut_sig1);
    tree->Branch("timeAtIpInOut_sig2", &timeAtIpInOut_sig2);
    tree->Branch("timeAtIpInOut_sig3", &timeAtIpInOut_sig3);
    tree->Branch("cQ_uS", &cQ_uS);
    tree->Branch("cQ_tK", &cQ_tK);
    tree->Branch("cQ_gK", &cQ_gK);
    tree->Branch("cQ_tRChi2", &cQ_tRChi2);
    tree->Branch("cQ_sRChi2", &cQ_sRChi2);
    tree->Branch("cQ_Chi2LP", &cQ_Chi2LP);
    tree->Branch("cQ_Chi2LM", &cQ_Chi2LM);
    tree->Branch("cQ_lD", &cQ_lD);
    tree->Branch("cQ_gDEP", &cQ_gDEP);
    tree->Branch("cQ_tM", &cQ_tM);
    tree->Branch("cQ_gTP", &cQ_gTP);
    tree->Branch("calEn_emMu1", &calEn_emMu1);
    tree->Branch("calEn_emMu2", &calEn_emMu2);
    tree->Branch("calEn_emMu3", &calEn_emMu3);
    tree->Branch("calEn_hadMu1", &calEn_hadMu1);
    tree->Branch("calEn_hadMu2", &calEn_hadMu2);
    tree->Branch("calEn_hadMu3", &calEn_hadMu3);
    tree->Branch("caloComp", &caloComp);
    tree->Branch("fliDistPVSV_Chi2", &fliDistPVSV_Chi2);
    tree->Branch("isGlb1", &isGlb1);
    tree->Branch("isMedium1", &isMedium1);
    tree->Branch("isMedium2", &isMedium2);
    tree->Branch("isMedium3", &isMedium3);
    tree->Branch("MVA1", &MVA1);
    tree->Branch("MVA2", &MVA2);
    tree->Branch("MVA3", &MVA3);
    tree->Branch("MVASoft1", &MVASoft1);
    tree->Branch("MVASoft2", &MVASoft2);
    tree->Branch("MVASoft3", &MVASoft3);
    tree->Branch("isTracker1", &isTracker1);
    tree->Branch("isLoose1", &isLoose1);
    tree->Branch("isSoft1", &isSoft1);
    tree->Branch("isPF1", &isPF1);
    tree->Branch("isRPC1", &isRPC1);
    tree->Branch("isSA1", &isSA1);
    tree->Branch("isCalo1", &isCalo1);
    tree->Branch("isGlb2", &isGlb2);
    tree->Branch("isTracker2", &isTracker2);
    tree->Branch("isLoose2", &isLoose2);
    tree->Branch("isSoft2", &isSoft2);
    tree->Branch("isPF2", &isPF2);
    tree->Branch("isRPC2", &isRPC2);
    tree->Branch("isSA2", &isSA2);
    tree->Branch("isCalo2", &isCalo2);
    tree->Branch("isGlb3", &isGlb3);
    tree->Branch("isTracker3", &isTracker3);
    tree->Branch("isLoose3", &isLoose3);
    tree->Branch("isSoft3", &isSoft3);
    tree->Branch("isPF3", &isPF3);
    tree->Branch("isRPC3", &isRPC3);
    tree->Branch("isSA3", &isSA3);
    tree->Branch("isCalo3", &isCalo3);
    tree->Branch("Vx1", &Vx1);
    tree->Branch("Vx2", &Vx2);
    tree->Branch("Vx3", &Vx3);
    tree->Branch("Vy1", &Vy1);
    tree->Branch("Vy2", &Vy2);
    tree->Branch("Vy3", &Vy3);
    tree->Branch("Vz1", &Vz1);
    tree->Branch("Vz2", &Vz2);
    tree->Branch("Vz3", &Vz3);
    tree->Branch("RefVx1", &RefVx1);
    tree->Branch("RefVx2", &RefVx2);
    tree->Branch("RefVx3", &RefVx3);
    tree->Branch("RefVy1", &RefVy1);
    tree->Branch("RefVy2", &RefVy2);
    tree->Branch("RefVy3", &RefVy3);
    tree->Branch("RefVz1", &RefVz1);
    tree->Branch("RefVz2", &RefVz2);
    tree->Branch("RefVz3", &RefVz3);
    tree->Branch("SVx", &SVx);
    tree->Branch("SVy", &SVy);
    tree->Branch("SVz", &SVz);
    tree->Branch("had03", &had03);
    tree->Branch("had05", &had05);
    tree->Branch("nJets03", &nJets03);
    tree->Branch("nJets05", &nJets05);
    tree->Branch("nTracks03_mu1", &nTracks03_mu1);
    tree->Branch("nTracks03_mu2", &nTracks03_mu2);
    tree->Branch("nTracks03_mu3", &nTracks03_mu3);
    tree->Branch("nTracks05_mu1", &nTracks05_mu1);
    tree->Branch("nTracks05_mu2", &nTracks05_mu2);
    tree->Branch("nTracks05_mu3", &nTracks05_mu3);
    tree->Branch("sumPt03_mu1", &sumPt03_mu1);
    tree->Branch("sumPt03_mu2", &sumPt03_mu2);
    tree->Branch("sumPt03_mu3", &sumPt03_mu3);
    tree->Branch("sumPt05_mu1", &sumPt05_mu1);
    tree->Branch("sumPt05_mu2", &sumPt05_mu2);
    tree->Branch("sumPt05_mu3", &sumPt05_mu3);
    tree->Branch("hadVeto03", &hadVeto03);
    tree->Branch("hadVeto05", &hadVeto05);
    tree->Branch("emVeto03", &emVeto03);
    tree->Branch("emVeto05", &emVeto05);
    tree->Branch("trVeto03", &trVeto03);
    tree->Branch("trVeto05", &trVeto05);
    
    // new branches
    tree->Branch("EnMu1", &EnMu1);
    tree->Branch("EnMu2", &EnMu2);
    tree->Branch("EnMu3", &EnMu3);
    tree->Branch("ChargeMu1", &ChargeMu1);
    tree->Branch("ChargeMu2", &ChargeMu2);
    tree->Branch("ChargeMu3", &ChargeMu3);
    // Mu1
    tree->Branch("isQValid1", &isQValid1);
    tree->Branch("isTValid1", &isTValid1);
    tree->Branch("isIsoValid1", &isIsoValid1);
    tree->Branch("GLnormChi2_mu1", &GLnormChi2_mu1);
    tree->Branch("GL_nValidMuHits1", &GL_nValidMuHits1);
    tree->Branch("trkLayersWMeas1", &trkLayersWMeas1);
    tree->Branch("validMuonHitComb1", &validMuonHitComb1);
    tree->Branch("nValidTrackerHits1", &nValidTrackerHits1);
    tree->Branch("nValidPixelHits1", &nValidPixelHits1);
    tree->Branch("outerTrk_P_1", &outerTrk_P_1);
    tree->Branch("outerTrk_Eta_1", &outerTrk_Eta_1);
    tree->Branch("outerTrk_normChi2_1", &outerTrk_normChi2_1);
    tree->Branch("outerTrk_muStValidHits_1", &outerTrk_muStValidHits_1);
    tree->Branch("innerTrk_P_1", &innerTrk_P_1);
    tree->Branch("innerTrk_Eta_1", &innerTrk_Eta_1);
    tree->Branch("innerTrk_normChi2_1", &innerTrk_normChi2_1);
    tree->Branch("innerTrk_highPurity_1", &innerTrk_highPurity_1);
    tree->Branch("innerTrk_ValidFraction_1", &innerTrk_ValidFraction_1);
    tree->Branch("QInnerOuter_1", &QInnerOuter_1);
    tree->Branch("cQ_uS_1", &cQ_uS_1);
    tree->Branch("cQ_tK_1", &cQ_tK_1);
    tree->Branch("cQ_gK_1", &cQ_gK_1);
    tree->Branch("cQ_tRChi2_1", &cQ_tRChi2_1);
    tree->Branch("cQ_sRChi2_1", &cQ_sRChi2_1);
    tree->Branch("cQ_Chi2LP_1", &cQ_Chi2LP_1);
    tree->Branch("cQ_Chi2LM_1", &cQ_Chi2LM_1);
    tree->Branch("cQ_lD_1", &cQ_lD_1);
    tree->Branch("cQ_gDEP_1", &cQ_gDEP_1);
    tree->Branch("cQ_tM_1", &cQ_tM_1);
    tree->Branch("cQ_gTP_1", &cQ_gTP_1);
    tree->Branch("segmComp_1", &segmComp_1);
    tree->Branch("caloComp_1", &caloComp_1);
    tree->Branch("match1_dX_1", &match1_dX_1);
    tree->Branch("match1_pullX_1", &match1_pullX_1);
    tree->Branch("match1_pullDxDz_1", &match1_pullDxDz_1);
    tree->Branch("match1_dY_1", &match1_dY_1);
    tree->Branch("match1_pullY_1", &match1_pullY_1);
    tree->Branch("match1_pullDyDz_1", &match1_pullDyDz_1);
    tree->Branch("match2_dX_1", &match2_dX_1);
    tree->Branch("match2_pullX_1", &match2_pullX_1);
    tree->Branch("match2_pullDxDz_1", &match2_pullDxDz_1);
    tree->Branch("match2_dY_1", &match2_dY_1);
    tree->Branch("match2_pullY_1", &match2_pullY_1);
    tree->Branch("match2_pullDyDz_1", &match2_pullDyDz_1);
    // Mu2
    tree->Branch("isQValid2", &isQValid2);
    tree->Branch("isTValid2", &isTValid2);
    tree->Branch("isIsoValid2", &isIsoValid2);
    tree->Branch("GLnormChi2_mu2", &GLnormChi2_mu2);
    tree->Branch("GL_nValidMuHits2", &GL_nValidMuHits2);
    tree->Branch("trkLayersWMeas2", &trkLayersWMeas2);
    tree->Branch("validMuonHitComb2", &validMuonHitComb2);
    tree->Branch("nValidTrackerHits2", &nValidTrackerHits2);
    tree->Branch("nValidPixelHits2", &nValidPixelHits2);
    tree->Branch("outerTrk_P_2", &outerTrk_P_2);
    tree->Branch("outerTrk_Eta_2", &outerTrk_Eta_2);
    tree->Branch("outerTrk_normChi2_2", &outerTrk_normChi2_2);
    tree->Branch("outerTrk_muStValidHits_2", &outerTrk_muStValidHits_2);
    tree->Branch("innerTrk_P_2", &innerTrk_P_2);
    tree->Branch("innerTrk_Eta_2", &innerTrk_Eta_2);
    tree->Branch("innerTrk_normChi2_2", &innerTrk_normChi2_2);
    tree->Branch("innerTrk_highPurity_2", &innerTrk_highPurity_2);
    tree->Branch("innerTrk_ValidFraction_2", &innerTrk_ValidFraction_2);
    tree->Branch("QInnerOuter_2", &QInnerOuter_2);
    tree->Branch("cQ_uS_2", &cQ_uS_2);
    tree->Branch("cQ_tK_2", &cQ_tK_2);
    tree->Branch("cQ_gK_2", &cQ_gK_2);
    tree->Branch("cQ_tRChi2_2", &cQ_tRChi2_2);
    tree->Branch("cQ_sRChi2_2", &cQ_sRChi2_2);
    tree->Branch("cQ_Chi2LP_2", &cQ_Chi2LP_2);
    tree->Branch("cQ_Chi2LM_2", &cQ_Chi2LM_2);
    tree->Branch("cQ_lD_2", &cQ_lD_2);
    tree->Branch("cQ_gDEP_2", &cQ_gDEP_2);
    tree->Branch("cQ_tM_2", &cQ_tM_2);
    tree->Branch("cQ_gTP_2", &cQ_gTP_2);
    tree->Branch("segmComp_2", &segmComp_2);
    tree->Branch("caloComp_2", &caloComp_2);
    tree->Branch("match1_dX_2", &match1_dX_2);
    tree->Branch("match1_pullX_2", &match1_pullX_2);
    tree->Branch("match1_pullDxDz_2", &match1_pullDxDz_2);
    tree->Branch("match1_dY_2", &match1_dY_2);
    tree->Branch("match1_pullY_2", &match1_pullY_2);
    tree->Branch("match1_pullDyDz_2", &match1_pullDyDz_2);
    tree->Branch("match2_dX_2", &match2_dX_2);
    tree->Branch("match2_pullX_2", &match2_pullX_2);
    tree->Branch("match2_pullDxDz_2", &match2_pullDxDz_2);
    tree->Branch("match2_dY_2", &match2_dY_2);
    tree->Branch("match2_pullY_2", &match2_pullY_2);
    tree->Branch("match2_pullDyDz_2", &match2_pullDyDz_2);
    // Mu3
    tree->Branch("isQValid3", &isQValid3);
    tree->Branch("isTValid3", &isTValid3);
    tree->Branch("isIsoValid3", &isIsoValid3);
    tree->Branch("GLnormChi2_mu3", &GLnormChi2_mu3);
    tree->Branch("GL_nValidMuHits3", &GL_nValidMuHits3);
    tree->Branch("trkLayersWMeas3", &trkLayersWMeas3);
    tree->Branch("validMuonHitComb3", &validMuonHitComb3);
    tree->Branch("nValidTrackerHits3", &nValidTrackerHits3);
    tree->Branch("nValidPixelHits3", &nValidPixelHits3);
    tree->Branch("outerTrk_P_3", &outerTrk_P_3);
    tree->Branch("outerTrk_Eta_3", &outerTrk_Eta_3);
    tree->Branch("outerTrk_normChi2_3", &outerTrk_normChi2_3);
    tree->Branch("outerTrk_muStValidHits_3", &outerTrk_muStValidHits_3);
    tree->Branch("innerTrk_P_3", &innerTrk_P_3);
    tree->Branch("innerTrk_Eta_3", &innerTrk_Eta_3);
    tree->Branch("innerTrk_normChi2_3", &innerTrk_normChi2_3);
    tree->Branch("innerTrk_highPurity_3", &innerTrk_highPurity_3);
    tree->Branch("innerTrk_ValidFraction_3", &innerTrk_ValidFraction_3);
    tree->Branch("QInnerOuter_3", &QInnerOuter_3);
    tree->Branch("cQ_uS_3", &cQ_uS_3);
    tree->Branch("cQ_tK_3", &cQ_tK_3);
    tree->Branch("cQ_gK_3", &cQ_gK_3);
    tree->Branch("cQ_tRChi2_3", &cQ_tRChi2_3);
    tree->Branch("cQ_sRChi2_3", &cQ_sRChi2_3);
    tree->Branch("cQ_Chi2LP_3", &cQ_Chi2LP_3);
    tree->Branch("cQ_Chi2LM_3", &cQ_Chi2LM_3);
    tree->Branch("cQ_lD_3", &cQ_lD_3);
    tree->Branch("cQ_gDEP_3", &cQ_gDEP_3);
    tree->Branch("cQ_tM_3", &cQ_tM_3);
    tree->Branch("cQ_gTP_3", &cQ_gTP_3);
    tree->Branch("segmComp_3", &segmComp_3);
    tree->Branch("caloComp_3", &caloComp_3);
    tree->Branch("match1_dX_3", &match1_dX_3);
    tree->Branch("match1_pullX_3", &match1_pullX_3);
    tree->Branch("match1_pullDxDz_3", &match1_pullDxDz_3);
    tree->Branch("match1_dY_3", &match1_dY_3);
    tree->Branch("match1_pullY_3", &match1_pullY_3);
    tree->Branch("match1_pullDyDz_3", &match1_pullDyDz_3);
    tree->Branch("match2_dX_3", &match2_dX_3);
    tree->Branch("match2_pullX_3", &match2_pullX_3);
    tree->Branch("match2_pullDxDz_3", &match2_pullDxDz_3);
    tree->Branch("match2_dY_3", &match2_dY_3);
    tree->Branch("match2_pullY_3", &match2_pullY_3);
    tree->Branch("match2_pullDyDz_3", &match2_pullDyDz_3);
    // other
    tree->Branch("dimu_OS1", &dimu_OS1);
    tree->Branch("dimu_OS2", &dimu_OS2);
    
}
/*
void myAnalizer::InitMVA( TString pathToWeight ){

    reader = new TMVA::Reader( "!Color:!Silent" );

    reader->TMVA::Reader::AddVariable( "Pmu3", &forBDTevaluation1 );
    reader->TMVA::Reader::AddVariable( "cLP", &forBDTevaluation2 );
    reader->TMVA::Reader::AddVariable( "tKink", &forBDTevaluation3 );
    reader->TMVA::Reader::AddVariable( "segmComp", &forBDTevaluation4 );
    reader->TMVA::Reader::AddVariable( "fv_nC", &forBDTevaluation5 );
    reader->TMVA::Reader::AddVariable( "fv_dphi3D", &forBDTevaluation6 );
    reader->TMVA::Reader::AddVariable( "fv_d3Dsig", &forBDTevaluation7 );
    reader->TMVA::Reader::AddVariable( "d0sig", &forBDTevaluation8 );
    reader->TMVA::Reader::AddVariable( "mindca_iso", &forBDTevaluation9 );
    reader->TMVA::Reader::AddSpectator( "tripletMass", &forBDTevaluation10 );    
//reader->TMVA::Reader::AddVariable( "trkRel", &forBDTevaluation10 );

    reader->TMVA::Reader::BookMVA( methodName, pathToWeight );
}

float myAnalizer::EvaluateMVA( Float_t Pmu3, Float_t cLP, Float_t tKink, Float_t segmComp, Float_t fv_nC, Float_t fv_dphi3D, Float_t fv_d3Dsig, Float_t d0sig, Float_t mindca_iso, Float_t tripletMass ){

    forBDTevaluation1 = Pmu3;
    forBDTevaluation2 = cLP;
    forBDTevaluation3 = tKink;
    forBDTevaluation4 = segmComp;
    forBDTevaluation5 = fv_nC;
    forBDTevaluation6 = fv_dphi3D;
    forBDTevaluation7 = fv_d3Dsig;
    forBDTevaluation8 = d0sig;
    forBDTevaluation9 = mindca_iso;
    forBDTevaluation10 = tripletMass;
    //forBDTevaluation10 = trkRel;

return reader->TMVA::Reader::EvaluateMVA( methodName );
}*/
