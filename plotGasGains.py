#!/usr/bin/env python
import ROOT
import argparse
import os
import glob
import errno
import itertools
from Utilities import OutputTools, IVCurve

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
def getPrettyLegend(graphs, entry_size, left):
    offset = ROOT.gPad.GetRightMargin() - 0.04
    xcoords = [.20, .5] if left else [.65-offset, .90-offset]
    unique_entries = len(graphs)
    ycoords = [.9, .9 - entry_size*unique_entries]
    legend = ROOT.TLegend(xcoords[0], ycoords[0], xcoords[1], ycoords[1])
    legend.SetFillColor(0)
    for graph in graphs:
        legend.AddEntry(graph, graph.GetTitle(), "PE")
    return legend
def main():
    #data_path = "/afs/cern.ch/cms/MUON/csc/fast1-test-ISR/IVmeasurements/"
    final_canvas = ROOT.TCanvas("final", "final")
    args = getComLineArgs()
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack, ROOT.kGreen, ROOT.kGray, ROOT.kAzure]
    graphs = []
    OutputTools.makeDirectory(args.output_folder)
    for i, data_file in enumerate(args.files):
        curve = IVCurve.IVCurve(data_file)
        graphs.append(curve.getCurve(args.output_folder))
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
    legend = getPrettyLegend(graphs, 0.1, True)
    legend.Draw()
    final_canvas.Print("/".join([args.output_folder, "final.pdf"]))

if __name__ == "__main__":
        main()
