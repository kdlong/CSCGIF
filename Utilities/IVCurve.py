import ROOT
import os
import OutputTools
from IPython import embed

class IVCurve(object):
    def __init__(self, data_file_name):
        self.config_info = {}
        self.data_file = data_file_name
        self.entries = self.readDataFromFile(data_file_name)
        self.stat_coords = [0, 0, 0.2, 0.2]
    def readDataFromFile(self, data_file_name):
        file_info = []
        with open(self.data_file) as data_file:
            time = lambda x: float(x) if ":" not in x else \
                (60*float(x.split(":")[0]) + float(x.split(":")[1]))
            for line in data_file:
                if line[0] in ["#"]:
                    continue
                elif "=" in line:
                    (key, value) = line.split("=")
                    self.config_info[key.strip().upper()] = value.strip() \
                        if ";" not in value else \
                            [x.strip() for x in value.split(";")]
                    continue
                data = line.split()
                if len(data) < 3:
                    continue
                file_info.append([time(x) for x in data])
            entries = {x : 
                {"currents" : [],
                    "times": [],
                    "errors" : [],
                "stable current" : 0,
                "stable error" : 0
                }
                for x in set([i[0] for i in file_info if len(i) > 0])
            }
        for entry in file_info:
            entries[entry[0]]["times"].append(entry[1])
            entries[entry[0]]["currents"].append(entry[2])
            entries[entry[0]]["errors"].append(0 if len(entry) < 4 else entry[3])
        return entries
    def fitVoltagePoint(self, voltage, output_dir):
        canvas = ROOT.TCanvas("v%i" % int(voltage))
        if output_dir != "" and not os.path.isdir(output_dir):
            OutputTools.makeDirectory(output_dir)
        entry = self.entries[voltage]
        graph = ROOT.TGraphErrors(len([x for x in entry["currents"] if x > 0]))
        graph.SetName("V=%s" % int(voltage))
        graph.SetMarkerStyle(20)
        offset = entry["times"][0]
        for j, point in enumerate(zip(entry["times"], entry["currents"], entry["errors"])):
            if point[1] < 0:
                continue
            graph.SetPoint(j, point[0] - offset, point[1])
            graph.SetPointError(j, 0, point[2])
        function = ROOT.TF1("test","[0]+[1]*exp([2]*x)",
            0, max(entry["times"]) - offset)
        function.SetParameter(0, min([x for x in entry["currents"] if x > 0]))
        function.SetParameter(1, 2)
        function.SetParameter(2, -0.1)
        fit = graph.Fit(function, "SR")
        if os.path.isdir(output_dir):
            graph.Draw("AP")
            graph.GetXaxis().SetTitle("Time (m)")
            graph.GetYaxis().SetTitle("Current (nA)")
            canvas.Print("%s/v%s.pdf" % (output_dir, int(voltage)))
        entry["stable current"] = function.GetParameter(0)
        entry["stable error"] = function.GetParError(0)
    def getCurve(self, output_dir):
        self.final_curve = ROOT.TGraphErrors(len(self.entries))
        voltages = self.entries.keys()
        voltages.sort()
        name = self.data_file.split("/")[-1].split(".")[0]
        self.final_curve.SetName("_".join([name, "final"])) 
        self.final_curve.SetTitle(name if "NAME" not in self.config_info.keys() else \
            self.config_info["NAME"]
        )
        for i, (key, value) in enumerate(self.entries.iteritems()):
            if len(value["currents"]) == 1:
                value["stable current"] = value["currents"][0]
                value["stable error"] = value["errors"][0]
            else:
                self.fitVoltagePoint(key, "/".join([output_dir, 
                    "%s_Fits" % self.data_file.split("/")[-1].split(".")[0]])
                )
            # Correction factor, using averages from 
            corr_voltage = key - value["stable current"]*0.000104
            self.final_curve.SetPoint(i, key, value["stable current"])
            self.final_curve.SetPointError(i, 0, value["stable error"]) 
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
            #embed()
            ROOT.gROOT.FindObject("final").Update() 
        self.final_curve.GetXaxis().SetTitle("Applied Voltage (V)")
        self.final_curve.GetYaxis().SetTitle("Current (nA)")
        self.final_curve.SetMinimum(0.1)
        self.final_curve.SetMaximum(max([v["stable current"] for k, v in self.entries.iteritems()]))
        self.final_curve.SetMarkerStyle(20)
        self.final_curve.SetMarkerSize(1)
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
            fit_text.AddText("I(%i) = %i nA" % (int(curr_point), int(round(result, 0))))
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
        return self.final_curve.GetListOfFunctions().FindObject("stats")
