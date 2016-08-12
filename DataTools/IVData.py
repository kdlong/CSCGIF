import ROOT
import os
import math
from Utilities import OutputTools

class IVData(object):
    def __init__(self, data_file_name):
        self.config_info = {"APPLY_VCORRECTIONS" : True }
        self.data_file = data_file_name
        self.entries = self.readDataFromFile(data_file_name)
        self.name = self.data_file.split("/")[-1].split(".")[0]

    def getName(self):
        return self.name

    def readDataFromFile(self, data_file_name):
        file_info = []
        with open(self.data_file, "r") as data_file:
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
                elif len(data) == 3 and ":" not in line:
                    data.insert(1, "0")
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
            print "entry ", entry
            entries[entry[0]]["times"].append(entry[1])
            entries[entry[0]]["currents"].append(entry[2])
            entries[entry[0]]["errors"].append(0 if len(entry) < 4 else entry[3])
        return entries

    def getConfigInfo(self):
        return self.config_info

    def fitVoltagePoint(self, voltage, output_dir):
        canvas = ROOT.TCanvas("v%i" % int(voltage))
        ROOT.gStyle.SetOptFit(1)
        if output_dir != "" and not os.path.isdir(output_dir):
            OutputTools.makeDirectory(output_dir)
        entry = self.entries[voltage]
        graph = ROOT.TGraphErrors(len([x for x in entry["currents"] if x > 0]))
        graph.SetName("V=%s" % int(voltage))
        graph.SetMarkerStyle(20)
        offset = entry["times"][0]-1
        for j, point in enumerate(zip(entry["times"], entry["currents"], entry["errors"])):
            if point[1] <= 0:
                continue
            graph.SetPoint(j, point[0] - offset, point[1])
            graph.SetPointError(j, 0, point[2])
        function = ROOT.TF1("test","[0]+[1]*exp([2]*x)", 0, max(entry["times"]) - offset+1)
        function.SetParameter(0, min([x for x in entry["currents"] if x > 0]))
        function.SetParameter(1, 2)
        function.SetParameter(2, -0.1)
        print ("HV = %i V")%int(voltage)
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
            canvas.Print("%s/v%s.png" % (output_dir, int(voltage)))

        fitStatus = ROOT.gMinuit.fCstatu
        if( ("CONVERGED" in fitStatus) or (''.join(fitStatus.split())=='OK') ):
            print "ACCEPTED!\n\n"
            entry["stable current"] = function.GetParameter(0)
            entry["stable error"] = function.GetParError(0)
        else:
            print "REJECTED!\n\n"
    # HV corrections due to voltage drop on HV resistors,
    # Calculated and presented by Andrey Korytov.
    #
    # For ME1/1:
    # section B (0.3 m^2, 73%): dV = 0.192Itot [uA]
    # section A (0.11 m^2, 27%): dV = 0.072Itot [uA]
    #
    # weighted average (inversely to areas):
    # dHV = 0.192*0.73 + 0.072*0.27 = 0.1596 uA?
    #
    # For ME2/1:
    # Correcitons depend on section,
    # I_{1}, I{2}, I{3} correspond to section 1, 2, 3
    # 0.607*I1 [uA] 0.631*I2 [uA] 0.647*I3 [uA]
    #
    def getCorrectedVoltage(self, voltage, current):
        chamber = [x for x in self.name.split("_") if "ME" in x][0]
        corr_factors = {"ME11" : 0.0001596,
                "ME21s1" : 0.000607,
                "ME21s2" : 0.000631,
                "ME21s3" : 0.000647
        }
        return voltage - current*corr_factors[chamber]
    def getVoltages(self):
        voltages = self.entries.keys()
        voltages.sort()
        return voltages
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
            corr_voltage = self.getCorrectedVoltage(key, value["stable current"]) if \
                self.config_info["APPLY_VCORRECTIONS"] in [True, "True", "true"] else key
            self.data.append((corr_voltage, value["stable current"], value["stable error"]))
    def getRawData(self, output_dir):
        if not hasattr(self, "data"):
            self.loadRawData(output_dir)
        return sorted(self.data, key=lambda x: x[0])
    def subtractData(self, ivdata):
        temp_entries = {}
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
        self.name = "#splitline{ME11-L2 w/Source - Dark Cur.}{(2016/02/29, 03/24)}"
        del self.config_info["NAME"]
