#!/usr/bin/env python
import ROOT
import argparse
import os
import glob
import errno
import itertools

config_info = {}
def getComLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", required=True,
            type=lambda x : itertools.chain(
                *[glob.glob(i.strip()) for i in x.split(",")]
            ),
            help="List of files of data files to plot, separated "
            "commas. Unix wildcards will be expanded"
    )
    parser.add_argument("--discard_fits", action='store_true',
            help="Don't store plots for fits to exponential "
                "fits (for pA points)"
    )
    parser.add_argument("--logy", action='store_true',
            help="Use log scale for y-axis"
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
            elif "=" in line:
                (key, value) = line.split("=")
                config_info[key.strip()] = value.strip()
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
def fitVoltagePoint(voltage, points, output_dir):
    canvas = ROOT.TCanvas("v%i" % int(voltage))
    if output_dir != "" and not os.path.isdir(output_dir):
        makeDirectory(output_dir)
    graph = ROOT.TGraphErrors(len(points))
    graph.SetName("V=%s" % int(voltage))
    graph.GetXaxis().SetTitle("Time (m)")
    graph.GetYaxis().SetTitle("Current (nA)")
    graph.SetMarkerStyle(20)
    offset = points[0][0]
    for j, point in enumerate(points):
        if point[1] < 0:
            continue
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
        graph.GetXaxis().SetTitle("Current (nA)")
        graph.GetYaxis().SetTitle("Time (min)")
        canvas.Print("%s/v%s.pdf" % (output_dir, int(voltage)))
    return (function.GetParameter(0), function.GetParError(0))
def makeDirectory(path):
    '''
    Make a directory, don't crash
    '''
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
            raise
def getCurve(data_file, output_dir):
    entries = readDataFromFile(data_file)
    total_graph = ROOT.TGraphErrors(len(entries))
    voltages = entries.keys()
    voltages.sort()
    print voltages
    total_graph.SetName("_".join(["curve", str(voltages[0]), str(voltages[-1])]))
    for i, (key, value) in enumerate(entries.iteritems()):
        if len(value["currents"]) == 1:
            value["stable current"] = value["currents"][0]
            value["stable error"] = value["errors"][0]
        else:
            (value["stable current"], value["stable error"]) = fitVoltagePoint(key, 
                    zip(value["times"], value["currents"], value["errors"]),
                    "/".join([output_dir, "%s_Fits" % data_file.split("/")[-1].split(".")[0]])
                )
        # Correction factor, using averages from 
        corr_voltage = key - value["stable current"]*0.000104
        total_graph.SetPoint(i, key, value["stable current"])
        total_graph.SetPointError(i, 0, value["stable error"]) 
    total_graph.GetXaxis().SetTitle("Applied Voltage (V)")
    total_graph.GetYaxis().SetTitle("Current (nA)")
    total_graph.SetMinimum(1)
    total_graph.SetMaximum(max([v["stable current"] for k, v in entries.iteritems()]))
    total_graph.SetMarkerStyle(20)
    total_graph.SetMarkerSize(1)
    return total_graph
def main():
    #data_path = "/afs/cern.ch/cms/MUON/csc/fast1-test-ISR/IVmeasurements/"
    final_canvas = ROOT.TCanvas("final", "final")
    args = getComLineArgs()
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack, ROOT.kGreen, ROOT.kGray, ROOT.kAzure]
    graphs = []
    makeDirectory(args.output_folder)
    for i, data_file in enumerate(args.files):
        print data_file
        graphs.append(getCurve(data_file, args.output_folder))
    ymax = 1.3*max([x.GetMaximum() for x in graphs])
    xmax = max([x.GetXaxis().GetXmax() for x in graphs])
    print "Xmax is %s" % xmax
    print "Ymax is %s" % ymax
    for i, graph in enumerate(graphs):    
        graph.SetMarkerColor(colors[i])
        if i == 0:
            graph.GetXaxis().SetLimits(0, xmax)
            graph.SetMaximum(ymax)
            graph.Draw("AP")
        else:
            graph.Draw("Psames")
    if args.logy:
        final_canvas.SetLogy()
    final_canvas.Print("/".join([args.output_folder, "final.pdf"]))

if __name__ == "__main__":
        main()
