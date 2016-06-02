import ROOT
import os
from Utilities import OutputTools
import Utilities.config_attributes as attributes
from IPython import embed

class IVCurve(object):
    def __init__(self, data):
        self.data = data
        self.config_info = data.getConfigInfo()
        self.stat_coords = [0, 0, 0.2, 0.2]
    def getCurve(self, output_dir):
        voltages = self.data.getEntries().keys()
        self.final_curve = ROOT.TGraphErrors(len(voltages))
        name = self.data.getName()
        self.final_curve.SetName("_".join([name, "final"])) 
        self.final_curve.SetTitle(name if "NAME" not in self.config_info.keys() else \
            self.config_info["NAME"]
        )
        for i, point in enumerate(self.data.getRawData(output_dir)):
            self.final_curve.SetPoint(i, point[0], point[1])
            self.final_curve.SetPointError(i, 0, point[2]) 
        if "FIT_FUNCTION" in self.config_info.keys():
            extrema = [float(x) for x in self.config_info["FIT_RANGE"]] \
                if "FIT_RANGE" in self.config_info else [voltages[0], voltages[1]]
            self.fit_func = ROOT.TF1("-".join([name, "fit"]),
                self.config_info["FIT_FUNCTION"],
                extrema[0], extrema[1]
            )
            self.fit_func.SetParameter(0,1)
            self.fit_func.SetParameter(1,0.005)
            self.final_curve.Fit(self.fit_func, "SR")
            if "EXTEND_FIT" in self.config_info:
                extend = self.fit_func.Clone()
                extend.SetName(extend.GetName().replace("fit", "extendedfit"))
                extend.SetRange(*[float(x) for x in self.config_info["EXTEND_FIT"]])
                extend.SetLineStyle(7)
                self.final_curve.GetListOfFunctions().Add(extend)
            ROOT.gROOT.FindObject("final").Update() 
        self.final_curve.GetXaxis().SetTitle("Applied Voltage (V)")
        self.final_curve.GetYaxis().SetTitle("Current (nA)")
        self.final_curve.SetMinimum(0.1)
        self.final_curve.SetMaximum(max([v["stable current"] \
            for v in self.data.getEntries().values()]))
        self.final_curve.SetMarkerStyle(20)
        self.final_curve.SetMarkerSize(1)
        if "COLOR" in self.config_info:
            attributes.setAttributes(self.final_curve, 
                {"SetLineColor" : self.config_info["COLOR"],
                "SetMarkerColor" : self.config_info["COLOR"]}
            )
        ROOT.SetOwnership(self.final_curve, False)
        return self.final_curve
    def getFitText(self):
        if "FIT_FUNCTION" not in self.config_info.keys():
            return 0
        height = 0.1 if not "EVALUATE_FIT_AT" in self.config_info else 0.1
#        ymax = min(self.stat_coords[1], self.stat_coords[3])
#        fit_text = ROOT.TPaveText(self.stat_coords[0], ymax-height,
#                self.stat_coords[2], ymax, "NDCnb")
        fit_text = ROOT.TPaveText(0.60, 0.4, 0.90, 0.4+height, "NDCnb")
        fit_text.SetFillColor(0)
        fit_text.SetName(self.final_curve.GetName().replace("final", "fittext"))
        fit_text.AddText("Fit function: %s" % self.config_info["FIT_FUNCTION"])
        if "EVALUATE_FIT_AT" in self.config_info:
            curr_point = float(self.config_info["EVALUATE_FIT_AT"])
            result = self.fit_func.Eval(curr_point)
            fit_text.AddText("I(%i) = %0.2f #muA" % (int(curr_point), round(result/1000, 2)))
        ROOT.SetOwnership(fit_text, False)
        return fit_text
    def setStatCoords(self, x1, y1, x2, y2):
        self.stat_coords = [x1, y1, x2, y2]
        stat_box = self.final_curve.GetListOfFunctions().FindObject("stats")
        stat_box.SetX1NDC(x1)
        stat_box.SetX2NDC(x2)
        stat_box.SetY1NDC(y1)
        stat_box.SetY2NDC(y2)
    def getStatBox(self):
        #print self.final_curve.GetListOfFunctions().FindObject("stats")
        return self.final_curve.GetListOfFunctions().FindObject("stats")
