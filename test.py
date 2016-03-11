import ROOT
import re

file_info = []
#with open("2016_02_16.dat") as data_file:
with open("mydata.dat") as data_file:
    time = lambda x: float(x) if ":" not in x else \
        (60*float(x.split(":")[0]) + float(x.split(":")[1]))
    for line in data_file:
        if line[0] in ["#"]:
            continue
        file_info.append([time(x) for x in line.split()])
    entries = {x : 
        {"currents" : [],
            "times": [],
            "errors" : [],
        "stable current" : 0,
        "stable error" : 0
        }
        for x in set([i[0] for i in file_info])
    }
for entry in file_info:
    entries[entry[0]]["times"].append(entry[1])
    entries[entry[0]]["currents"].append(entry[2])
    entries[entry[0]]["errors"].append(0 if len(entry) < 3 else entry[3])
final_canvas = ROOT.TCanvas("final", "final")
total_graph = ROOT.TGraphErrors(len(entries))
total_graph.SetName("Total")
i = 0
for key, value in entries.iteritems():
    if len(value["currents"]) == 1:
        value["stable current"] = value["currents"][0]
        value["stable error"] = value["errors"][0]
    else:
        canvas = ROOT.TCanvas("v%i" % int(key))
        graph = ROOT.TGraphErrors(len(value["times"]))
        graph.SetName("V=%s" % key)
        graph.GetXaxis().SetTitle("Time (m)")
        graph.GetYaxis().SetTitle("Current (nA)")
        graph.SetMarkerStyle(20)
        graph.GetXaxis().SetTile("Applied Voltage (V)")
        graph.GetYaxis().SetTile("Current (nA)")
        offset = value["times"][0]
        graph.GetXaxis().SetRangeUser(-5, value["times"][-1] - offset + 2)
        for j, point in enumerate(zip(value["times"], value["currents"])):
            graph.SetPoint(j, point[0] - offset, point[1])
            graph.SetPointError(j, 0, value["errors"][j])
        function = ROOT.TF1("test","[0]+[1]*exp([2]*x)",
            0, value["times"][-1] - offset)
        function.SetParameter(0, value["currents"][-1])
        function.SetParameter(1, 2)
        function.SetParameter(2, -0.1)
        fit = graph.Fit(function, "SR")
        value["stable current"] = function.GetParameter(0)
        value["stable error"] = function.GetParError(0)
        graph.Draw("AP")
        canvas.Print("~/www/GIFstuff/v%i.pdf" % int(key))
    total_graph.SetPoint(i, key, value["stable current"])
    total_graph.SetPointError(i, 0, value["stable error"]) 
    i += 1
final_canvas.cd()
final_canvas.SetLogy()
total_graph.GetXaxis().SetTile("Applied Voltage (V)")
total_graph.GetYaxis().SetTile("Current (nA)")
total_graph.SetMinimum(1)
total_graph.SetMarkerStyle(20)
total_graph.SetMarkerSize(1)
total_graph.Draw("AP")
final_canvas.Print("~/www/GIFstuff/final.pdf")
