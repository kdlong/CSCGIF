#!/usr/bin/env python
import ROOT
import argparse
import os

def getComLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_name", required=True,
            help="EDM file name (should be full path, starting"
                "with '/store' for file on DAS"
    )
    parser.add_argument("--discard_fits", action='store_true',
            help="Don't store plots for fits to exponential "
                "fits (for pA points)"
    )
    parser.add_argument("-o", "--output_folder", type=str,
            default="/afs/cern.ch/user/k/kelong/www/GIFstuff",
            help="Name of folder to store plots"
    )
    return parser.parse_args()
def readDataFromFile(file_name):
    file_info = []
    with open(file_name) as data_file:
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
    return entries
def fitVoltagePoint(voltage, points, output_dir):
    canvas = ROOT.TCanvas("v%i" % int(voltage))
    if output_dir != "" and not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    graph = ROOT.TGraphErrors(len(points))
    graph.SetName("V=%s" % int(voltage))
    graph.GetXaxis().SetTitle("Time (m)")
    graph.GetYaxis().SetTitle("Current (nA)")
    graph.SetMarkerStyle(20)
    graph.GetXaxis().SetTitle("Applied Voltage (V)")
    graph.GetYaxis().SetTitle("Current (nA)")
    offset = points[0][0]
    for j, point in enumerate(points):
        graph.SetPoint(j, point[0] - offset, point[1])
        graph.SetPointError(j, 0, point[2])
    function = ROOT.TF1("test","[0]+[1]*exp([2]*x)",
        0, points[-1][0] - offset)
    function.SetParameter(0, points[-1][1])
    function.SetParameter(1, 2)
    function.SetParameter(2, -0.1)
    fit = graph.Fit(function, "SR")
    if os.path.isdir(output_dir):
        graph.Draw("AP")
        graph.GetXaxis().SetRangeUser(-5, points[-1][0] - offset + 5)
        canvas.Print("%s/v%s.pdf" % (output_dir, int(voltage)))
    return (function.GetParameter(0), function.GetParError(0))
def main():
    data_path = "/afs/cern.ch/cms/MUON/csc/fast1-test-ISR/IVmeasurements/GasGain"
    args = getComLineArgs()
    entries = readDataFromFile("/".join([data_path, args.file_name]))
    final_canvas = ROOT.TCanvas("final", "final")
    total_graph = ROOT.TGraphErrors(len(entries))
    total_graph.SetName("Total")
    output_dir = "/".join([args.output_folder, 
                    "GasGain", args.file_name.split("/")[0]])
    for i, (key, value) in enumerate(entries.iteritems()):
        if len(value["currents"]) == 1:
            value["stable current"] = value["currents"][0]
            value["stable error"] = value["errors"][0]
        else:
            (value["stable current"], value["stable error"]) = fitVoltagePoint(key, 
                    zip(value["times"], value["currents"], value["errors"]),
                    "/".join([output_dir, "pAFits"])
                )
        total_graph.SetPoint(i, key, value["stable current"])
        total_graph.SetPointError(i, 0, value["stable error"]) 
    final_canvas.cd()
    final_canvas.SetLogy()
    total_graph.GetXaxis().SetTitle("Applied Voltage (V)")
    total_graph.GetYaxis().SetTitle("Current (nA)")
    total_graph.SetMinimum(1)
    total_graph.SetMarkerStyle(20)
    total_graph.SetMarkerSize(1)
    total_graph.Draw("AP")
    final_canvas.Print("/".join([output_dir, "final.pdf"]))

if __name__ == "__main__":
        main()
