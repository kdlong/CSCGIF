{ 
  const unsigned int NN0 = 7;
  short unsigned int N0[NN0][3]; 
  const unsigned int NN1 = 8;
  short unsigned int N1[NN1][2]; 

  double * time[NN1][2]; // max{NN0, NN1}
  double * I[NN1][2];

  double time100V_0 [3] = {2,5,10};
  double I_100V_0   [3] = {5.645, 5.2266, 5.0174};
  time[0][0] = time100V_0;
  I[0][0]  = I_100V_0;
  N0[0][0] = 3;
  N0[0][1] = 100;

  double time100V_1 [6] = {3, 6, 10, 14, 23, 30};
  double I_100V_1   [6] = {7.0048, 6.3772, 6.168, 5.9588, 5.7496, 5.645};
  time[0][1] = time100V_1;
  I[0][1]  = I_100V_1;
  N1[0][0] = 6;
  N1[0][1] = 100;

  double time200V_0 [4] = {2, 6, 14, 20};
  double I_200V_0   [4] = {10.5612, 6.3772, 5.8542, 5.7496};
  time[1][0] = time200V_0;
  I[1][0]  = I_200V_0;
  N0[1][0] = 4;
  N0[1][1] = 200;

  double time200V_1 [3] = {9, 15, 28};
  double I_200V_1   [3] = {6.9002, 6.4818, 6.2726};
  time[1][1] = time200V_1;
  I[1][1]  = I_200V_1;
  N1[1][0] = 3;
  N1[1][1] = 200;

  double time300V_1 [5] = {8, 10, 14, 17, 26};
  double I_300V_1   [5] = {7.6324, 7.4232, 7.214, 7.1094, 6.9002};
  time[2][1] = time300V_1;
  I[2][1]  = I_300V_1;
  N1[2][0] = 5;
  N1[2][1] = 300;

  double time350V_0 [5] = {2, 5, 8, 14, 17};
  double I_350V_0   [5] = {8.68, 7.74, 7.63, 7.00, 7.00};
  time[2][0] = time350V_0;
  I[2][0]  = I_350V_0;
  N0[2][0] = 5;
  N0[2][1] = 350;
 
  double time400V_1 [6] = {5, 10, 13, 17, 20, 28};
  double I_400V_1   [6] = {8.8876, 8.26, 8.1554, 7.9462, 7.8416, 7.737};
  time[3][1] = time400V_1;
  I[3][1]  = I_400V_1;
  N1[3][0] = 6;
  N1[3][1] = 400;


  double time450V_0 [5] = {4, 8, 12, 24, 30};
  double I_450V_0   [5] = {9.10, 8.47, 8.26, 7.95, 7.84};
  time[3][0] = time450V_0;
  I[3][0]  = I_450V_0;
  N0[3][0] = 4;
  N0[3][1] = 450;


  double time500V_1[6] = {3, 6, 12, 18, 20, 24};
  double I_500V_1  [6] = {10.5612, 9.7244, 9.2014, 9.0968, 8.9922, 8.8876};
  time[4][1] = time500V_1;
  I[4][1]  = I_500V_1;
  N1[4][0] = 6;
  N1[4][1] = 500;

  double time550V_0 [4] = {6, 11, 18, 25};
  double I_550V_0   [4] = {10.14, 9.72, 9.41, 9.31};
  time[4][0] = time550V_0;
  I[4][0]  = I_550V_0;
  N0[4][0] = 4;
  N0[4][1] = 550;

  double time600V_1[5] = {5, 9, 16, 21, 26};
  double I_600V_1  [5] = {11.8164, 11.0842, 10.6658, 10.4566, 10.352};
  time[5][1] = time600V_1;
  I[5][1]  = I_600V_1;
  N1[5][0] = 5;
  N1[5][1] = 600;

  double time650V_0[3] = {  14, 20, 30};
  double I_650V_0  [3] = {  11.50, 11.19, 11.08};
  time[5][0] = time650V_0;
  I[5][0]  = I_650V_0;
  N0[5][0] = 3;
  N0[5][1] = 650;

  double time700V_1[4] = {10, 14, 18, 27};
  double I_700V_1  [4] = {13.0716, 12.8624, 12.6532, 12.3394};
  time[6][1] = time700V_1;
  I[6][1]  = I_700V_1;
  N1[6][0] = 4;
  N1[6][1] = 700;

  double time800V_0[4] = {5, 10, 15, 23};
  double I_800V_0  [4] = {17.46, 16.00, 15.58, 15.37};
  time[6][0] = time800V_0;
  I[6][0]  = I_800V_0;
  N0[6][0] = 4;
  N0[6][1] = 800;
  
  double time800V_1[5] = {7, 10, 17, 21, 27};
  double I_800V_1  [5] = {16.5234, 16.0004, 15.6866, 15.4774, 15.2682};
  time[7][1] = time800V_1;
  I[7][1]  = I_800V_1;
  N1[7][0] = 5;
  N1[7][1] = 800;



  TGraphErrors * gr[NN1][2];
  TF1          * fu[NN1][2];
  for(unsigned int i=0;i<NN0; i++){
    TString name  = "gr["; name+=i; name+="]["; name+=0; name+="]";
    TString title = name+="; HV="; title+=N0[i][1]; title+=" V";
    gr[i][0] = new TGraphErrors(N0[i][0]);
    std::cout << title << " " << N0[i][0] << std::endl;
    for(unsigned int j=0; j<N0[i][0]; j++){
      std::cout << time[i][0][j] << "\t" << I[i][0][j] << std::endl;
      gr[i][0]->SetPoint     (j, time[i][0][j], I[i][0][j]);
      gr[i][0]->SetPointError(j, 1,             0.1);
      gr[i][0]->SetMarkerColor(1);
      gr[i][0]->SetLineColor(1);
      gr[i][0]->SetMarkerStyle(20);
    };
    name  = "fu["; name+=i; name+="]["; name+=0; name+="]";
    fu[i][0] = new TF1(name,"[0]+[1]*exp([2]*x)",0,16);
    fu[i][0]->SetLineColor(2);
  };

  std::cout << "=====" << std::endl;
  for(unsigned int i=0;i<NN1; i++){
    TString name  = "gr["; name+=i; name+="]["; name+=1; name+="]";
    TString title = name+="; HV="; title+=N1[i][1]; title+=" V";
    gr[i][1] = new TGraphErrors(N1[i][0]);
    std::cout << N1[i][0] << std::endl;
    for(unsigned int j=0; j<N1[i][0]; j++){
      std::cout << time[i][1][j] << "\t" << I[i][1][j] << std::endl;
      gr[i][1]->SetPoint     (j, time[i][1][j], I[i][1][j]);
      gr[i][1]->SetPointError(j, 1,             0.1);
      gr[i][1]->SetMarkerColor(4);
      gr[i][1]->SetLineColor(4);
      gr[i][1]->SetMarkerStyle(20);
    };
    name  = "fu["; name+=i; name+="]["; name+=1; name+="]";
    fu[i][1] = new TF1(name,"[0]+[1]*exp([2]*x)",0,16);
    fu[i][1]->SetLineColor(2);
  }

  
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);
  TH2F *hax[NN1];
  TCanvas *c[NN1];
  
  unsigned int coinA[NN0];
  unsigned int coinN = 0;
  //  for(unsigned int i=0;i<4; i++){
  for(unsigned int i=0;i<NN1; i++){
    TString name  = "hax["; name+=i; name+="]";
    hax[i] = new TH2F(name,";time [min];I [nA]", 30, 0, 40, 200, 0, 20);
    name   = "c["; name+=i; name+="]";
    TString title = "HV="; title+=N1[i][1]; title+=" V";
    c[i] = new TCanvas(name, title, 600,600);
    hax[i]->Draw();
    gr[i][1]->Draw("Psames");
    fu[i][1]->SetParameter(0,I[i][1][N1[i][0]-1]);
    fu[i][1]->SetParameter(1,2);
    fu[i][1]->SetParameter(2,-0.1);
    gr[i][1]->Fit(fu[i][1],"R");
    bool found = false;
    unsigned int i0    = 0;
    if(coinN>0)
      i0=coinA[coinN-1];
    //    std::cout << i << " " << i0 << " " << coinN << " " << std::endl;
    while( (i0<NN0) && !(found) ){
      // std::cout << i << " " << i0 << "\t" << N1[i][1] << "  " << N0[i0][1] << std::endl;     
      if( N0[i0][1]==N1[i][1] ){
    //std::cout << "we're here\n";
    gr[i0][0]->Draw("Psames");
    fu[i0][0]->SetParameter(0,I[i0][0][N0[i0][0]-1]);
    fu[i0][0]->SetParameter(1,2);
    fu[i0][0]->SetParameter(2,-0.1);
    gr[i0][0]->Fit(fu[i0][0],"R");
    coinA[coinN++] = i0;
    found = true;
    };
     i0++;
    };
  };
  
  
  /////////////////////////////////////////////////////////////
  // plot measurements0 which are different from measurements1
  TCanvas *c0  [NN0-coinN];
  TH2F    *hax0[NN0-coinN];
  unsigned int i0 = 0;
  for(unsigned int i=0;i<NN0; i++){
    bool exists = false;
    unsigned int coini = 0;
    while ( (coini<coinN) && (exists==false) ){
      if(i==coinA[coini])
    exists = true;
      coini++;
    };
    if(!exists){
      TString name  = "hax0["; name+=i0; name+="]";
      hax0[i0] = new TH2F(name,";time [min];I [nA]", 30, 0, 40, 200, 0, 20);
      name          =   "c0["; name+=i0; name+="]";
      TString title = "HV="; title+=N0[i][1]; title+=" V";
      c0[i0] = new TCanvas(name, title, 600,600);
      hax0[i0]->Draw();
      gr[i][0]->Draw("Psames");
      fu[i][0]->SetParameter(0,I[i][0][N0[i][0]-1]);
      fu[i][0]->SetParameter(1,2);
      fu[i][0]->SetParameter(2,-0.1);   
      gr[i][0]->Fit(fu[i][0],"R");     
      i0++;
    };
  };
  /////////////////////////////////////////////////////////////  
  TGraphErrors * meas0m = new TGraphErrors(NN0+4);
  TGraphErrors * meas0f = new TGraphErrors(NN0);
  TGraphErrors * meas1m = new TGraphErrors(NN1);
  TGraphErrors * meas1f = new TGraphErrors(NN1);
  TLatex       * time0m[N0];
  TLatex       * time1m[N1];

  double firstPointsHV[4] = {10,   25,   50,   75};
  double firstPointsI [4] = {3.13, 3.76, 4.39, 4.70};

  TCanvas * cc = new TCanvas ("cc","cc", 800, 720);
  TH2F  * hhax = new TH2F("hhax","ME11 L5 10.02.16;HV [V];I [nA]", 100, 0, 1000, 200, 0, 20);
  hhax->Draw();
  for(unsigned int i=0;i<NN1; i++){
    printf("%4d %4d %6.2f \t\t", N1[i][1],  time[i][1][N1[i][0]-1], I[i][1][N1[i][0]-1]);
    printf("%8.2f +/- %8.2f\t\t", fu[i][1]->GetParameter(0), fu[i][1]->GetParError(0));
    for(unsigned int ipar=1; ipar<3; ipar++){
      printf("%8.2f   ", fu[i][1]->GetParameter(ipar));
    };std::cout << std::endl;
    meas1m->SetPoint     (i, N1[i][1], I[i][1][N1[i][0]-1]);
    meas1m->SetPointError(i, 0,        0.1);
    meas1m->SetMarkerColor(1);
    meas1m->SetLineColor(1);
    meas1m->SetMarkerStyle(20);
    meas1f->SetPoint     (i, N1[i][1], fu[i][1]->GetParameter(0));
    meas1f->SetPointError(i, 0,        fu[i][1]->GetParError(0));
    meas1f->SetMarkerColor(kGray+2);
    meas1f->SetLineColor(kGray+2);
    meas1f->SetMarkerStyle(20);
    TString str = ""; str+=time[i][1][N1[i][0]-1];
    time1m[i] = new TLatex(N1[i][1]-10, I[i][1][N1[i][0]-1]+1,str.Data());
    time1m[i]->SetTextSize(0.02);
  };
  std::cout << "----------------------" << std::endl;
  for(unsigned int i=0;i<NN0; i++){
    printf("%4d %4d %6.2f\t\t", N0[i][1], time[i][0][N0[i][0]-1], I[i][0][N0[i][0]-1]);
    printf("%8.2f +/- %8.2f\t\t", fu[i][0]->GetParameter(0), fu[i][0]->GetParError(0));
    for(unsigned int ipar=1; ipar<3; ipar++){
      printf("%8.2f   ", fu[i][0]->GetParameter(ipar));
    };std::cout << std::endl;
    meas0m->SetPoint     (i+4, N0[i][1], I[i][0][N0[i][0]-1]);
    meas0m->SetPointError(i+4, 0,        0.1);
    meas0m->SetMarkerColor(2);
    meas0m->SetLineColor(2);
    meas0m->SetMarkerStyle(20);
    meas0f->SetPoint     (i, N0[i][1], fu[i][0]->GetParameter(0));
    meas0f->SetPointError(i, 0,        fu[i][0]->GetParError(0));
    meas0f->SetMarkerColor(kOrange+2);
    meas0f->SetLineColor(kOrange+2);
    meas0f->SetMarkerStyle(20);
    TString str = ""; str+=time[i][0][N0[i][0]-1];
    time0m[i] = new TLatex(N0[i][1]-10, I[i][0][N0[i][0]-1]-1,str.Data());
    time0m[i]->SetTextSize(0.02);
  };
  for(unsigned int i=0;i<4; i++){
    meas0m->SetPoint     (i, firstPointsHV[i], firstPointsI[i]);
    meas0m->SetPointError(i, 0,        0.1);
  };

  // remove fits with 2 points only for fit
  meas1f->RemovePoint(1);  
  meas1f->RemovePoint(6-1); 
  meas1f->RemovePoint(7-2); 
  meas0f->RemovePoint(4);  
  meas0f->RemovePoint(5-1); 

  meas0m->Draw("Psames");
  meas0f->Draw("Psames");
  meas1m->Draw("Psames");
  meas1f->Draw("Psames");
  for(unsigned int i=0;i<NN1; i++)
    time1m[i]->Draw();
  for(unsigned int i=0;i<NN0; i++)
    time0m[i]->Draw();
  double meanI200 = (I[1][1][N1[1][0]-1]+I[0][1][N0[1][0]-1])/2;
  TString str200;
  str200.Form("<I(200V)> = %6.2f nA; #DeltaI(200V)/<I(200V)> = %6.2f",meanI200, (I[1][1][N1[1][0]-1]-I[0][1][N0[1][0]-1])/meanI200);
  std::cout << str200 << std::endl;
  TLatex * latex200 = new TLatex(150, 3, str200.Data());
  latex200->SetTextSize(0.03);
  latex200->Draw();
  
  TLegend *l = new TLegend(0.15,0.65,0.48,0.85);
  l->AddEntry(meas0m,   "last points, set#0, e(I)=0.1 nA","ep");
  l->AddEntry(meas0f,   "fits, set#0 && time #leq 15min","ep");
  l->AddEntry(meas1m,   "last points, set#1, e(I)=0.1 nA","ep");
  l->AddEntry(meas1f,   "fits, set#1 && time #leq 15min","ep");
  l->Draw();
  
  

  double HVcaen200uA[9]   = {1200, 1500, 2000, 2300,  2500,  2600,  2700,   2750,   2800};
  double Icaen200uA[9]    = {20,   120,  1840, 10520, 34280, 61080, 106220, 138000, 177000};
  double Icaen200uAerr[9];
  double HVcaen200uAcorr[9];

  double HVcaen1mA[7]     = {2000, 2300,  2500,  2700,   2800,   2850,   2900};
  double Icaen1mA[7]      = {1700, 10400, 34200, 106300, 177300, 224100, 278900};
  double Icaen1mAerr[7]; 
  double Icaen1mAdelta[7];
  double Icaen1mAdeltaerr[7];
  double HVcaen1mAcorr[7];

  const double dHVME11ave = 0.000104;
   
  const double alphaME11aL5    = 0.00545;
  const double alphaME11bL5    = 0.00590;
  const double alphaME11aL5err = 0.00003;
  const double alphaME11bL5err = 0.00003;
  const double ME11abAreas[2]  = {0.27, 0.73};
  double alphaME11L5    = alphaME11aL5*ME11abAreas[0]+alphaME11bL5*ME11abAreas[1];
  double alphaME11L5err = TMath::Sqrt(alphaME11aL5err*alphaME11aL5err*ME11abAreas[0]*ME11abAreas[0]+alphaME11bL5err*alphaME11bL5err*ME11abAreas[1]*ME11abAreas[1]);
  std::cout << "average slope " << alphaME11L5 << " +/- " << alphaME11L5err << std::endl;
  for(unsigned int i=0; i<9; i++){
    HVcaen200uAcorr[i] = HVcaen200uA[i]-Icaen200uA[i]*dHVME11ave;
    Icaen200uAerr[i]   = 20;
    printf("%8.1f %8.1f %8.1f\n", HVcaen200uA[i], HVcaen200uAcorr[i], Icaen200uA[i]);
  };
  for(unsigned int i=0; i<7; i++){
    HVcaen1mAcorr[i] = HVcaen1mA[i]-Icaen1mA[i]*dHVME11ave;
    Icaen1mAerr[i] = 100;
    printf("%8.1f %8.1f %8.1f\n", HVcaen1mA[i], HVcaen1mAcorr[i], Icaen1mA[i]);
  };
  TGraphErrors * gr200uA = new TGraphErrors(9, HVcaen200uAcorr, Icaen200uA, 0, Icaen200uAerr);
  gr200uA->SetMarkerColor(4);
  gr200uA->SetLineColor(4);
  gr200uA->SetMarkerStyle(20);

  TGraphErrors * gr1mA   = new TGraphErrors(7, HVcaen1mAcorr,   Icaen1mA,   0, Icaen1mAerr);
  gr1mA->SetMarkerColor(kCyan+1);
  gr1mA->SetLineColor(kCyan+1);
  gr1mA->SetMarkerStyle(20);

  TCanvas * cc1 = new TCanvas ("cc1","cc1", 800, 720); 
  TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0); 
  TPad *pad2 = new TPad("pad2", "pad2", 0, 0.0, 1, 0.3);

  pad1->Draw();
  pad1->cd();
  pad1->SetLogy(); 
  pad1->SetGridx(); pad1->SetGridy();  
  TH2F  * hhax1 = new TH2F("hhax1","ME11 L5 10.02.16;HV [V]; I [nA]",600, 0, 3000, 400000, 0, 400000);
  hhax1->Draw();
  meas1m->Draw("Psames");
  gr200uA->Draw("Psames");
  gr1mA->Draw("Psames");  
  TF1 * f1mA   = new TF1("f1mA","exp([0]+[1]*x)",1900, 2750);   
  TF1 * f1mAex = new TF1("f1mAex","exp([0]+[1]*x)",500, 3000);
  f1mAex->SetLineStyle(3);
  //  f1mA->SetParameter(0,5);
  //  f1mA->FixParameter(0,5);
  //  f1mA->SetParLimits(0,0,10);
  f1mA->SetParameter(0,1);
  f1mA->SetParameter(1,0.005);
  TFitResultPtr r = gr1mA->Fit(f1mA,"SR");
  //Icaen1mAdeltaerr - error on the fitfunction for x=HVcaen1mAcorr
  r->GetConfidenceIntervals(7, 1, 1, HVcaen1mAcorr, Icaen1mAdeltaerr, 0.683, true);
  for(unsigned int i=0; i<3; i++){
    f1mAex->SetParameter(i, f1mA->GetParameter(i));
  };
  f1mAex->Draw("sames");

  pad1->Update(); 
  TPaveStats *pt1 = (TPaveStats*)(pad1->GetPrimitive("stats"));
  pt1->SetX1NDC(0.2);
  pt1->SetX2NDC(0.5);
  pt1->SetY1NDC(0.45);
  pt1->SetY2NDC(0.6);
  pad1->Modified();
  pad1->Update(); 
  for(unsigned int i=0; i<7; i++){
    double fitfunc      = f1mAex->Eval(HVcaen1mAcorr[i]);
    Icaen1mAdelta[i]    = (Icaen1mA[i]-fitfunc)/fitfunc;
    double tmp          = Icaen1mAdeltaerr[i]*Icaen1mA[i]/fitfunc;
    Icaen1mAdeltaerr[i] = TMath::Sqrt(Icaen1mAerr[i]*Icaen1mAerr[i]+tmp*tmp)/fitfunc;
    printf("%8.1f %8.1f %8.3f %8.3f\n",  HVcaen1mAcorr[i], Icaen1mA[i], Icaen1mAdelta[i], Icaen1mAdeltaerr[i]);
  };
  TLegend *l = new TLegend(0.2,0.6,0.5,0.85);
  l->AddEntry(meas1m,  "pAmeter, set#1","p");
  l->AddEntry(gr200uA, "CAEN 200uA, corrected","ep");
  l->AddEntry(gr1mA,   "CAEN   1mA, corrected","ep");
  l->AddEntry(f1mA,    "fit CAEN 1mA","l");
  l->AddEntry(f1mAex,  "extrapolation fit CAEN 1mA","l");
  l->Draw();
  TString str2880;
  double HV2880[1]={2880}; double err2880[1]={0};
  r->GetConfidenceIntervals(7, 1, 1, HV2880, err2880, 0.683, true);
  str2880.Form("fit(2880V) = %6.2e #pm %6.2e nA",f1mAex->Eval(HV2880[0]), err2880[0]);
  std::cout << str2880 << std::endl;
  TLatex * latex2880 = new TLatex(1500, 10, str2880.Data());
  latex2880->SetTextSize(0.04);
  latex2880->Draw();




        
  cc1->cd();
  pad2->SetBottomMargin(0.2);
  pad2->SetTopMargin(0.2);
  pad2->SetGridx(); pad2->SetGridy();
  pad2->Draw();
  pad2->cd();
  TGraphErrors * gr1mAdelta   = new TGraphErrors(7, HVcaen1mAcorr,   Icaen1mAdelta,   0, Icaen1mAdeltaerr);
  TH2F  * hhax2 = new TH2F("hhax2","[I_{i}-fit(HV_{i}^{corr})]/fit(HV_{i}^{corr});HV [V]; I [nA]",600, 0, 3000, 300, -0.2, 0.1);
  hhax2->Draw();
  pad2->Update(); 
  TPaveText *pt2 = (TPaveText*)(pad2->GetPrimitive("title"));
  pt2->SetTextSize(0.1);
  pad2->Modified(); 
  hhax2->GetXaxis()->SetLabelSize(0.09);//hhax2->GetXaxis()->SetNdivisions(505);
  hhax2->GetXaxis()->SetTitleSize(0.09); hhax2->GetXaxis()->SetTitleOffset(1.0);
  hhax2->GetYaxis()->SetLabelSize(0.09);hhax2->GetYaxis()->SetNdivisions(505);
  hhax2->GetYaxis()->SetTitleSize(0.09); hhax2->GetYaxis()->SetTitleOffset(0.5);
  gr1mAdelta->SetMarkerColor(kCyan+1);
  gr1mAdelta->SetLineColor(kCyan+1);
  gr1mAdelta->SetMarkerStyle(20);
  gr1mAdelta->SetFillColor(kCyan+1);
  gr1mAdelta->SetFillStyle(3002);  
  gr1mAdelta->Draw("3PL");
}
