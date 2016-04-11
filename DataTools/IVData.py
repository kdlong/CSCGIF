import ROOT
import os
import math
from Utilities import OutputTools

class IVData(object):
    def __init__(self, data_file_name):
        self.config_info = {}
        self.data_file = data_file_name
        self.entries = self.readDataFromFile(data_file_name)
        self.name = self.data_file.split("/")[-1].split(".")[0]
    def getName(self):
        return self.name
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
    def getConfigInfo(self):
        return self.config_info
    def fitVoltagePoint(self, voltage, output_dir):
        canvas = ROOT.TCanvas("v%i" % int(voltage))
        if output_dir != "" and not os.path.isdir(output_dir):
            OutputTools.makeDirectory(output_dir)
        entry = self.entries[voltage]
        graph = ROOT.TGraphErrors(len([x for x in entry["currents"] if x > 0])+1)
        graph.SetName("V=%s" % int(voltage))
        graph.SetMarkerStyle(20)
        offset = entry["times"][0]
        for j, point in enumerate(zip(entry["times"], entry["currents"], entry["errors"])):
            if point[1] <= 0:
                continue
            graph.SetPoint(j, point[0] - offset, point[1])
            graph.SetPointError(j, 0, point[2])
        function = ROOT.TF1("test","[0]+[1]*exp([2]*x)",
            0.1, max(entry["times"]) - offset)
        function.SetParameter(0, min([x for x in entry["currents"] if x > 0]))
        function.SetParameter(1, 2)
        function.SetParameter(2, -0.1)
        fit = graph.Fit(function, "SR")
        if os.path.isdir(output_dir):
            graph.Draw("AP")
            graph.GetXaxis().SetTitle("Time (m)")
            graph.GetYaxis().SetTitle("Current (nA)")
            fit_text = ROOT.TPaveText(0.15, 0.15, 0.45, 0.22, "NDCnb")
            fit_text.SetFillColor(0)
            fit_text.SetName(graph.GetName() + "_fittext")
            fit_text.AddText("Fit for V_{applied} = %i V" % int(voltage))
            fit_text.AddText("Fit function: [0]+[1]*exp([2]*x)")
            fit_text.Draw()
            canvas.Print("%s/v%s.pdf" % (output_dir, int(voltage)))
        entry["stable current"] = function.GetParameter(0)
        entry["stable error"] = function.GetParError(0)
    # HV corrections due to voltage drop on HV resistors,
    # Calculated and presented by Andrey Korytov.
    #
    # For ME1/1:
    # section B (0.3 m^2, 73%): dV = 0.192Itot [uA]
    # section A (0.11 m^2, 27%): dV = 0.072Itot [uA]
    #
    # weighted average (inversely to areas):
    # dHV = 0.192*0.73 + 0.072*0.27 = 0.1596 uA?!?
    # dHV = 0.192*0.27 + 0.072*0.73 = 0.1044 uA?!?
    #
    # For ME2/1:
    # 0.607I1 [uA] 0.631I2 [uA] 0.647I3 [uA]
    # Areas: HV1: 0.45 m^2 (27.1%)
    # Areas: HV2: 0.54 m^2 (32.5%)
    # Areas: HV3: 0.67 m^2 (40.4%)
    #
    # Weighted average:
    # dHV = 0.607*0.271 + 0.631*0.325 + 0.67*0.404
    # dHV = 0.6403 uA
    def getVoltages(self):
        voltages = self.entries.keys()
        voltages.sort()
        return voltages
    def getCorrectedVoltage(self, voltage, current, chamber):
        corr_factors = {"ME11" : 0.0001044,
                "ME21" : 0.0006403
        }
        return voltage - current*corr_factors[chamber]
    def getEntries(self):
        return self.entries
    def loadRawData(self, output_dir=""):
        self.data = []
        for i, (key, value) in enumerate(self.entries.iteritems()):
            if len(value["currents"]) == 1:
                value["stable current"] = value["currents"][0]
                value["stable error"] = value["errors"][0]
            else:
                self.fitVoltagePoint(key, "/".join([output_dir, 
                    "%s_Fits" % self.data_file.split("/")[-1].split(".")[0]]) if \
                        output_dir != "" else ""
                )
            corr_voltage = self.getCorrectedVoltage(key, value["stable current"], 
                "ME11" if "ME11" in self.data_file else "ME21")
            self.data.append((corr_voltage, value["stable current"], value["stable error"]))
    def getRawData(self, output_dir):
        if not hasattr(self, "data"):
            self.loadRawData(output_dir)
        return self.data
    def subtractData(self, ivdata):
        temp_entries = {}
        self.name = "ME11-L1 Gain - Dark Cur."
        del self.config_info["NAME"]
        for key, value in ivdata.getEntries().iteritems():
            if key in self.entries:
                temp_entries.update({key : self.entries[key]})
                temp_entries[key]["stable current"] -= value["stable current"]
                temp_entries[key]["currents"] = [temp_entries[key]["stable current"]]
                temp_entries[key]["times"] = [0]
                self.entries[key]["stable error"] = math.sqrt(
                    value["stable current"]*value["stable current"] + 
                    self.entries[key]["stable error"]*self.entries[key]["stable error"] 
                )
        self.entries = temp_entries
        self.loadRawData()
